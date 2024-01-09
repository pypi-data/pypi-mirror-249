from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.landescode import Landescode


class Adresse(BaseModel):
    """
    Contains an address that can be used for most purposes.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Adresse.svg" type="image/svg+xml"></object>

    .. HINT::
        `Adresse JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Adresse.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    adresszusatz: Annotated[str | None, Field(None, title="Adresszusatz")]
    co_ergaenzung: Annotated[str | None, Field(None, alias="coErgaenzung", title="Coergaenzung")]
    hausnummer: Annotated[str | None, Field(None, title="Hausnummer")]
    landescode: Landescode | None = Landescode.DE
    ort: Annotated[str | None, Field(None, title="Ort")]
    ortsteil: Annotated[str | None, Field(None, title="Ortsteil")]
    postfach: Annotated[str | None, Field(None, title="Postfach")]
    postleitzahl: Annotated[str | None, Field(None, title="Postleitzahl")]
    strasse: Annotated[str | None, Field(None, title="Strasse")]
