from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .auf_abschlagstaffel_pro_ort import AufAbschlagstaffelProOrt


class AufAbschlagProOrt(BaseModel):
    """
    Mit dieser Komponente können Auf- und Abschläge verschiedener Typen im Zusammenhang
    mit örtlichen Gültigkeiten abgebildet werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/AufAbschlagProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `AufAbschlagProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/AufAbschlagProOrt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    netznr: Annotated[str | None, Field(None, title="Netznr")]
    ort: Annotated[str | None, Field(None, title="Ort")]
    postleitzahl: Annotated[str | None, Field(None, title="Postleitzahl")]
    staffeln: Annotated[list[AufAbschlagstaffelProOrt] | None, Field(None, title="Staffeln")]
