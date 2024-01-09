from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .tarifpreisstaffel_pro_ort import TarifpreisstaffelProOrt


class TarifpreispositionProOrt(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden

    .. raw:: html

        <object data="../_static/images/bo4e/com/TarifpreispositionProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `TarifpreispositionProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/TarifpreispositionProOrt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    netznr: Annotated[str | None, Field(None, title="Netznr")]
    ort: Annotated[str | None, Field(None, title="Ort")]
    postleitzahl: Annotated[str | None, Field(None, title="Postleitzahl")]
    preisstaffeln: Annotated[list[TarifpreisstaffelProOrt] | None, Field(None, title="Preisstaffeln")]
