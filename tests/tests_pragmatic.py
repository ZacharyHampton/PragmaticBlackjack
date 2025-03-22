import os
from dotenv import load_dotenv
import pragmatic_blackjack

load_dotenv()


def tests_first_test():
    def dealer_handler(event: pragmatic_blackjack.Dealer, raw: str = None):
        print(event)

    table = pragmatic_blackjack.Table(
        os.getenv("TABLE_ID"), os.getenv("SESSION_ID"),
        handles={
            pragmatic_blackjack.Dealer: dealer_handler
        }
    )

    table.connect()
