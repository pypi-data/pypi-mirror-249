from enum import Enum


class Rufnummernart(str, Enum):
    """
    Abbildung verschiedener Rufnummerntypen.
    """

    RUF_ZENTRALE = "RUF_ZENTRALE"
    FAX_ZENTRALE = "FAX_ZENTRALE"
    SAMMELRUF = "SAMMELRUF"
    SAMMELFAX = "SAMMELFAX"
    ABTEILUNGRUF = "ABTEILUNGRUF"
    ABTEILUNGFAX = "ABTEILUNGFAX"
    RUF_DURCHWAHL = "RUF_DURCHWAHL"
    FAX_DURCHWAHL = "FAX_DURCHWAHL"
    MOBIL_NUMMER = "MOBIL_NUMMER"
