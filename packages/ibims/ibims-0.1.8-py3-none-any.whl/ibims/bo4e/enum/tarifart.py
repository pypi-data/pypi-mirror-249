from enum import Enum


class Tarifart(str, Enum):
    """
    Die Tarifart wird verwendet zur Charakterisierung von Zählern und daraus resultierenden Tarifen.
    """

    EINTARIF = "EINTARIF"
    ZWEITARIF = "ZWEITARIF"
    MEHRTARIF = "MEHRTARIF"
    SMART_METER = "SMART_METER"
    LEISTUNGSGEMESSEN = "LEISTUNGSGEMESSEN"
