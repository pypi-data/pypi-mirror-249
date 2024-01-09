from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class SepaInfo(BaseModel):
    """
    This class includes details about the sepa mandates.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    sepa_id: Annotated[str, Field(alias="sepaId", title="Sepaid")]
    sepa_zahler: Annotated[bool, Field(alias="sepaZahler", title="Sepazahler")]
    creditor_identifier: Annotated[str | None, Field(None, alias="creditorIdentifier", title="Creditoridentifier")]
    gueltig_seit: Annotated[AwareDatetime | None, Field(None, alias="gueltigSeit", title="Gueltigseit")]
