from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.waehrungseinheit import Waehrungseinheit


class PositionsAufAbschlag(BaseModel):
    """
    Differenzierung der zu betrachtenden Produkte anhand der preiserhöhenden (Aufschlag)
    bzw. preisvermindernden (Abschlag) Zusatzvereinbarungen,
    die individuell zu einem neuen oder bestehenden Liefervertrag abgeschlossen werden können.
    Es können mehrere Auf-/Abschläge gleichzeitig ausgewählt werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/PositionsAufAbschlag.svg" type="image/svg+xml"></object>

    .. HINT::
        `PositionsAufAbschlag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/PositionsAufAbschlag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    auf_abschlagstyp: Annotated[AufAbschlagstyp | None, Field(None, alias="aufAbschlagstyp")]
    auf_abschlagswaehrung: Annotated[Waehrungseinheit | None, Field(None, alias="aufAbschlagswaehrung")]
    auf_abschlagswert: Annotated[float | str | None, Field(None, alias="aufAbschlagswert", title="Aufabschlagswert")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
