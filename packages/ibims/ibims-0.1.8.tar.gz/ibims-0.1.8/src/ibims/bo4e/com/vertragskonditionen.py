from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .zeitraum import Zeitraum


class Vertragskonditionen(BaseModel):
    """
    Abbildung für Vertragskonditionen. Die Komponente wird sowohl im Vertrag als auch im Tarif verwendet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Vertragskonditionen.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertragskonditionen JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Vertragskonditionen.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    abschlagszyklus: Zeitraum | None = None
    anzahl_abschlaege: Annotated[float | str | None, Field(None, alias="anzahlAbschlaege", title="Anzahlabschlaege")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    kuendigungsfrist: Zeitraum | None = None
    vertragslaufzeit: Zeitraum | None = None
    vertragsverlaengerung: Zeitraum | None = None
