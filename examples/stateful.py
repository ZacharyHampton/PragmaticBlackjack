from pragmatic_blackjack import Table, HandlerBase, Event, Subscribe
from pragmatic_blackjack.event import Seat as SeatEvent
from pragmatic_blackjack.seat import Seat
import os
import logging
from dotenv import load_dotenv
import time

load_dotenv()

table = Table(os.getenv("TABLE_ID"), os.getenv("SESSION_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sit(HandlerBase):
    def __init__(self):
        super().__init__()

        self.seats: list[SeatEvent] = []
        self.seat: Seat | None = None

    @property
    def get_empty_seat(self) -> int | None:
        seat_numbers = [seat.seat_number for seat in self.seats]
        empty_seats = [x for x in range(0, 6) if x not in seat_numbers]

        if empty_seats:
            return max(empty_seats)

    def handle_seat(self, event: SeatEvent, raw: str = None):
        logger.info(f"Seated player {event.screen_name} at seat {event.seat_number}.")
        self.seats.append(event)

        if self.seat and self.seat.seat_number == event.seat_number:  #: we have successfully sat down
            time.sleep(5) # test
            self.seat.leave()
            self.seat = None
            logger.info(f"Left seat {event.seat_number}.")

    def handle_subscribe(self, event: Subscribe, raw: str = None):
        logger.info("Game is ready.")

        seat = table.sit(self.get_empty_seat)
        self.seat = seat


def main():
    custom_state = Sit()

    table.register(custom_state)
    table.connect()


if __name__ == "__main__":
    main()
