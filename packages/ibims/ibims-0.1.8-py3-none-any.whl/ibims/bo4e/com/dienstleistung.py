from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.dienstleistungstyp import Dienstleistungstyp


class Dienstleistung(BaseModel):
    """
    Abbildung einer abrechenbaren Dienstleistung.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Dienstleistung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Dienstleistung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Dienstleistung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    dienstleistungstyp: Dienstleistungstyp | None = None
