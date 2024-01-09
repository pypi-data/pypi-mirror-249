from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class StandorteigenschaftenStrom(BaseModel):
    """
    Standorteigenschaften der Sparte Strom

    .. raw:: html

        <object data="../_static/images/bo4e/com/StandorteigenschaftenStrom.svg" type="image/svg+xml"></object>

    .. HINT::
        `StandorteigenschaftenStrom JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/StandorteigenschaftenStrom.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bilanzierungsgebiet_eic: Annotated[
        str | None, Field(None, alias="bilanzierungsgebietEic", title="Bilanzierungsgebieteic")
    ]
    regelzone: Annotated[str | None, Field(None, title="Regelzone")]
    regelzone_eic: Annotated[str | None, Field(None, alias="regelzoneEic", title="Regelzoneeic")]
