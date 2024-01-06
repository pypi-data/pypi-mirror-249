from enum import Enum


class Marktrolle(str, Enum):
    """
    Diese Rollen kann ein Marktteilnehmer einnehmen.
    """

    NB = "NB"
    LF = "LF"
    MSB = "MSB"
    DL = "DL"
    BKV = "BKV"
    BKO = "BKO"
    UENB = "UENB"
    KUNDE_SELBST_NN = "KUNDE_SELBST_NN"
    MGV = "MGV"
    EIV = "EIV"
    RB = "RB"
    KUNDE = "KUNDE"
    INTERESSENT = "INTERESSENT"
    BTR = "BTR"
