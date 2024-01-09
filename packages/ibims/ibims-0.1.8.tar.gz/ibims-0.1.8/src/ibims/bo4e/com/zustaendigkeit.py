from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.themengebiet import Themengebiet


class Zustaendigkeit(BaseModel):
    """
    Enthält die zeitliche Zuordnung eines Ansprechpartners zu Abteilungen und Zuständigkeiten.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zustaendigkeit.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zustaendigkeit JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zustaendigkeit.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    abteilung: Annotated[str | None, Field(None, title="Abteilung")]
    jobtitel: Annotated[str | None, Field(None, title="Jobtitel")]
    themengebiet: Themengebiet | None = None
