from enum import Enum


class NNRechnungsart(str, Enum):
    """
    Abbildung verschiedener in der INVOIC angegebenen Rechnungsarten.
    """

    HANDELSRECHNUNG = "HANDELSRECHNUNG"
    SELBSTAUSGESTELLT = "SELBSTAUSGESTELLT"
