from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.preismodell import Preismodell
from ..enum.rechnungslegung import Rechnungslegung
from ..enum.sparte import Sparte
from ..enum.vertragsform import Vertragsform
from .ausschreibungsdetail import Ausschreibungsdetail
from .menge import Menge
from .zeitraum import Zeitraum


class Ausschreibungslos(BaseModel):
    """
    Eine Komponente zur Abbildung einzelner Lose einer Ausschreibung

    .. raw:: html

        <object data="../_static/images/bo4e/com/Ausschreibungslos.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibungslos JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Ausschreibungslos.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anzahl_lieferstellen: Annotated[int | None, Field(None, alias="anzahlLieferstellen", title="Anzahllieferstellen")]
    bemerkung: Annotated[str | None, Field(None, title="Bemerkung")]
    betreut_durch: Annotated[str | None, Field(None, alias="betreutDurch", title="Betreutdurch")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    energieart: Sparte | None = None
    gesamt_menge: Annotated[Menge | None, Field(None, alias="gesamtMenge")]
    lieferstellen: Annotated[list[Ausschreibungsdetail] | None, Field(None, title="Lieferstellen")]
    lieferzeitraum: Zeitraum | None = None
    losnummer: Annotated[str | None, Field(None, title="Losnummer")]
    preismodell: Preismodell | None = None
    wiederholungsintervall: Zeitraum | None = None
    wunsch_kuendingungsfrist: Annotated[Zeitraum | None, Field(None, alias="wunschKuendingungsfrist")]
    wunsch_maximalmenge: Annotated[Menge | None, Field(None, alias="wunschMaximalmenge")]
    wunsch_mindestmenge: Annotated[Menge | None, Field(None, alias="wunschMindestmenge")]
    wunsch_rechnungslegung: Annotated[Rechnungslegung | None, Field(None, alias="wunschRechnungslegung")]
    wunsch_vertragsform: Annotated[Vertragsform | None, Field(None, alias="wunschVertragsform")]
    wunsch_zahlungsziel: Annotated[Zeitraum | None, Field(None, alias="wunschZahlungsziel")]
