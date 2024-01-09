from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.zaehlwerk import Zaehlwerk
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.geraetemerkmal import Geraetemerkmal
from ..enum.messwerterfassung import Messwerterfassung
from ..enum.netzebene import Netzebene
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlertyp import Zaehlertyp
from .geschaeftspartner import Geschaeftspartner


class ZaehlerGas(BaseModel):
    """
    Resolve some ambiguity of `Strom` and `Gas`
    """

    model_config = ConfigDict(
        extra="allow",
    )
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.ZAEHLER, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    zaehlernummer: Annotated[str | None, Field(None, title="Zaehlernummer")]
    sparte: Sparte | None = None
    zaehlerauspraegung: Zaehlerauspraegung | None = None
    zaehlertyp: Zaehlertyp
    zaehlwerke: Annotated[list[Zaehlwerk] | None, Field(None, title="Zaehlwerke")]
    tarifart: Tarifart | None = None
    zaehlerkonstante: Annotated[float | str | None, Field(None, title="Zaehlerkonstante")]
    eichung_bis: Annotated[AwareDatetime | None, Field(None, alias="eichungBis", title="Eichungbis")]
    letzte_eichung: Annotated[AwareDatetime | None, Field(None, alias="letzteEichung", title="Letzteeichung")]
    zaehlerhersteller: Geschaeftspartner | None = None
    messwerterfassung: Messwerterfassung
    nachstes_ablesedatum: Annotated[
        AwareDatetime | None, Field(None, alias="nachstesAblesedatum", title="Nachstesablesedatum")
    ]
    aktiver_zeitraum: Annotated[Zeitraum | None, Field(None, alias="aktiverZeitraum")]
    zaehlergroesse: Geraetemerkmal
    druckniveau: Netzebene
