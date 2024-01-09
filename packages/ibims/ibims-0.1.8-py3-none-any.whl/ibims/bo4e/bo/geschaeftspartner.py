from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..enum.anrede import Anrede
from ..enum.bo_typ import BoTyp
from ..enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from ..enum.kontaktart import Kontaktart


class Geschaeftspartner(BaseModel):
    """
    Mit diesem Objekt können Geschäftspartner übertragen werden.
    Sowohl Unternehmen, als auch Privatpersonen können Geschäftspartner sein.
    Hinweis: Marktteilnehmer haben ein eigenes BO, welches sich von diesem BO ableitet.
    Hier sollte daher keine Zuordnung zu Marktrollen erfolgen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Geschaeftspartner.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geschaeftspartner JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Geschaeftspartner.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    amtsgericht: Annotated[str | None, Field(None, title="Amtsgericht")]
    anrede: Anrede | None = None
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.GESCHAEFTSPARTNER, alias="boTyp")]
    e_mail_adresse: Annotated[str | None, Field(None, alias="eMailAdresse", title="Emailadresse")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    geschaeftspartnerrolle: Annotated[list[Geschaeftspartnerrolle] | None, Field(None, title="Geschaeftspartnerrolle")]
    gewerbekennzeichnung: Annotated[bool | None, Field(None, title="Gewerbekennzeichnung")]
    glaeubiger_id: Annotated[str | None, Field(None, alias="glaeubigerId", title="Glaeubigerid")]
    hrnummer: Annotated[str | None, Field(None, title="Hrnummer")]
    kontaktweg: Annotated[list[Kontaktart] | None, Field(None, title="Kontaktweg")]
    name1: Annotated[str | None, Field(None, title="Name1")]
    name2: Annotated[str | None, Field(None, title="Name2")]
    name3: Annotated[str | None, Field(None, title="Name3")]
    partneradresse: Adresse | None = None
    umsatzsteuer_id: Annotated[str | None, Field(None, alias="umsatzsteuerId", title="Umsatzsteuerid")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
    website: Annotated[str | None, Field(None, title="Website")]
    erstellungsdatum: Annotated[AwareDatetime | None, Field(None, title="Erstellungsdatum")]
    geburtstag: Annotated[AwareDatetime | None, Field(None, title="Geburtstag")]
    telefonnummer_mobil: Annotated[str | None, Field(None, alias="telefonnummerMobil", title="Telefonnummermobil")]
    telefonnummer_privat: Annotated[str | None, Field(None, alias="telefonnummerPrivat", title="Telefonnummerprivat")]
    telefonnummer_geschaeft: Annotated[
        str | None, Field(None, alias="telefonnummerGeschaeft", title="Telefonnummergeschaeft")
    ]
    firmenname: Annotated[str | None, Field(None, title="Firmenname")]
    hausbesitzer: Annotated[bool | None, Field(None, title="Hausbesitzer")]
