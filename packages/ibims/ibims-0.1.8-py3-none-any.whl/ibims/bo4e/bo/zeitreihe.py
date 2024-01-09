from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.zeitreihenwert import Zeitreihenwert
from ..enum.bo_typ import BoTyp
from ..enum.medium import Medium
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messart import Messart
from ..enum.messgroesse import Messgroesse
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren


class Zeitreihe(BaseModel):
    """
    Abbildung einer allgemeinen Zeitreihe mit einem Wertvektor.
    Die Werte können mit wahlfreier zeitlicher Distanz im Vektor abgelegt sein.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zeitreihe.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihe JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Zeitreihe.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.ZEITREIHE, alias="boTyp")]
    einheit: Mengeneinheit | None = None
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    medium: Medium | None = None
    messart: Messart | None = None
    messgroesse: Messgroesse | None = None
    version: Annotated[str | None, Field(None, title="Version")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    werte: Annotated[list[Zeitreihenwert] | None, Field(None, title="Werte")]
    wertherkunft: Wertermittlungsverfahren | None = None
