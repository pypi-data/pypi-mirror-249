from enum import Enum


class Zeiteinheit(str, Enum):
    """
    Auflistung möglicher Einheiten zur Verwendung in zeitbezogenen Angaben.
    """

    SEKUNDE = "SEKUNDE"
    MINUTE = "MINUTE"
    STUNDE = "STUNDE"
    VIERTEL_STUNDE = "VIERTEL_STUNDE"
    TAG = "TAG"
    WOCHE = "WOCHE"
    MONAT = "MONAT"
    QUARTAL = "QUARTAL"
    HALBJAHR = "HALBJAHR"
    JAHR = "JAHR"
