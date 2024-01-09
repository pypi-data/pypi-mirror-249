from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .menge import Menge


class Vertragsteil(BaseModel):
    """
    Abbildung für einen Vertragsteil. Der Vertragsteil wird dazu verwendet,
    eine vertragliche Leistung in Bezug zu einer Lokation (Markt- oder Messlokation) festzulegen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Vertragsteil.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertragsteil JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Vertragsteil.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    lokation: Annotated[str | None, Field(None, title="Lokation")]
    maximale_abnahmemenge: Annotated[Menge | None, Field(None, alias="maximaleAbnahmemenge")]
    minimale_abnahmemenge: Annotated[Menge | None, Field(None, alias="minimaleAbnahmemenge")]
    vertraglich_fixierte_menge: Annotated[Menge | None, Field(None, alias="vertraglichFixierteMenge")]
    vertragsteilbeginn: Annotated[AwareDatetime | None, Field(None, title="Vertragsteilbeginn")]
    vertragsteilende: Annotated[AwareDatetime | None, Field(None, title="Vertragsteilende")]
