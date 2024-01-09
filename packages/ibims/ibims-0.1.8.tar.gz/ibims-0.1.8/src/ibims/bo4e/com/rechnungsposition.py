from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.zeiteinheit import Zeiteinheit
from .betrag import Betrag
from .menge import Menge
from .preis import Preis
from .steuerbetrag import Steuerbetrag


class Rechnungsposition(BaseModel):
    """
    Über Rechnungspositionen werden Rechnungen strukturiert.
    In einem Rechnungsteil wird jeweils eine in sich geschlossene Leistung abgerechnet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Rechnungsposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Rechnungsposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Rechnungsposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    artikel_id: Annotated[str | None, Field(None, alias="artikelId", title="Artikelid")]
    artikelnummer: BDEWArtikelnummer | None = None
    einzelpreis: Preis | None = None
    lieferung_bis: Annotated[AwareDatetime | None, Field(None, alias="lieferungBis", title="Lieferungbis")]
    lieferung_von: Annotated[AwareDatetime | None, Field(None, alias="lieferungVon", title="Lieferungvon")]
    lokations_id: Annotated[str | None, Field(None, alias="lokationsId", title="Lokationsid")]
    positions_menge: Annotated[Menge | None, Field(None, alias="positionsMenge")]
    positionsnummer: Annotated[int | None, Field(None, title="Positionsnummer")]
    positionstext: Annotated[str | None, Field(None, title="Positionstext")]
    teilrabatt_netto: Annotated[Betrag | None, Field(None, alias="teilrabattNetto")]
    teilsumme_netto: Annotated[Betrag | None, Field(None, alias="teilsummeNetto")]
    teilsumme_steuer: Annotated[Steuerbetrag | None, Field(None, alias="teilsummeSteuer")]
    zeitbezogene_menge: Annotated[Menge | None, Field(None, alias="zeitbezogeneMenge")]
    zeiteinheit: Zeiteinheit | None = None
