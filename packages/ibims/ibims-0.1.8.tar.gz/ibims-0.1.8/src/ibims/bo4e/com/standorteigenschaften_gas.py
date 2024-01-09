from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .marktgebiet_info import MarktgebietInfo


class StandorteigenschaftenGas(BaseModel):
    """
    Standorteigenschaften der Sparte Gas

    .. raw:: html

        <object data="../_static/images/bo4e/com/StandorteigenschaftenGas.svg" type="image/svg+xml"></object>

    .. HINT::
        `StandorteigenschaftenGas JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/StandorteigenschaftenGas.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    marktgebiete: Annotated[list[MarktgebietInfo] | None, Field(None, title="Marktgebiete")]
    netzkontonummern: Annotated[list[str] | None, Field(None, title="Netzkontonummern")]
