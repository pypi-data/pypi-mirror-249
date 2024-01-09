from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.kontaktart import Kontaktart
from .adresse import Adresse


class Vertragskonto(BaseModel):
    """
    Bundle common attributes of MBA and CBA.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    ouid: Annotated[int, Field(title="Ouid")]
    vertrags_adresse: Annotated[Adresse, Field(alias="vertragsAdresse")]
    vertragskontonummer: Annotated[str, Field(title="Vertragskontonummer")]
    rechnungsstellung: Kontaktart
