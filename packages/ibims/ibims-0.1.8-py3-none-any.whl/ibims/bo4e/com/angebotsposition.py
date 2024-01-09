from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .betrag import Betrag
from .menge import Menge
from .preis import Preis


class Angebotsposition(BaseModel):
    """
    Unterhalb von Angebotsteilen sind die Angebotspositionen eingebunden.
    Hier werden die angebotenen Bestandteile einzeln aufgeführt. Beispiel:
    Positionsmenge: 4000 kWh
    Positionspreis: 24,56 ct/kWh
    Positionskosten: 982,40 EUR

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Angebotsposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    positionsbezeichnung: Annotated[str | None, Field(None, title="Positionsbezeichnung")]
    positionskosten: Betrag | None = None
    positionsmenge: Menge | None = None
    positionspreis: Preis | None = None
