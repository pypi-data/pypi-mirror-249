from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..bo.vertrag import Vertrag
from ..enum.kontaktart import Kontaktart
from .adresse import Adresse


class VertragskontoCBA(BaseModel):
    """
    Models a CBA (child billing account) which directly relates to a single contract. It contains information about
    locks and billing dates. But in the first place, CBAs will be grouped together by the address in their contracts.
    For each group of CBAs with a common address there will be created an MBA (master billing
    account) to support that the invoices for the CBAs can be bundled into a single invoice for the MBA.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    ouid: Annotated[int, Field(title="Ouid")]
    vertrags_adresse: Annotated[Adresse, Field(alias="vertragsAdresse")]
    vertragskontonummer: Annotated[str, Field(title="Vertragskontonummer")]
    rechnungsstellung: Kontaktart
    vertrag: Vertrag
    erstellungsdatum: Annotated[AwareDatetime, Field(title="Erstellungsdatum")]
    rechnungsdatum_start: Annotated[AwareDatetime, Field(alias="rechnungsdatumStart", title="Rechnungsdatumstart")]
    rechnungsdatum_naechstes: Annotated[
        AwareDatetime, Field(alias="rechnungsdatumNaechstes", title="Rechnungsdatumnaechstes")
    ]
