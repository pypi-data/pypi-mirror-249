from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.zaehlwerk import Zaehlwerk
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.messwerterfassung import Messwerterfassung
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlertyp import Zaehlertyp
from .geschaeftspartner import Geschaeftspartner


class Zaehler(BaseModel):
    """
    Object containing information about a meter/"Zaehler".

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zaehler.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehler JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Zaehler.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.ZAEHLER, alias="boTyp")]
    eichung_bis: Annotated[AwareDatetime | None, Field(None, alias="eichungBis", title="Eichungbis")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    letzte_eichung: Annotated[AwareDatetime | None, Field(None, alias="letzteEichung", title="Letzteeichung")]
    sparte: Sparte | None = None
    tarifart: Tarifart | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    zaehlerauspraegung: Zaehlerauspraegung | None = None
    zaehlerhersteller: Geschaeftspartner | None = None
    zaehlerkonstante: Annotated[float | str | None, Field(None, title="Zaehlerkonstante")]
    zaehlernummer: Annotated[str | None, Field(None, title="Zaehlernummer")]
    zaehlertyp: Zaehlertyp | None = None
    zaehlwerke: Annotated[list[Zaehlwerk] | None, Field(None, title="Zaehlwerke")]
    messwerterfassung: Messwerterfassung
    nachstes_ablesedatum: Annotated[
        AwareDatetime | None, Field(None, alias="nachstesAblesedatum", title="Nachstesablesedatum")
    ]
    aktiver_zeitraum: Annotated[Zeitraum | None, Field(None, alias="aktiverZeitraum")]
