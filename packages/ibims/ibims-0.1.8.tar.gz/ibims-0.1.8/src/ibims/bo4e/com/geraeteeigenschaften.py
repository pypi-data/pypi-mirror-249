from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.geraetemerkmal import Geraetemerkmal
from ..enum.geraetetyp import Geraetetyp


class Geraeteeigenschaften(BaseModel):
    """
    Mit dieser Komponente werden die Eigenschaften eines Gerätes in Bezug auf den Typ und weitere Merkmale modelliert

    .. raw:: html

        <object data="../_static/images/bo4e/com/Geraeteeigenschaften.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geraeteeigenschaften JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Geraeteeigenschaften.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    geraetemerkmal: Geraetemerkmal | None = None
    geraetetyp: Geraetetyp | None = None
