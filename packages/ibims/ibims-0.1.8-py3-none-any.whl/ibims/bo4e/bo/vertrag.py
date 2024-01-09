from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.unterschrift import Unterschrift
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.vertragsteil import Vertragsteil
from ..enum.bo_typ import BoTyp
from ..enum.sparte import Sparte
from ..enum.vertragsart import Vertragsart
from ..enum.vertragsstatus import Vertragsstatus
from .geschaeftspartner import Geschaeftspartner


class Vertrag(BaseModel):
    """
    Modell für die Abbildung von Vertragsbeziehungen;
    Das Objekt dient dazu, alle Arten von Verträgen, die in der Energiewirtschaft Verwendung finden, abzubilden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Vertrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Vertrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.VERTRAG, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    sparte: Sparte | None = None
    unterzeichnervp1: Annotated[list[Unterschrift] | None, Field(None, title="Unterzeichnervp1")]
    unterzeichnervp2: Annotated[list[Unterschrift] | None, Field(None, title="Unterzeichnervp2")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    vertragsart: Vertragsart | None = None
    vertragsbeginn: Annotated[AwareDatetime | None, Field(None, title="Vertragsbeginn")]
    vertragsende: Annotated[AwareDatetime | None, Field(None, title="Vertragsende")]
    vertragskonditionen: Vertragskonditionen | None = None
    vertragsnummer: Annotated[str | None, Field(None, title="Vertragsnummer")]
    vertragspartner1: Geschaeftspartner | None = None
    vertragspartner2: Geschaeftspartner | None = None
    vertragsstatus: Vertragsstatus | None = None
    vertragsteile: Annotated[list[Vertragsteil] | None, Field(None, title="Vertragsteile")]
