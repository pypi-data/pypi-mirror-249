from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class Unterschrift(BaseModel):
    """
    Modellierung einer Unterschrift, z.B. für Verträge, Angebote etc.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Unterschrift.svg" type="image/svg+xml"></object>

    .. HINT::
        `Unterschrift JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Unterschrift.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    datum: Annotated[AwareDatetime | None, Field(None, title="Datum")]
    name: Annotated[str | None, Field(None, title="Name")]
    ort: Annotated[str | None, Field(None, title="Ort")]
