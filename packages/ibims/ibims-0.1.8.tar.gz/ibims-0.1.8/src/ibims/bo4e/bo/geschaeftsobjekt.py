from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp


class Geschaeftsobjekt(BaseModel):
    """
    Das BO Geschäftsobjekt ist der Master für alle Geschäftsobjekte.
    Alle Attribute, die hier in diesem BO enthalten sind, werden an alle BOs vererbt.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Geschaeftsobjekt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geschaeftsobjekt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Geschaeftsobjekt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.GESCHAEFTSOBJEKT, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
