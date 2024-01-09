from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.energiemix import Energiemix
from ..com.externe_referenz import ExterneReferenz
from ..com.regionale_preisgarantie import RegionalePreisgarantie
from ..com.regionale_tarifpreisposition import RegionaleTarifpreisposition
from ..com.regionaler_auf_abschlag import RegionalerAufAbschlag
from ..com.tarifberechnungsparameter import Tarifberechnungsparameter
from ..com.tarifeinschraenkung import Tarifeinschraenkung
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kundentyp import Kundentyp
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.tarifmerkmal import Tarifmerkmal
from ..enum.tariftyp import Tariftyp
from .marktteilnehmer import Marktteilnehmer


class Regionaltarif(BaseModel):
    """
    .. raw:: html

        <object data="../_static/images/bo4e/bo/Regionaltarif.svg" type="image/svg+xml"></object>

    .. HINT::
        `Regionaltarif JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Regionaltarif.json>`_
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
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.REGIONALTARIF, alias="boTyp")]
    energiemix: Energiemix | None = None
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    kundentypen: Annotated[list[Kundentyp] | None, Field(None, title="Kundentypen")]
    preisgarantien: Annotated[list[RegionalePreisgarantie] | None, Field(None, title="Preisgarantien")]
    preisstand: Annotated[AwareDatetime | None, Field(None, title="Preisstand")]
    sparte: Sparte | None = None
    tarif_auf_abschlaege: Annotated[
        list[RegionalerAufAbschlag] | None, Field(None, alias="tarifAufAbschlaege", title="Tarifaufabschlaege")
    ]
    tarifart: Tarifart | None = None
    tarifeinschraenkung: Tarifeinschraenkung | None = None
    tarifmerkmale: Annotated[list[Tarifmerkmal] | None, Field(None, title="Tarifmerkmale")]
    tarifpreise: Annotated[list[RegionaleTarifpreisposition] | None, Field(None, title="Tarifpreise")]
    tariftyp: Tariftyp | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    vertragskonditionen: Vertragskonditionen | None = None
    website: Annotated[str | None, Field(None, title="Website")]
    zeitliche_gueltigkeit: Annotated[Zeitraum | None, Field(None, alias="zeitlicheGueltigkeit")]
