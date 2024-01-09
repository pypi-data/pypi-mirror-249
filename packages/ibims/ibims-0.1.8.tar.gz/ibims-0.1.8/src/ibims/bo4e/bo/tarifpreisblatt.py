from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.auf_abschlag import AufAbschlag
from ..com.energiemix import Energiemix
from ..com.externe_referenz import ExterneReferenz
from ..com.preisgarantie import Preisgarantie
from ..com.tarifberechnungsparameter import Tarifberechnungsparameter
from ..com.tarifeinschraenkung import Tarifeinschraenkung
from ..com.tarifpreisposition import Tarifpreisposition
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kundentyp import Kundentyp
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.tarifmerkmal import Tarifmerkmal
from ..enum.tariftyp import Tariftyp
from .marktteilnehmer import Marktteilnehmer


class Tarifpreisblatt(BaseModel):
    """
    Tarifinformation mit Preisen, Aufschlägen und Berechnungssystematik

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Tarifpreisblatt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreisblatt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Tarifpreisblatt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anbieter: Marktteilnehmer | None = None
    anbietername: Annotated[str | None, Field(None, title="Anbietername")]
    anwendung_von: Annotated[AwareDatetime | None, Field(None, alias="anwendungVon", title="Anwendungvon")]
    bemerkung: Annotated[str | None, Field(None, title="Bemerkung")]
    berechnungsparameter: Tarifberechnungsparameter | None = None
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.TARIFPREISBLATT, alias="boTyp")]
    energiemix: Energiemix | None = None
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    kundentypen: Annotated[list[Kundentyp] | None, Field(None, title="Kundentypen")]
    preisgarantie: Preisgarantie | None = None
    preisstand: Annotated[AwareDatetime | None, Field(None, title="Preisstand")]
    sparte: Sparte | None = None
    tarif_auf_abschlaege: Annotated[
        list[AufAbschlag] | None, Field(None, alias="tarifAufAbschlaege", title="Tarifaufabschlaege")
    ]
    tarifart: Tarifart | None = None
    tarifeinschraenkung: Tarifeinschraenkung | None = None
    tarifmerkmale: Annotated[list[Tarifmerkmal] | None, Field(None, title="Tarifmerkmale")]
    tarifpreise: Annotated[list[Tarifpreisposition] | None, Field(None, title="Tarifpreise")]
    tariftyp: Tariftyp | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    vertragskonditionen: Vertragskonditionen | None = None
    website: Annotated[str | None, Field(None, title="Website")]
    zeitliche_gueltigkeit: Annotated[Zeitraum | None, Field(None, alias="zeitlicheGueltigkeit")]
