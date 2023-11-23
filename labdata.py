from dataclasses import dataclass, field


@dataclass
class LabData():
    locations_json: list[dict] = field(default_factory=list)
    places_json: dict = field(default_factory=list)
    places_info_json: list[dict] = field(default_factory=list)
    weather_json: dict = field(default_factory=list)
