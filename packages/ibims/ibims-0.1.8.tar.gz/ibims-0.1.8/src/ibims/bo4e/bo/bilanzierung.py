from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.lastprofil import Lastprofil
from ..enum.aggregationsverantwortung import Aggregationsverantwortung
from ..enum.bo_typ import BoTyp
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage


class Bilanzierung(BaseModel):
    """
    Bilanzierung is a business object used for balancing. This object is no BO4E standard and a complete go
    implementation can be found at
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/bilanzierung.go
    """

    model_config = ConfigDict(
        extra="allow",
    )
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    bo_typ: Annotated[BoTyp | None, Field("BILANZIERUNG", alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bilanzierungsbeginn: Annotated[AwareDatetime, Field(title="Bilanzierungsbeginn")]
    bilanzierungsende: Annotated[AwareDatetime, Field(title="Bilanzierungsende")]
    bilanzkreis: Annotated[str | None, Field(None, title="Bilanzkreis")]
    aggregationsverantwortung: Aggregationsverantwortung | None = None
    lastprofile: Annotated[list[Lastprofil] | None, Field(None, title="Lastprofile")]
    prognosegrundlage: Prognosegrundlage | None = None
    details_prognosegrundlage: Annotated[Profiltyp | None, Field(None, alias="detailsPrognosegrundlage")]
