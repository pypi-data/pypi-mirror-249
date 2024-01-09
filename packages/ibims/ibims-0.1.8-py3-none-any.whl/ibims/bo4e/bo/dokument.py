from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp


class Dokument(BaseModel):
    """
    A generic document reference like for bills, order confirmations and cancellations
    """

    model_config = ConfigDict(
        extra="allow",
    )
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.GESCHAEFTSOBJEKT, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    erstellungsdatum: Annotated[AwareDatetime, Field(title="Erstellungsdatum")]
    has_been_sent: Annotated[bool, Field(alias="hasBeenSent", title="Hasbeensent")]
    dokumentenname: Annotated[str, Field(title="Dokumentenname")]
    vorlagenname: Annotated[str, Field(title="Vorlagenname")]
