from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.adresse import Adresse
from ..com.dienstleistung import Dienstleistung
from ..com.externe_referenz import ExterneReferenz
from ..com.geokoordinaten import Geokoordinaten
from ..com.hardware import Hardware
from ..com.katasteradresse import Katasteradresse
from ..enum.bo_typ import BoTyp
from ..enum.netzebene import Netzebene
from ..enum.sparte import Sparte
from .zaehler import Zaehler


class Messlokation(BaseModel):
    """
    Object containing information about a Messlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Messlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Messlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Messlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.MESSLOKATION, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    geoadresse: Geokoordinaten | None = None
    geraete: Annotated[list[Hardware] | None, Field(None, title="Geraete")]
    grundzustaendiger_msb_codenr: Annotated[
        str | None, Field(None, alias="grundzustaendigerMsbCodenr", title="Grundzustaendigermsbcodenr")
    ]
    grundzustaendiger_msbim_codenr: Annotated[
        str | None, Field(None, alias="grundzustaendigerMsbimCodenr", title="Grundzustaendigermsbimcodenr")
    ]
    katasterinformation: Katasteradresse | None = None
    messadresse: Adresse | None = None
    messdienstleistung: Annotated[list[Dienstleistung] | None, Field(None, title="Messdienstleistung")]
    messgebietnr: Annotated[str | None, Field(None, title="Messgebietnr")]
    messlokations_id: Annotated[str | None, Field(None, alias="messlokationsId", title="Messlokationsid")]
    messlokationszaehler: Annotated[list[Zaehler] | None, Field(None, title="Messlokationszaehler")]
    netzebene_messung: Annotated[Netzebene | None, Field(None, alias="netzebeneMessung")]
    sparte: Sparte | None = None
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
