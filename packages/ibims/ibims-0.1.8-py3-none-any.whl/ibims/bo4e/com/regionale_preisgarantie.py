from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.preisgarantietyp import Preisgarantietyp
from .regionale_gueltigkeit import RegionaleGueltigkeit
from .zeitraum import Zeitraum


class RegionalePreisgarantie(BaseModel):
    """
    Abbildung einer Preisgarantie mit regionaler Abgrenzung

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionalePreisgarantie.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionalePreisgarantie JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionalePreisgarantie.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    preisgarantietyp: Preisgarantietyp | None = None
    regionale_gueltigkeit: Annotated[RegionaleGueltigkeit | None, Field(None, alias="regionaleGueltigkeit")]
    zeitliche_gueltigkeit: Annotated[Zeitraum | None, Field(None, alias="zeitlicheGueltigkeit")]
