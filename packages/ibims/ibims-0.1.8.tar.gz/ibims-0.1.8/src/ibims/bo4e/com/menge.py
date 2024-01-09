from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.mengeneinheit import Mengeneinheit


class Menge(BaseModel):
    """
    Abbildung einer Menge mit Wert und Einheit.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Menge.svg" type="image/svg+xml"></object>

    .. HINT::
        `Menge JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Menge.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    einheit: Mengeneinheit | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
