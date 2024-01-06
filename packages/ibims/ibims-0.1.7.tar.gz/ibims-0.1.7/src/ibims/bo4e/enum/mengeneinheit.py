from enum import Enum


class Mengeneinheit(str, Enum):
    """
    Einheit: Messgrößen, die per Messung oder Vorgabe ermittelt werden können.
    """

    W = "W"
    WH = "WH"
    KW = "KW"
    KWH = "KWH"
    KVARH = "KVARH"
    MW = "MW"
    MWH = "MWH"
    STUECK = "STUECK"
    KUBIKMETER = "KUBIKMETER"
    STUNDE = "STUNDE"
    TAG = "TAG"
    MONAT = "MONAT"
    JAHR = "JAHR"
    PROZENT = "PROZENT"
