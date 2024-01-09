from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .geraeteeigenschaften import Geraeteeigenschaften


class Geraet(BaseModel):
    """
    Mit dieser Komponente werden alle Geräte modelliert, die keine Zähler sind.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Geraet.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geraet JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Geraet.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    geraeteeigenschaften: Geraeteeigenschaften | None = None
    geraetenummer: Annotated[str | None, Field(None, title="Geraetenummer")]
