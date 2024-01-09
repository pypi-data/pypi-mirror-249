from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.zeitreihenwert import Zeitreihenwert
from ..enum.bo_typ import BoTyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.sparte import Sparte


class Lastgang(BaseModel):
    """
    Modell zur Abbildung eines Lastganges;
    In diesem Modell werden die Messwerte mit einem vollständigen Zeitintervall angegeben und es bietet daher eine hohe
    Flexibilität in der Übertragung jeglicher zeitlich veränderlicher Messgrössen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Lastgang.svg" type="image/svg+xml"></object>

    .. HINT::
        `Lastgang JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Lastgang.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.LASTGANG, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    lokations_id: Annotated[str | None, Field(None, alias="lokationsId", title="Lokationsid")]
    lokationstyp: Annotated[str | None, Field(None, title="Lokationstyp")]
    messgroesse: Mengeneinheit | None = None
    obis_kennzahl: Annotated[str | None, Field(None, alias="obisKennzahl", title="Obiskennzahl")]
    sparte: Sparte | None = None
    version: Annotated[str | None, Field(None, title="Version")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    werte: Annotated[list[Zeitreihenwert] | None, Field(None, title="Werte")]
