from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.ausschreibungslos import Ausschreibungslos
from ..com.externe_referenz import ExterneReferenz
from ..com.zeitraum import Zeitraum
from ..enum.ausschreibungsportal import Ausschreibungsportal
from ..enum.ausschreibungsstatus import Ausschreibungsstatus
from ..enum.ausschreibungstyp import Ausschreibungstyp
from ..enum.bo_typ import BoTyp
from .geschaeftspartner import Geschaeftspartner


class Ausschreibung(BaseModel):
    """
    Das BO Ausschreibung dient zur detaillierten Darstellung von ausgeschriebenen Energiemengen in der Energiewirtschaft

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Ausschreibung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Ausschreibung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    abgabefrist: Zeitraum | None = None
    ausschreibender: Geschaeftspartner | None = None
    ausschreibungportal: Ausschreibungsportal | None = None
    ausschreibungsnummer: Annotated[str | None, Field(None, title="Ausschreibungsnummer")]
    ausschreibungsstatus: Ausschreibungsstatus | None = None
    ausschreibungstyp: Ausschreibungstyp | None = None
    bindefrist: Zeitraum | None = None
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.AUSSCHREIUNG, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    kostenpflichtig: Annotated[bool | None, Field(None, title="Kostenpflichtig")]
    lose: Annotated[list[Ausschreibungslos] | None, Field(None, title="Lose")]
    veroeffentlichungszeitpunkt: Annotated[AwareDatetime | None, Field(None, title="Veroeffentlichungszeitpunkt")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    webseite: Annotated[str | None, Field(None, title="Webseite")]
