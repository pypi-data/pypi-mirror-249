from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.energiemix import Energiemix
from ..com.externe_referenz import ExterneReferenz
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kundentyp import Kundentyp
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.tarifmerkmal import Tarifmerkmal
from ..enum.tariftyp import Tariftyp
from .kosten import Kosten
from .marktteilnehmer import Marktteilnehmer


class Tarifkosten(BaseModel):
    """
    Objekt zur Kommunikation von Kosten, die im Rahmen der Tarifanwendung entstehen

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Tarifkosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifkosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Tarifkosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anbieter: Marktteilnehmer | None = None
    anbietername: Annotated[str | None, Field(None, title="Anbietername")]
    anwendung_von: Annotated[AwareDatetime | None, Field(None, alias="anwendungVon", title="Anwendungvon")]
    bemerkung: Annotated[str | None, Field(None, title="Bemerkung")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.TARIFKOSTEN, alias="boTyp")]
    energiemix: Energiemix | None = None
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    kosten: Kosten | None = None
    kundentypen: Annotated[list[Kundentyp] | None, Field(None, title="Kundentypen")]
    sparte: Sparte | None = None
    tarifart: Tarifart | None = None
    tarifmerkmale: Annotated[list[Tarifmerkmal] | None, Field(None, title="Tarifmerkmale")]
    tariftyp: Tariftyp | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    vertragskonditionen: Vertragskonditionen | None = None
    website: Annotated[str | None, Field(None, title="Website")]
    zeitliche_gueltigkeit: Annotated[Zeitraum | None, Field(None, alias="zeitlicheGueltigkeit")]
