from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.rufnummernart import Rufnummernart


class Rufnummer(BaseModel):
    """
    Contains information to call or fax someone

    .. raw:: html

        <object data="../_static/images/bo4e/com/Rufnummer.svg" type="image/svg+xml"></object>

    .. HINT::
        `Rufnummer JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Rufnummer.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    nummerntyp: Rufnummernart | None = None
    rufnummer: Annotated[str | None, Field(None, title="Rufnummer")]
