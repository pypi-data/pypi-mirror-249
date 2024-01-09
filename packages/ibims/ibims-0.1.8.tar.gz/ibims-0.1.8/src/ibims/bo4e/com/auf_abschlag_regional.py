from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.auf_abschlagsziel import AufAbschlagsziel
from ..enum.waehrungseinheit import Waehrungseinheit
from .auf_abschlag_pro_ort import AufAbschlagProOrt
from .energiemix import Energiemix
from .preisgarantie import Preisgarantie
from .tarifeinschraenkung import Tarifeinschraenkung
from .vertragskonditionen import Vertragskonditionen
from .zeitraum import Zeitraum


class AufAbschlagRegional(BaseModel):
    """
    Mit dieser Komponente können Auf- und Abschläge verschiedener Typen
    im Zusammenhang mit regionalen Gültigkeiten abgebildet werden.
    Hier sind auch die Auswirkungen auf verschiedene Tarifparameter modelliert,
    die sich durch die Auswahl eines Auf- oder Abschlags ergeben.

    .. raw:: html

        <object data="../_static/images/bo4e/com/AufAbschlagRegional.svg" type="image/svg+xml"></object>

    .. HINT::
        `AufAbschlagRegional JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/AufAbschlagRegional.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    auf_abschlagstyp: Annotated[AufAbschlagstyp | None, Field(None, alias="aufAbschlagstyp")]
    auf_abschlagsziel: Annotated[AufAbschlagsziel | None, Field(None, alias="aufAbschlagsziel")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    betraege: Annotated[list[AufAbschlagProOrt] | None, Field(None, title="Betraege")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    einheit: Waehrungseinheit | None = None
    einschraenkungsaenderung: Tarifeinschraenkung | None = None
    energiemixaenderung: Energiemix | None = None
    garantieaenderung: Preisgarantie | None = None
    gueltigkeitszeitraum: Zeitraum | None = None
    tarifnamensaenderungen: Annotated[str | None, Field(None, title="Tarifnamensaenderungen")]
    vertagskonditionsaenderung: Vertragskonditionen | None = None
    voraussetzungen: Annotated[list[str] | None, Field(None, title="Voraussetzungen")]
    website: Annotated[str | None, Field(None, title="Website")]
    zusatzprodukte: Annotated[list[str] | None, Field(None, title="Zusatzprodukte")]
