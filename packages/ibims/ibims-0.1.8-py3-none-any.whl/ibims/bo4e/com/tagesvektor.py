from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .zeitreihenwertkompakt import Zeitreihenwertkompakt


class Tagesvektor(BaseModel):
    """
    Abbildung eines Tagesvektors eines beliebigen äquidistanten Zeitrasters

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tagesvektor.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tagesvektor JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tagesvektor.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    tag: Annotated[AwareDatetime | None, Field(None, title="Tag")]
    werte: Annotated[list[Zeitreihenwertkompakt] | None, Field(None, title="Werte")]
