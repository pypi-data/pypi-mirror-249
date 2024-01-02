import logging
from asyncio import CancelledError, Event, Lock, Task, create_task
from asyncio import sleep as asyncio_sleep
from asyncio import sleep as notifier_asyncio_sleep
from time import perf_counter

from nicett6.utils import AsyncObservable, check_pct

_LOGGER = logging.getLogger(__name__)

POLLING_INTERVAL = 0.2


class Cover(AsyncObservable):
    """A sensor class that can be used to monitor the position of a cover"""

    MOVEMENT_THRESHOLD_INTERVAL = 2.7
    IS_CLOSED_PCT = 0.95

    def __init__(self, name, max_drop):
        super().__init__()
        self.name = name
        self.max_drop = max_drop
        self._drop_pct = 1.0
        self._prev_movement = perf_counter() - self.MOVEMENT_THRESHOLD_INTERVAL
        self._prev_drop_pct = self._drop_pct
        self._notifier = PostMovementNotifier(self)
        self.idle_event = Event()
        self.idle_event.set()

    def __repr__(self):
        return (
            f"Cover: {self.name}, {self.max_drop}, "
            f"{self._drop_pct}, {self._prev_drop_pct}, "
            f"{self._prev_movement}"
        )

    def log(self, msg, loglevel=logging.DEBUG):
        _LOGGER.log(
            loglevel,
            f"{msg}; "
            f"name: {self.name}; "
            f"max_drop: {self.max_drop}; "
            f"drop_pct: {self.drop_pct}; "
            f"_prev_drop_pct: {self._prev_drop_pct}; "
            f"is_moving: {self.is_moving}; "
            f"is_opening: {self.is_opening}; "
            f"is_closing: {self.is_closing}; "
            f"is_closed: {self.is_closed}; ",
        )

    @property
    def drop_pct(self):
        return self._drop_pct

    async def set_drop_pct(self, value):
        """Drop as a percentage (0.0 fully down to 1.0 fully up)"""
        prev_drop_pct = self._drop_pct  # Preserve state in case of exception
        self._drop_pct = check_pct(f"{self.name} drop", value)
        self._prev_drop_pct = prev_drop_pct
        await self.moved()

    @property
    def drop(self):
        return (1.0 - self._drop_pct) * self.max_drop

    async def moved(self):
        """Called to indicate movement"""
        self._prev_movement = perf_counter()
        self.idle_event.clear()
        await self._notifier.moved()
        await self.notify_observers()

    async def set_idle(self):
        """Called to indicate that movement has finished"""
        self._prev_drop_pct = self._drop_pct
        self._prev_movement = perf_counter() - self.MOVEMENT_THRESHOLD_INTERVAL
        self.idle_event.set()
        await self.notify_observers()

    async def wait_idle(self):
        _LOGGER.debug(f"State of idle_event is {self.idle_event.is_set()}")
        await self.idle_event.wait()

    @property
    def is_moving(self):
        """
        Returns True if the cover has moved recently

        When initiating movement, call self.moved() so that self.is_moving
        will be meaningful before the first POS message comes back from the cover
        """
        return perf_counter() - self._prev_movement < self.MOVEMENT_THRESHOLD_INTERVAL

    @property
    def is_closed(self):
        """Returns True if the cover is fully up (opposite of a blind)"""
        return not self.is_moving and self.drop_pct > self.IS_CLOSED_PCT

    @property
    def is_closing(self):
        """
        Returns True if the cover is going up (opposite of a blind)

        Will only be meaningful after drop_pct has been set by the first
        POS message coming back from the cover for a movement
        """
        return self.is_moving and self._drop_pct > self._prev_drop_pct

    @property
    def is_opening(self):
        """
        Returns True if the cover is going down (opposite of a blind)

        Will only be meaningful after drop_pct has been set by the first
        POS message coming back from the cover for a movement
        """
        return self.is_moving and self._drop_pct < self._prev_drop_pct

    async def set_closing(self):
        """Force the state to is_closing"""
        self._prev_drop_pct = self._drop_pct - 0.0001
        await self.moved()

    async def set_opening(self):
        """Force the state to is_opening"""
        self._prev_drop_pct = self._drop_pct + 0.0001
        await self.moved()

    async def set_target_drop_pct_hint(self, target_drop_pct):
        """ "Force the state to is_opening/closing based on target drop_pct"""
        if target_drop_pct < self._drop_pct:
            await self.set_opening()
        elif target_drop_pct > self._drop_pct:
            await self.set_closing()

    async def stop_notifier(self):
        await self._notifier.cancel_task()


async def wait_for_motion_to_complete(covers):
    """
    Poll for motion to complete

    Make sure that Cover.moving() is called when movement
    is initiated for this method to work reliably
    (see TT6Cover.handle_response_message)
    Has the side effect of notifying observers of the idle state
    """
    while True:
        await asyncio_sleep(POLLING_INTERVAL)
        if all([not cover.is_moving for cover in covers]):
            return


class PostMovementNotifier:
    """
    Invokes set_idle (and hence notify_observers) one last time after movement stops

    The cover is considered idle if it hasn't moved for
    Cover.MOVEMENT_THRESHOLD_INTERVAL + PostMovementNotifier.POST_MOVEMENT_ALLOWANCE seconds
    """

    POST_MOVEMENT_ALLOWANCE = 0.05

    def __init__(self, cover: Cover) -> None:
        self.cover = cover
        self._task_lock: Lock = Lock()
        self._task: Task | None = None

    async def moved(self) -> None:
        """
        Manage a task that will call set_idle on the cover after a short delay

        Reset the task if movement happens again while a task is running
        """
        async with self._task_lock:
            await self._cancel_task()
            self._task = create_task(self._set_idle_after_delay())
            self.cover.log("PostMovementNotifier task started", logging.DEBUG)

    async def _set_idle_after_delay(self) -> None:
        await notifier_asyncio_sleep(
            Cover.MOVEMENT_THRESHOLD_INTERVAL + self.POST_MOVEMENT_ALLOWANCE
        )
        await self.cover.set_idle()
        self.cover.log("PostMovementNotifier set to idle", logging.DEBUG)

    async def cancel_task(self):
        async with self._task_lock:
            await self._cancel_task()

    async def _cancel_task(self):
        """Cancel task - make sure you have acquired the lock first"""
        if self._task is not None:
            if not self._task.done():
                self._task.cancel()
            try:
                await self._task
            except CancelledError:
                pass
