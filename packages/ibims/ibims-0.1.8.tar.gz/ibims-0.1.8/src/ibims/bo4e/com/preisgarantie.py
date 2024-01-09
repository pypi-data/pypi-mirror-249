from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.preisgarantietyp import Preisgarantietyp
from .zeitraum import Zeitraum


class Preisgarantie(BaseModel):
    """
    Definition für eine Preisgarantie mit der Möglichkeit verschiedener Ausprägungen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisgarantie.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisgarantie JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preisgarantie.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    preisgarantietyp: Preisgarantietyp | None = None
    zeitliche_gueltigkeit: Annotated[Zeitraum | None, Field(None, alias="zeitlicheGueltigkeit")]
    creation_date: Annotated[AwareDatetime | None, Field(None, alias="creationDate", title="Creationdate")]
