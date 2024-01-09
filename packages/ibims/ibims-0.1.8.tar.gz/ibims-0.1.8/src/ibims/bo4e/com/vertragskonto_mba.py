from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.kontaktart import Kontaktart
from .adresse import Adresse
from .vertragskonto_cba import VertragskontoCBA


class VertragskontoMBA(BaseModel):
    """
    Models an MBA (master billing account). Its main purpose is to bundle CBAs together having the same address in
    their related contracts. This feature supports a single invoice for all CBAs instead of several
    invoices for each.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    ouid: Annotated[int, Field(title="Ouid")]
    vertrags_adresse: Annotated[Adresse, Field(alias="vertragsAdresse")]
    vertragskontonummer: Annotated[str, Field(title="Vertragskontonummer")]
    rechnungsstellung: Kontaktart
    cbas: Annotated[list[VertragskontoCBA], Field(title="Cbas")]
