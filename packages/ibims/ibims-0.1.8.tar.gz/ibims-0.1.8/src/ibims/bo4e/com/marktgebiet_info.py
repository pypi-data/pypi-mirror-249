from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class MarktgebietInfo(BaseModel):
    """
    Informationen zum Marktgebiet im Gas.

    .. raw:: html

        <object data="../_static/images/bo4e/com/MarktgebietInfo.svg" type="image/svg+xml"></object>

    .. HINT::
        `MarktgebietInfo JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/MarktgebietInfo.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    marktgebiet: Annotated[str | None, Field(None, title="Marktgebiet")]
    marktgebietcode: Annotated[str | None, Field(None, title="Marktgebietcode")]
