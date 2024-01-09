from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.gueltigkeitstyp import Gueltigkeitstyp
from .kriterium_wert import KriteriumWert


class RegionaleGueltigkeit(BaseModel):
    """
    Mit dieser Komponente können regionale Gültigkeiten, z.B. für Tarife, Zu- und Abschläge und Preise definiert werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionaleGueltigkeit.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionaleGueltigkeit JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionaleGueltigkeit.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    gueltigkeitstyp: Gueltigkeitstyp | None = None
    kriteriums_werte: Annotated[
        list[KriteriumWert] | None, Field(None, alias="kriteriumsWerte", title="Kriteriumswerte")
    ]
