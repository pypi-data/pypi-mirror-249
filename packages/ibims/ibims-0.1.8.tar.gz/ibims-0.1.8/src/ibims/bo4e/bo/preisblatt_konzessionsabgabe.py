from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.preisposition import Preisposition
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kundengruppe_ka import KundengruppeKA
from ..enum.preisstatus import Preisstatus
from ..enum.sparte import Sparte
from .marktteilnehmer import Marktteilnehmer


class PreisblattKonzessionsabgabe(BaseModel):
    """
    Die Variante des Preisblattmodells zur Abbildung von allgemeinen Abgaben

    .. raw:: html

        <object data="../_static/images/bo4e/bo/PreisblattKonzessionsabgabe.svg" type="image/svg+xml"></object>

    .. HINT::
        `PreisblattKonzessionsabgabe JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/PreisblattKonzessionsabgabe.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.PREISBLATTKONZESSIONSABGABE, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    gueltigkeit: Zeitraum | None = None
    herausgeber: Marktteilnehmer | None = None
    kundengruppe_ka: Annotated[KundengruppeKA | None, Field(None, alias="kundengruppeKA")]
    preispositionen: Annotated[list[Preisposition] | None, Field(None, title="Preispositionen")]
    preisstatus: Preisstatus | None = None
    sparte: Sparte | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
