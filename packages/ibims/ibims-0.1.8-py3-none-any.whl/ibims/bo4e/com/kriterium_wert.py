from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.tarifregionskriterium import Tarifregionskriterium


class KriteriumWert(BaseModel):
    """
    Mit dieser Komponente können Kriterien und deren Werte definiert werden

    .. raw:: html

        <object data="../_static/images/bo4e/com/KriteriumWert.svg" type="image/svg+xml"></object>

    .. HINT::
        `KriteriumWert JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/KriteriumWert.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    kriterium: Tarifregionskriterium | None = None
    wert: Annotated[str | None, Field(None, title="Wert")]
