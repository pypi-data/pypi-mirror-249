from enum import Enum


class Abgabeart(str, Enum):
    """
    This AbgabeArt models the Konzessionsabgabentyp.
    It contains concessionfee types needed for concessionFee mapping.
    """

    KAS = "KAS"
    SA = "SA"
    SAS = "SAS"
    TA = "TA"
    TAS = "TAS"
    TK = "TK"
    TKS = "TKS"
    TS = "TS"
    TSS = "TSS"
