from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .sepa_info import SepaInfo


class Bankverbindung(BaseModel):
    """
    This component contains bank connection information.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    iban: Annotated[str | None, Field(None, title="Iban")]
    bic: Annotated[str | None, Field(None, title="Bic")]
    gueltig_seit: Annotated[AwareDatetime | None, Field(None, alias="gueltigSeit", title="Gueltigseit")]
    gueltig_bis: Annotated[AwareDatetime | None, Field(None, alias="gueltigBis", title="Gueltigbis")]
    bankname: Annotated[str | None, Field(None, title="Bankname")]
    sepa_info: Annotated[SepaInfo | None, Field(None, alias="sepaInfo")]
    kontoinhaber: Annotated[str | None, Field(None, title="Kontoinhaber")]
    ouid: Annotated[int, Field(title="Ouid")]
