from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp


class Kampagne(BaseModel):
    """
    A "Kampagne"/campaign models which marketing activities led customers to a product/tariff.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.GESCHAEFTSOBJEKT, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    id: Annotated[str, Field(title="Id")]
    name: Annotated[str, Field(title="Name")]
