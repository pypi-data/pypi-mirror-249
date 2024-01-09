from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.messpreistyp import Messpreistyp
from ..enum.tarifkalkulationsmethode import Tarifkalkulationsmethode
from .preis import Preis
from .tarifpreis import Tarifpreis


class Tarifberechnungsparameter(BaseModel):
    """
    In dieser Komponente sind die Berechnungsparameter für die Ermittlung der Tarifkosten zusammengefasst.
    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifberechnungsparameter.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifberechnungsparameter JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifberechnungsparameter.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    berechnungsmethode: Tarifkalkulationsmethode | None = None
    hoechstpreis_ht: Annotated[Preis | None, Field(None, alias="hoechstpreisHT")]
    hoechstpreis_nt: Annotated[Preis | None, Field(None, alias="hoechstpreisNT")]
    kw_inklusive: Annotated[float | str | None, Field(None, alias="kwInklusive", title="Kwinklusive")]
    kw_weitere_mengen: Annotated[float | str | None, Field(None, alias="kwWeitereMengen", title="Kwweiteremengen")]
    messpreis_beruecksichtigen: Annotated[
        bool | None, Field(None, alias="messpreisBeruecksichtigen", title="Messpreisberuecksichtigen")
    ]
    messpreis_in_gp_enthalten: Annotated[
        bool | None, Field(None, alias="messpreisInGpEnthalten", title="Messpreisingpenthalten")
    ]
    messpreistyp: Messpreistyp | None = None
    mindestpreis: Preis | None = None
    zusatzpreise: Annotated[list[Tarifpreis] | None, Field(None, title="Zusatzpreise")]
