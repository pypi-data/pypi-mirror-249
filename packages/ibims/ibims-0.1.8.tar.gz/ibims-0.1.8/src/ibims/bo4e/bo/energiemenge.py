from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.verbrauch import Verbrauch
from ..enum.bo_typ import BoTyp
from ..enum.lokationstyp import Lokationstyp


class Energiemenge(BaseModel):
    """
    Abbildung von Mengen, die Lokationen zugeordnet sind

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Energiemenge.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemenge JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Energiemenge.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.ENERGIEMENGE, alias="boTyp")]
    energieverbrauch: Annotated[list[Verbrauch] | None, Field(None, title="Energieverbrauch")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    lokations_id: Annotated[str | None, Field(None, alias="lokationsId", title="Lokationsid")]
    lokationstyp: Lokationstyp | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
