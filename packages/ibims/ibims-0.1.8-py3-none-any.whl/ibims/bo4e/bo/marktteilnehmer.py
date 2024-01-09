from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..enum.anrede import Anrede
from ..enum.bo_typ import BoTyp
from ..enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from ..enum.kontaktart import Kontaktart
from ..enum.marktrolle import Marktrolle
from ..enum.rollencodetyp import Rollencodetyp
from ..enum.sparte import Sparte


class Marktteilnehmer(BaseModel):
    """
    Objekt zur Aufnahme der Information zu einem Marktteilnehmer

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktteilnehmer.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktteilnehmer JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Marktteilnehmer.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    amtsgericht: Annotated[str | None, Field(None, title="Amtsgericht")]
    anrede: Anrede | None = None
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.MARKTTEILNEHMER, alias="boTyp")]
    e_mail_adresse: Annotated[str | None, Field(None, alias="eMailAdresse", title="Emailadresse")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    geschaeftspartnerrolle: Annotated[list[Geschaeftspartnerrolle] | None, Field(None, title="Geschaeftspartnerrolle")]
    gewerbekennzeichnung: Annotated[bool | None, Field(None, title="Gewerbekennzeichnung")]
    glaeubiger_id: Annotated[str | None, Field(None, alias="glaeubigerId", title="Glaeubigerid")]
    hrnummer: Annotated[str | None, Field(None, title="Hrnummer")]
    kontaktweg: Annotated[list[Kontaktart] | None, Field(None, title="Kontaktweg")]
    makoadresse: Annotated[str | None, Field(None, title="Makoadresse")]
    marktrolle: Marktrolle | None = None
    name1: Annotated[str | None, Field(None, title="Name1")]
    name2: Annotated[str | None, Field(None, title="Name2")]
    name3: Annotated[str | None, Field(None, title="Name3")]
    partneradresse: Adresse | None = None
    rollencodenummer: Annotated[str | None, Field(None, title="Rollencodenummer")]
    rollencodetyp: Rollencodetyp | None = None
    sparte: Sparte | None = None
    umsatzsteuer_id: Annotated[str | None, Field(None, alias="umsatzsteuerId", title="Umsatzsteuerid")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    website: Annotated[str | None, Field(None, title="Website")]
