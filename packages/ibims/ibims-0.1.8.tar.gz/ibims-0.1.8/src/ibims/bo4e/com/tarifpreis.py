from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.preisstatus import Preisstatus
from ..enum.preistyp import Preistyp
from ..enum.waehrungseinheit import Waehrungseinheit


class Tarifpreis(BaseModel):
    """
    Abbildung eines Tarifpreises mit Preistyp und Beschreibung abgeleitet von COM Preis.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifpreis.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreis JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifpreis.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    beschreibung: Annotated[str | None, Field(None, title="Beschreibung")]
    bezugswert: Mengeneinheit | None = None
    einheit: Waehrungseinheit | None = None
    preistyp: Preistyp | None = None
    status: Preisstatus | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
