from dataclasses import dataclass
import xmltodict


@dataclass
class Event:
    @staticmethod
    def _xml_to_json(data: str) -> dict:
        return xmltodict.parse(data)
