from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class Sigmoidparameter(BaseModel):
    """
    Die Sigmoid-Funktion, beispielsweise zur Berechnung eines Leistungspreises hat die Form:
    LP=A/(1+(P/B)^C)+D

    .. raw:: html

        <object data="../_static/images/bo4e/com/Sigmoidparameter.svg" type="image/svg+xml"></object>

    .. HINT::
        `Sigmoidparameter JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Sigmoidparameter.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    a: Annotated[float | str | None, Field(None, alias="A", title="A")]
    b: Annotated[float | str | None, Field(None, alias="B", title="B")]
    c: Annotated[float | str | None, Field(None, alias="C", title="C")]
    d: Annotated[float | str | None, Field(None, alias="D", title="D")]
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
