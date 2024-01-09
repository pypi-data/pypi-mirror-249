from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..com.standorteigenschaften_gas import StandorteigenschaftenGas
from ..com.standorteigenschaften_strom import StandorteigenschaftenStrom
from ..enum.bo_typ import BoTyp


class Standorteigenschaften(BaseModel):
    """
    Modelliert die regionalen und spartenspezifischen Eigenschaften einer gegebenen Adresse.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Standorteigenschaften.svg" type="image/svg+xml"></object>

    .. HINT::
        `Standorteigenschaften JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Standorteigenschaften.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.STANDORTEIGENSCHAFTEN, alias="boTyp")]
    eigenschaften_gas: Annotated[StandorteigenschaftenGas | None, Field(None, alias="eigenschaftenGas")]
    eigenschaften_strom: Annotated[
        list[StandorteigenschaftenStrom] | None, Field(None, alias="eigenschaftenStrom", title="Eigenschaftenstrom")
    ]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
