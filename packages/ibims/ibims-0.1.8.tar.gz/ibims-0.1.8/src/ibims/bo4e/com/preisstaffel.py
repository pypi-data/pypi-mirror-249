from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .sigmoidparameter import Sigmoidparameter


class Preisstaffel(BaseModel):
    """
    Gibt die Staffelgrenzen der jeweiligen Preise an

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisstaffel.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisstaffel JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preisstaffel.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    einheitspreis: Annotated[float | str | None, Field(None, title="Einheitspreis")]
    sigmoidparameter: Sigmoidparameter | None = None
    staffelgrenze_bis: Annotated[float | str | None, Field(None, alias="staffelgrenzeBis", title="Staffelgrenzebis")]
    staffelgrenze_von: Annotated[float | str | None, Field(None, alias="staffelgrenzeVon", title="Staffelgrenzevon")]
