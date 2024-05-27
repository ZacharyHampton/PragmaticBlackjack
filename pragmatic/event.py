from dataclasses import dataclass
import xmltodict


@dataclass
class Event:
    @staticmethod
    def _xml_to_json(data: str) -> dict:
        return xmltodict.parse(data)

    @classmethod
    def from_raw(cls, data: str) -> "Event": ...


@dataclass
class Seat(Event):
    """
    Seat event
    XML Example: <seat casino_id="ppcds00000003709" country_code="CA" screen_name="itsazert" user_id="ppc1716788013363" casino_name="PP Rare Stake" num="2" event="sit" table_id="bj321mstakebj321" enrollment_date="2024-05-27" currency_code="CAD" sidebets="false" seq="3">11d74766-f84f-4168-8ff5-285cf614da8d 11d74766-f84f-4168-8ff5-285cf614da8d</seat>
    """

    casino_id: str
    country_code: str  #: can make an enum
    username: str
    user_id: str
    casino_name: str
    seat_number: int
    event: str
    table_id: str
    enrollment_date: str  #: can make a datetime
    currency_code: str  #: can make an enum
    side_bets: bool

    @classmethod
    def from_raw(cls, data: str) -> "Seat":
        data = cls._xml_to_json(data)

        return cls(
            casino_id=data["@casino_id"],
            country_code=data["@country_code"],
            username=data["@screen_name"],
            user_id=data["@user_id"],
            casino_name=data["@casino_name"],
            seat_number=int(data["@num"]),
            event=data["@event"],
            table_id=data["@table_id"],
            enrollment_date=data["@enrollment_date"],
            currency_code=data["@currency_code"],
            side_bets=data["@sidebets"] == "true",
        )
