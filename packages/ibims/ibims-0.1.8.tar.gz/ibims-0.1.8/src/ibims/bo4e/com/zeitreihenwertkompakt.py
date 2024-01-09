from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.messwertstatus import Messwertstatus
from ..enum.messwertstatuszusatz import Messwertstatuszusatz


class Zeitreihenwertkompakt(BaseModel):
    """
    Abbildung eines kompakten Zeitreihenwertes in dem ausschliesslich der Wert und Statusinformationen stehen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitreihenwertkompakt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihenwertkompakt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitreihenwertkompakt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    status: Messwertstatus | None = None
    statuszusatz: Messwertstatuszusatz | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
