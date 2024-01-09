from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.tagesvektor import Tagesvektor
from ..com.zeitintervall import Zeitintervall
from ..enum.bo_typ import BoTyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.sparte import Sparte


class LastgangKompakt(BaseModel):
    """
    Modell zur Abbildung eines kompakten Lastganges.
    In diesem Modell werden die Messwerte in Form von Tagesvektoren mit fester Anzahl von Werten übertragen.
    Daher ist dieses BO nur zur Übertragung von äquidistanten Messwertverläufen geeignet.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.LASTGANG_KOMPAKT, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    lokations_id: Annotated[str | None, Field(None, alias="lokationsId", title="Lokationsid")]
    lokationstyp: Annotated[str | None, Field(None, title="Lokationstyp")]
    messgroesse: Mengeneinheit | None = None
    obis_kennzahl: Annotated[str | None, Field(None, alias="obisKennzahl", title="Obiskennzahl")]
    sparte: Sparte | None = None
    tagesvektoren: Annotated[list[Tagesvektor] | None, Field(None, title="Tagesvektoren")]
    version: Annotated[str | None, Field(None, title="Version")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    zeitintervall: Zeitintervall | None = None
