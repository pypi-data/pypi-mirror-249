from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.geraetetyp import Geraetetyp


class Hardware(BaseModel):
    """
    Abbildung einer abrechenbaren Hardware

    .. raw:: html

        <object data="../_static/images/bo4e/com/Hardware.svg" type="image/svg+xml"></object>

    .. HINT::
        `Hardware JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Hardware.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    geraetetyp: Geraetetyp | None = None
