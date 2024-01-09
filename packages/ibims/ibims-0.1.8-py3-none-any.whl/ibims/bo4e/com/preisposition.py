from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.bemessungsgroesse import Bemessungsgroesse
from ..enum.kalkulationsmethode import Kalkulationsmethode
from ..enum.leistungstyp import Leistungstyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.steuerkennzeichen import Steuerkennzeichen
from ..enum.tarifzeit import Tarifzeit
from ..enum.waehrungseinheit import Waehrungseinheit
from ..enum.zeiteinheit import Zeiteinheit
from .preisstaffel import Preisstaffel


class Preisposition(BaseModel):
    """
    Preis für eine definierte Lieferung oder Leistung innerhalb eines Preisblattes

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preisposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bdew_artikelnummer: Annotated[BDEWArtikelnummer | None, Field(None, alias="bdewArtikelnummer")]
    berechnungsmethode: Kalkulationsmethode | None = None
    bezugsgroesse: Mengeneinheit | None = None
    freimenge_blindarbeit: Annotated[
        float | str | None, Field(None, alias="freimengeBlindarbeit", title="Freimengeblindarbeit")
    ]
    freimenge_leistungsfaktor: Annotated[
        float | str | None, Field(None, alias="freimengeLeistungsfaktor", title="Freimengeleistungsfaktor")
    ]
    gruppenartikel_id: Annotated[str | None, Field(None, alias="gruppenartikelId", title="Gruppenartikelid")]
    leistungsbezeichnung: Annotated[str | None, Field(None, title="Leistungsbezeichnung")]
    leistungstyp: Leistungstyp | None = None
    preiseinheit: Waehrungseinheit | None = None
    preisstaffeln: Annotated[list[Preisstaffel] | None, Field(None, title="Preisstaffeln")]
    tarifzeit: Tarifzeit | None = None
    zeitbasis: Zeiteinheit | None = None
    zonungsgroesse: Bemessungsgroesse | None = None
    steuersatz: Steuerkennzeichen
