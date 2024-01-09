from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.zeiteinheit import Zeiteinheit


class Zeitintervall(BaseModel):
    """
    Abbildung für ein Zeitintervall. Die Abbildung eines Zeitintervalls.
    Z.B. zur Anwendung als Raster in äquidistanten Zeitreihen/Lastgängen, beispielsweise 15 Minuten.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitintervall.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitintervall JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitintervall.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    wert: Annotated[int | None, Field(None, title="Wert")]
    zeiteinheit: Zeiteinheit | None = None
