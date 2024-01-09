from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .regionale_gueltigkeit import RegionaleGueltigkeit
from .sigmoidparameter import Sigmoidparameter


class RegionalePreisstaffel(BaseModel):
    """
    Abbildung einer Preisstaffel mit regionaler Abgrenzung

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionalePreisstaffel.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionalePreisstaffel JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionalePreisstaffel.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    einheitspreis: Annotated[float | str | None, Field(None, title="Einheitspreis")]
    regionale_gueltigkeit: Annotated[RegionaleGueltigkeit | None, Field(None, alias="regionaleGueltigkeit")]
    sigmoidparameter: Sigmoidparameter | None = None
    staffelgrenze_bis: Annotated[float | str | None, Field(None, alias="staffelgrenzeBis", title="Staffelgrenzebis")]
    staffelgrenze_von: Annotated[float | str | None, Field(None, alias="staffelgrenzeVon", title="Staffelgrenzevon")]
