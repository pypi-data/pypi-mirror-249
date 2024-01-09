from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.geraeteeigenschaften import Geraeteeigenschaften
from ..com.preisposition import Preisposition
from ..com.zeitraum import Zeitraum
from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.bo_typ import BoTyp
from ..enum.dienstleistungstyp import Dienstleistungstyp
from ..enum.netzebene import Netzebene
from ..enum.preisstatus import Preisstatus
from ..enum.sparte import Sparte
from .marktteilnehmer import Marktteilnehmer


class PreisblattHardware(BaseModel):
    """
    Variante des Preisblattmodells zur Abbildung der Preise für zusätzliche Hardware

    .. raw:: html

        <object data="../_static/images/bo4e/bo/PreisblattHardware.svg" type="image/svg+xml"></object>

    .. HINT::
        `PreisblattHardware JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/PreisblattHardware.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    basisgeraet: Geraeteeigenschaften | None = None
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    bilanzierungsmethode: Bilanzierungsmethode | None = None
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.PREISBLATTHARDWARE, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    gueltigkeit: Zeitraum | None = None
    herausgeber: Marktteilnehmer | None = None
    inklusive_dienstleistungen: Annotated[
        list[Dienstleistungstyp] | None,
        Field(None, alias="inklusiveDienstleistungen", title="Inklusivedienstleistungen"),
    ]
    inklusive_geraete: Annotated[
        list[Geraeteeigenschaften] | None, Field(None, alias="inklusiveGeraete", title="Inklusivegeraete")
    ]
    messebene: Netzebene | None = None
    preispositionen: Annotated[list[Preisposition] | None, Field(None, title="Preispositionen")]
    preisstatus: Preisstatus | None = None
    sparte: Sparte | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
