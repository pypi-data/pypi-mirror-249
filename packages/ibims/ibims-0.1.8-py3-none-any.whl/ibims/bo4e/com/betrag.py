from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.waehrungscode import Waehrungscode


class Betrag(BaseModel):
    """
    Die Komponente wird dazu verwendet, Summenbeträge (beispielsweise in Angeboten und Rechnungen) als Geldbeträge
    abzubilden. Die Einheit ist dabei immer die Hauptwährung also Euro, Dollar etc…

    .. raw:: html

        <object data="../_static/images/bo4e/com/Betrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Betrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Betrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    waehrung: Waehrungscode | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
