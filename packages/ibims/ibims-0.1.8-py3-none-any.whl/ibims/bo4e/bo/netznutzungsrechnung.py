from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.rechnungsposition import Rechnungsposition
from ..com.steuerbetrag import Steuerbetrag
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.nn_rechnungsart import NNRechnungsart
from ..enum.nn_rechnungstyp import NNRechnungstyp
from ..enum.rechnungsstatus import Rechnungsstatus
from ..enum.rechnungstyp import Rechnungstyp
from ..enum.sparte import Sparte
from .geschaeftspartner import Geschaeftspartner


class Netznutzungsrechnung(BaseModel):
    """
    Modell für die Abbildung von Netznutzungsrechnungen

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Netznutzungsrechnung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Netznutzungsrechnung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Netznutzungsrechnung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    absendercodenummer: Annotated[str | None, Field(None, title="Absendercodenummer")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.NETZNUTZUNGSRECHNUNG, alias="boTyp")]
    empfaengercodenummer: Annotated[str | None, Field(None, title="Empfaengercodenummer")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    faelligkeitsdatum: Annotated[AwareDatetime | None, Field(None, title="Faelligkeitsdatum")]
    gesamtbrutto: Betrag | None = None
    gesamtnetto: Betrag | None = None
    gesamtsteuer: Betrag | None = None
    lokations_id: Annotated[str | None, Field(None, alias="lokationsId", title="Lokationsid")]
    nnrechnungsart: NNRechnungsart | None = None
    nnrechnungstyp: NNRechnungstyp | None = None
    original: Annotated[bool | None, Field(None, title="Original")]
    original_rechnungsnummer: Annotated[
        str | None, Field(None, alias="originalRechnungsnummer", title="Originalrechnungsnummer")
    ]
    rabatt_brutto: Annotated[Betrag | None, Field(None, alias="rabattBrutto")]
    rechnungsdatum: Annotated[AwareDatetime | None, Field(None, title="Rechnungsdatum")]
    rechnungsempfaenger: Geschaeftspartner | None = None
    rechnungsersteller: Geschaeftspartner | None = None
    rechnungsnummer: Annotated[str | None, Field(None, title="Rechnungsnummer")]
    rechnungsperiode: Zeitraum | None = None
    rechnungspositionen: Annotated[list[Rechnungsposition] | None, Field(None, title="Rechnungspositionen")]
    rechnungsstatus: Rechnungsstatus | None = None
    rechnungstitel: Annotated[str | None, Field(None, title="Rechnungstitel")]
    rechnungstyp: Rechnungstyp | None = None
    simuliert: Annotated[bool | None, Field(None, title="Simuliert")]
    sparte: Sparte | None = None
    steuerbetraege: Annotated[list[Steuerbetrag] | None, Field(None, title="Steuerbetraege")]
    storno: Annotated[bool | None, Field(None, title="Storno")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    vorausgezahlt: Betrag | None = None
    zuzahlen: Betrag | None = None
