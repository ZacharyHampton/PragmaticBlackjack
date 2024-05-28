from pragmatic import Table, HandlerBase, Event, Subscribe
from pragmatic.event import Seat
import os
import logging
from dotenv import load_dotenv

load_dotenv()

table = Table(os.getenv("TABLE_ID"), os.getenv("SESSION_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sit(HandlerBase):
    def __init__(self):
        super().__init__()

        self.seats: list[Seat] = []

    @property
    def get_empty_seat(self):
        seat_numbers = [seat.seat_number for seat in self.seats]

        return max([x for x in range(0, 6) if x not in seat_numbers])

    def handle_seat(self, event: Seat, raw: str = None):
        logger.info(f"Seated player {event.screen_name} at seat {event.seat_number}.")

        self.seats.append(event)

    def handle_subscribe(self, event: Subscribe, raw: str = None):
        logger.info("Game is ready.")

        table.sit(self.get_empty_seat)


def main():
    custom_state = Sit()

    table.register(custom_state)
    table.connect()


if __name__ == "__main__":
    main()
