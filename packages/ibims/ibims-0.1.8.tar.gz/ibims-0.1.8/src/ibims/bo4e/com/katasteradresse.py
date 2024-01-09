from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class Katasteradresse(BaseModel):
    """
    Dient der Adressierung über die Liegenschafts-Information.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Katasteradresse.svg" type="image/svg+xml"></object>

    .. HINT::
        `Katasteradresse JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Katasteradresse.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    flurstueck: Annotated[str | None, Field(None, title="Flurstueck")]
    gemarkung_flur: Annotated[str | None, Field(None, alias="gemarkungFlur", title="Gemarkungflur")]
