import asyncio
import logging

from nicett6.ciw_manager import CIWManager
from nicett6.ciw_position_logger import position_logger
from nicett6.cover import Cover
from nicett6.cover_manager import CoverManager
from nicett6.image_def import ImageDef
from nicett6.ttbus_device import TTBusDeviceAddress
from nicett6.utils import parse_example_args, run_coro_after_delay

_LOGGER = logging.getLogger(__name__)


async def request_screen_position(writer, tt_addr):
    _LOGGER.info("requesting screen position")
    responses = await writer.process_request(
        writer.send_simple_command(tt_addr, "READ_POS"), 0.5
    )
    _LOGGER.info("screen position request responses: %r", responses)


async def example_ciw1(ciw: CIWManager):
    _LOGGER.info("closing screen")
    await ciw.send_close_command()
    await ciw.wait_for_motion_to_complete()
    _LOGGER.info("screen closed, opening screen")
    await ciw.send_open_command()
    await ciw.wait_for_motion_to_complete()
    _LOGGER.info("screen opened")


async def main(serial_port, example):
    async with CoverManager(serial_port) as mgr:
        screen_tt6_cover = await mgr.add_cover(
            TTBusDeviceAddress(0x02, 0x04), Cover("Screen", 1.77)
        )
        mask_tt6_cover = await mgr.add_cover(
            TTBusDeviceAddress(0x03, 0x04), Cover("Mask", 0.6)
        )
        ciw = CIWManager(
            screen_tt6_cover,
            mask_tt6_cover,
            ImageDef(0.05, 1.57, 16 / 9),
        )
        with position_logger(ciw.get_helper(), logging.INFO):
            reader_task = asyncio.create_task(mgr.message_tracker())
            example_task = asyncio.create_task(example(ciw))
            writer = mgr.conn.get_writer()
            request_task = asyncio.create_task(
                run_coro_after_delay(
                    request_screen_position(writer, ciw.screen_tt6_cover.tt_addr)
                )
            )
            await example_task
            await request_task
    await reader_task


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    examples = (("ciw1", example_ciw1),)
    serial_port, example = parse_example_args(examples)
    asyncio.run(main(serial_port, example))
