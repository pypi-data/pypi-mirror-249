from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.auf_abschlagsziel import AufAbschlagsziel
from ..enum.waehrungseinheit import Waehrungseinheit
from .preisstaffel import Preisstaffel
from .zeitraum import Zeitraum


class AufAbschlag(BaseModel):
    """
    Modell für die preiserhöhenden (Aufschlag) bzw. preisvermindernden (Abschlag) Zusatzvereinbarungen,
    die individuell zu einem neuen oder bestehenden Liefervertrag abgeschlossen wurden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/AufAbschlag.svg" type="image/svg+xml"></object>

    .. HINT::
        `AufAbschlag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/AufAbschlag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    auf_abschlagstyp: Annotated[AufAbschlagstyp | None, Field(None, alias="aufAbschlagstyp")]
    auf_abschlagsziel: Annotated[AufAbschlagsziel | None, Field(None, alias="aufAbschlagsziel")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    einheit: Waehrungseinheit | None = None
    gueltigkeitszeitraum: Zeitraum | None = None
    staffeln: Annotated[list[Preisstaffel] | None, Field(None, title="Staffeln")]
    website: Annotated[str | None, Field(None, title="Website")]
