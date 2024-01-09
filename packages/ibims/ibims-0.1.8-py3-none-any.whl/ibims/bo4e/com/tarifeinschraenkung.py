from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.voraussetzungen import Voraussetzungen
from .geraet import Geraet
from .menge import Menge


class Tarifeinschraenkung(BaseModel):
    """
    Mit dieser Komponente werden Einschränkungen für die Anwendung von Tarifen modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifeinschraenkung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifeinschraenkung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifeinschraenkung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    einschraenkungleistung: Annotated[list[Menge] | None, Field(None, title="Einschraenkungleistung")]
    einschraenkungzaehler: Annotated[list[Geraet] | None, Field(None, title="Einschraenkungzaehler")]
    voraussetzungen: Annotated[list[Voraussetzungen] | None, Field(None, title="Voraussetzungen")]
    zusatzprodukte: Annotated[list[str] | None, Field(None, title="Zusatzprodukte")]
