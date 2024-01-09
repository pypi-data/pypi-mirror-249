from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class AufAbschlagstaffelProOrt(BaseModel):
    """
    Gibt den Wert eines Auf- oder Abschlags und dessen Staffelgrenzen an

    .. raw:: html

        <object data="../_static/images/bo4e/com/AufAbschlagstaffelProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `AufAbschlagstaffelProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/AufAbschlagstaffelProOrt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    staffelgrenze_bis: Annotated[float | str | None, Field(None, alias="staffelgrenzeBis", title="Staffelgrenzebis")]
    staffelgrenze_von: Annotated[float | str | None, Field(None, alias="staffelgrenzeVon", title="Staffelgrenzevon")]
    wert: Annotated[float | str | None, Field(None, title="Wert")]
