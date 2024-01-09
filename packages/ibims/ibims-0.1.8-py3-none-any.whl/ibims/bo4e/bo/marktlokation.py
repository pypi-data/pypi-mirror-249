from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..com.geokoordinaten import Geokoordinaten
from ..com.katasteradresse import Katasteradresse
from ..com.messlokationszuordnung import Messlokationszuordnung
from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.bo_typ import BoTyp
from ..enum.energierichtung import Energierichtung
from ..enum.gasqualitaet import Gasqualitaet
from ..enum.gebiettyp import Gebiettyp
from ..enum.kundentyp import Kundentyp
from ..enum.marktgebiet import Marktgebiet
from ..enum.messtechnische_einordnung import MesstechnischeEinordnung
from ..enum.netzebene import Netzebene
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage
from ..enum.regelzone import Regelzone
from ..enum.sparte import Sparte
from ..enum.variant import Variant
from ..enum.verbrauchsart import Verbrauchsart
from .geschaeftspartner import Geschaeftspartner


class Marktlokation(BaseModel):
    """
    Object containing information about a Marktlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Marktlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bilanzierungsgebiet: Annotated[str | None, Field(None, title="Bilanzierungsgebiet")]
    bilanzierungsmethode: Bilanzierungsmethode | None = None
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.MARKTLOKATION, alias="boTyp")]
    endkunde: Geschaeftspartner | None = None
    energierichtung: Energierichtung | None = None
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    gasqualitaet: Gasqualitaet | None = None
    gebietstyp: Gebiettyp | None = None
    geoadresse: Geokoordinaten | None = None
    grundversorgercodenr: Annotated[str | None, Field(None, title="Grundversorgercodenr")]
    katasterinformation: Katasteradresse | None = None
    kundengruppen: Annotated[list[Kundentyp] | None, Field(None, title="Kundengruppen")]
    lokationsadresse: Adresse | None = None
    marktlokations_id: Annotated[str | None, Field(None, alias="marktlokationsId", title="Marktlokationsid")]
    netzbetreibercodenr: Annotated[str | None, Field(None, title="Netzbetreibercodenr")]
    netzebene: Netzebene | None = None
    netzgebietsnr: Annotated[str | None, Field(None, title="Netzgebietsnr")]
    sparte: Sparte | None = None
    unterbrechbar: Annotated[bool | None, Field(None, title="Unterbrechbar")]
    verbrauchsart: Verbrauchsart | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    zugehoerige_messlokation: Annotated[Messlokationszuordnung | None, Field(None, alias="zugehoerigeMesslokation")]
    messtechnische_einordnung: Annotated[MesstechnischeEinordnung, Field(alias="messtechnischeEinordnung")]
    uebertragungsnetzgebiet: Regelzone | None = None
    marktgebiet: Marktgebiet | None = None
    variant: Variant
    community_id: Annotated[str, Field(alias="communityId", title="Communityid")]
    prognose_grundlage: Annotated[Prognosegrundlage | None, Field(None, alias="prognoseGrundlage")]
    prognose_grundlage_detail: Annotated[Profiltyp | None, Field(None, alias="prognoseGrundlageDetail")]
