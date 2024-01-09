from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.zaehlertyp import Zaehlertyp
from .adresse import Adresse
from .menge import Menge
from .zeitraum import Zeitraum


class Ausschreibungsdetail(BaseModel):
    """
    Die Komponente Ausschreibungsdetail wird verwendet um die Informationen zu einer Abnahmestelle innerhalb eines
    Ausschreibungsloses abzubilden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Ausschreibungsdetail.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibungsdetail JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Ausschreibungsdetail.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    kunde: Annotated[str | None, Field(None, title="Kunde")]
    lastgang_vorhanden: Annotated[bool | None, Field(None, alias="lastgangVorhanden", title="Lastgangvorhanden")]
    lieferzeitraum: Zeitraum | None = None
    marktlokations_id: Annotated[str | None, Field(None, alias="marktlokationsId", title="Marktlokationsid")]
    marktlokationsadresse: Adresse | None = None
    marktlokationsbezeichnung: Annotated[str | None, Field(None, title="Marktlokationsbezeichnung")]
    netzbetreiber: Annotated[str | None, Field(None, title="Netzbetreiber")]
    netzebene_lieferung: Annotated[str | None, Field(None, alias="netzebeneLieferung", title="Netzebenelieferung")]
    netzebene_messung: Annotated[str | None, Field(None, alias="netzebeneMessung", title="Netzebenemessung")]
    prognose_arbeit_lieferzeitraum: Annotated[Menge | None, Field(None, alias="prognoseArbeitLieferzeitraum")]
    prognose_jahresarbeit: Annotated[Menge | None, Field(None, alias="prognoseJahresarbeit")]
    prognose_leistung: Annotated[Menge | None, Field(None, alias="prognoseLeistung")]
    rechnungsadresse: Adresse | None = None
    zaehlernummer: Annotated[str | None, Field(None, title="Zaehlernummer")]
    zaehlertechnik: Zaehlertyp | None = None
