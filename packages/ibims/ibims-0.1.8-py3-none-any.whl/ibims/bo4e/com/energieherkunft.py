from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.erzeugungsart import Erzeugungsart


class Energieherkunft(BaseModel):
    """
    Abbildung einer Energieherkunft

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energieherkunft.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energieherkunft JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Energieherkunft.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anteil_prozent: Annotated[float | str | None, Field(None, alias="anteilProzent", title="Anteilprozent")]
    erzeugungsart: Erzeugungsart | None = None
