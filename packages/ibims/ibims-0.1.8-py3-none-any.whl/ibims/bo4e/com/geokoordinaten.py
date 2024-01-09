from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class Geokoordinaten(BaseModel):
    """
    This component provides the geo-coordinates for a location.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Geokoordinaten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geokoordinaten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Geokoordinaten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    breitengrad: Annotated[float | str | None, Field(None, title="Breitengrad")]
    laengengrad: Annotated[float | str | None, Field(None, title="Laengengrad")]
