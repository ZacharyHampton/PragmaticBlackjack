import os
from dotenv import load_dotenv
import pragmatic

load_dotenv()


def tests_first_test():
    def dealer_handler(event: pragmatic.Dealer, raw: str = None):
        print(event)

    table = pragmatic.Table(
        os.getenv("TABLE_ID"), os.getenv("SESSION_ID"),
        handles={
            pragmatic.Dealer: dealer_handler
        }
    )

