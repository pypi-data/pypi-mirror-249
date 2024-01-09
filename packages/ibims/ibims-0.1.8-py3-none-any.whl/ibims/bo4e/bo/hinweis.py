from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp
from ..enum.hinweis_thema import HinweisThema


class Hinweis(BaseModel):
    """
    Contains specific hints for the handling of contracts and customers.
    Hints are meant to be read and written by agents or customer service employees.
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
    thema: Annotated[HinweisThema | str, Field(title="Thema")]
    nachricht: Annotated[str, Field(title="Nachricht")]
