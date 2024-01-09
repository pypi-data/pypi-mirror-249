from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.kostenblock import Kostenblock
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kostenklasse import Kostenklasse


class Kosten(BaseModel):
    """
    Dieses BO wird zur Übertagung von hierarchischen Kostenstrukturen verwendet.
    Die Kosten werden dabei in Kostenblöcke und diese wiederum in Kostenpositionen strukturiert.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Kosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Kosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.KOSTEN, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    gueltigkeit: Zeitraum | None = None
    kostenbloecke: Annotated[list[Kostenblock] | None, Field(None, title="Kostenbloecke")]
    kostenklasse: Kostenklasse | None = None
    summe_kosten: Annotated[list[Betrag] | None, Field(None, alias="summeKosten", title="Summekosten")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
