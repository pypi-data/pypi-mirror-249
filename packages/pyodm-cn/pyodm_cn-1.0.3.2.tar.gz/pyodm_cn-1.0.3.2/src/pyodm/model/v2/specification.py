import pyodm.model.definition as Model






class Mixin:

    @classmethod
    def first(cls): return cls

    @classmethod
    def find(cls, **attributes): return cls

    @classmethod
    def index(cls, i): return cls

    @classmethod
    def each(cls, usage, **attributes): return cls

    @classmethod
    def select(cls, **attributes): return cls

    @classmethod
    def usage(cls, usage): return cls



class MetaDataVersion(Mixin):
    OID = Model.Attribute()
    Name = Model.Attribute()
    CommentOID = Model.Attribute()
    Description = Model.OneElement()
    Include = Model.OneElement()
    Standards = Model.OneElement()
    AnnotatedCRF = Model.OneElement()
    SupplementalDoc = Model.OneElement()
    ValueListDef = Model.ManyElements()
    WhereClauseDef = Model.ManyElements()
    Protocol = Model.OneElement()
    WorkflowDef = Model.ManyElements()
    StudyEventGroupDef = Model.ManyElements()
    StudyEventDef = Model.ManyElements()
    ItemGroupDef = Model.ManyElements()
    ItemDef = Model.ManyElements()
    CodeList = Model.ManyElements()
    ConditionDef = Model.ManyElements()
    MethodDef = Model.ManyElements()
    CommentDef = Model.ManyElements()
    Leaf = Model.ManyElements()


class ReferenceData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ReferenceData
    """
    StudyOID = Model.Attribute()
    MetaDataVersionOID = Model.Attribute()
    ItemGroupData = Model.ManyElements()
    AuditRecord = Model.OneElement()
    Signature = Model.OneElement()
    Annotation = Model.ManyElements()


class AdminData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/AdminData+Element
    """

    StudyOID = Model.Attribute()

    User = Model.ManyElements()

    Organization = Model.ManyElements()

    Location = Model.ManyElements()

    SignatureDef = Model.ManyElements()


class User(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/User+Element
    """

    OID = Model.Attribute()

    UserType = Model.Attribute()

    OrganizationOID = Model.Attribute()

    LocationOID = Model.Attribute()

    UserName = Model.OneElement()

    Prefix = Model.OneElement()

    Suffix = Model.OneElement()

    FullName = Model.OneElement()

    GivenName = Model.OneElement()

    FamilyName = Model.OneElement()

    Image = Model.OneElement()

    Address = Model.ManyElements()

    Telecom = Model.ManyElements()


class UserName(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/UserName+Element
    """


class Prefix(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Prefix+Element
    """


class Suffix(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Suffix+Element
    """


class FullName(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/FullName+Element
    """


class GivenName(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/GivenName+Element
    """


class FamilyName(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/FamilyName+Element
    """


class Image(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Image+Element
    """

    ImageFileName = Model.Attribute()

    href = Model.Attribute()

    MimeType = Model.Attribute()


class Organization(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Organization+Element
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Role = Model.Attribute()

    Type = Model.Attribute()

    LocationOID = Model.Attribute()

    PartOfOrganizationOID = Model.Attribute()

    Description = Model.OneElement()

    Address = Model.ManyElements()

    Telecom = Model.ManyElements()


class Location(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Location+Element
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Role = Model.Attribute()

    OrganizationOID = Model.Attribute()

    Description = Model.OneElement()

    MetaDataVersionRef = Model.ManyElements()

    Address = Model.ManyElements()

    Telecom = Model.ManyElements()

    Query = Model.ManyElements()


class Address(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Address+Element
    """

    StreetName = Model.OneElement()

    HouseNumber = Model.OneElement()

    City = Model.OneElement()

    StateProv = Model.OneElement()

    Country = Model.OneElement()

    PostalCode = Model.OneElement()

    GeoPosition = Model.OneElement()

    OtherText = Model.OneElement()


class Telecom(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Telecom+Element
    """

    TelecomType = Model.Attribute()

    Value = Model.Attribute()


class StreetName(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StreetName+Element
    """


class HouseNumber(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/HouseNumber+Element
    """


class City(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/City+Element
    """


class StateProv(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StateProv+Element
    """


class Country(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Country+Element
    """


class PostalCode(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/PostalCode+Element
    """


class GeoPosition(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/GeoPosition+Element
    """

    Longitude = Model.Attribute()

    Latitude = Model.Attribute()

    Altitude = Model.Attribute()


class OtherText(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/OtherText+Element
    """


class MetaDataVersionRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/MetaDataVersionRef+Element
    """

    StudyOID = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    EffectiveDate = Model.Attribute()


class SignatureDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureDef+Element
    """

    OID = Model.Attribute()

    Methodology = Model.Attribute()

    Meaning = Model.OneElement()

    LegalReason = Model.OneElement()


class Meaning(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Meaning+Element
    """


class LegalReason(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/LegalReason+Element
    """


class ClinicalData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ClinicalData+Element
    """

    StudyOID = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    SubjectData = Model.ManyElements()

    ItemGroupData = Model.ManyElements()

    Query = Model.ManyElements()

    AuditRecord = Model.OneElement()

    Signature = Model.OneElement()

    Annotation = Model.ManyElements()


class SubjectData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SubjectData+Element
    """

    SubjectKey = Model.Attribute()

    TransactionType = Model.Attribute()

    InvestigatorRef = Model.OneElement()

    SiteRef = Model.OneElement()

    StudyEventData = Model.ManyElements()

    Query = Model.ManyElements()

    AuditRecord = Model.OneElement()

    Signature = Model.OneElement()

    Annotation = Model.ManyElements()


class SiteRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SiteRef+Element
    """

    LocationOID = Model.Attribute()


class InvestigatorRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/InvestigatorRef+Element
    """

    UserOID = Model.Attribute()


class StudyEventData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventData+Element
    """

    StudyEventOID = Model.Attribute()

    StudyEventRepeatKey = Model.Attribute()

    TransactionType = Model.Attribute()

    ItemGroupData = Model.ManyElements()

    Query = Model.ManyElements()

    AuditRecord = Model.OneElement()

    Signature = Model.OneElement()

    Annotation = Model.ManyElements()


class ItemGroupData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupData+Element
    """

    ItemGroupOID = Model.Attribute()

    ItemGroupRepeatKey = Model.Attribute()

    TransactionType = Model.Attribute()

    ItemGroupDataSeq = Model.Attribute()

    Query = Model.ManyElements()

    ItemGroupData = Model.ManyElements()

    ItemData = Model.ManyElements()

    AuditRecord = Model.OneElement()

    Signature = Model.OneElement()

    Annotation = Model.ManyElements()


class ItemData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemData+Element
    """

    ItemOID = Model.Attribute()

    TransactionType = Model.Attribute()

    IsNull = Model.Attribute()

    Value = Model.ManyElements()

    Query = Model.ManyElements()

    AuditRecord = Model.OneElement()

    Signature = Model.OneElement()

    Annotation = Model.ManyElements()


class AuditRecord(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/AuditRecord+Element
    """

    EditPoint = Model.Attribute()

    UsedMethod = Model.Attribute()

    UserRef = Model.OneElement()

    LocationRef = Model.OneElement()

    DateTimeStamp = Model.OneElement()

    ReasonForChange = Model.OneElement()

    SourceID = Model.OneElement()


class UserRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/UserRef+Element
    """

    UserOID = Model.Attribute()


class LocationRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/LocationRef+Element
    """

    LocationOID = Model.Attribute()


class DateTimeStamp(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/DateTimeStamp+Element
    """


class ReasonForChange(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ReasonForChange+Element
    """


class SourceID(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SourceID+Element
    """


class Signature(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Signature+Element
    """

    ID = Model.Attribute()

    UserRef = Model.OneElement()

    LocationRef = Model.OneElement()

    SignatureRef = Model.OneElement()

    DateTimeStamp = Model.OneElement()


class SignatureRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureRef+Element
    """

    SignatureOID = Model.Attribute()


class Alias(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Alias
    """

    Context = Model.Attribute()

    Name = Model.Attribute()


class Description(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Description
    """

    TranslatedText = Model.ManyElements()


class TranslatedText(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/TranslatedText
    """

    xml_lang = Model.Attribute()

    Type = Model.Attribute()

    xhtml_div = Model.ManyElements()


class Study(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Study
    """

    OID = Model.Attribute()

    StudyName = Model.Attribute()

    ProtocolName = Model.Attribute()

    VersionID = Model.Attribute()

    VersionName = Model.Attribute()

    Status = Model.Attribute()

    Description = Model.OneElement()

    MetaDataVersion = Model.ManyElements()


class MetaDataVersion(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/MetaDataVersion
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    Include = Model.ManyElements()

    Standards = Model.ManyElements()

    AnnotatedCRF = Model.ManyElements()

    SupplementalDoc = Model.ManyElements()

    ValueListDef = Model.ManyElements()

    WhereClauseDef = Model.ManyElements()

    Protocol = Model.ManyElements()

    WorkflowDef = Model.ManyElements()

    StudyEventGroupDef = Model.ManyElements()

    StudyEventDef = Model.ManyElements()

    ItemGroupDef = Model.ManyElements()

    ItemDef = Model.ManyElements()

    CodeList = Model.ManyElements()

    ConditionDef = Model.ManyElements()

    MethodDef = Model.ManyElements()

    CommentDef = Model.ManyElements()

    Leaf = Model.ManyElements()


class DocumentRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/DocumentRef
    """

    LeafID = Model.Attribute()

    PDFPageRef = Model.ManyElements()


class PDFPageRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/PDFPageRef
    """


class Leaf(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Leaf
    """

    ID = Model.Attribute()

    xlink_href = Model.Attribute()

    Title = Model.ManyElements()


class Title(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Title
    """


class Include(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Include
    """

    StudyOID = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    href = Model.Attribute()


class Standards(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Standards
    """

    Standard = Model.ManyElements()


class Standard(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Standard
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Type = Model.Attribute()

    PublishingSet = Model.Attribute()

    Version = Model.Attribute()

    Status = Model.Attribute()

    CommentOID = Model.Attribute()


class AnnotatedCRF(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/AnnotatedCRF
    """

    DocumentRef = Model.ManyElements()


class SupplementalDoc(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SupplementalDoc
    """

    DocumentRef = Model.ManyElements()


class ValueListDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ValueListDef
    """

    OID = Model.Attribute()

    Description = Model.ManyElements()

    ItemRef = Model.ManyElements()


class WhereClauseRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WhereClauseRef
    """

    WhereClauseOID = Model.Attribute()


class WhereClauseDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WhereClauseDef
    """

    OID = Model.Attribute()

    CommentOID = Model.Attribute()

    RangeCheck = Model.ManyElements()


class StudyEventGroupRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventGroupRef
    """

    StudyEventGroupOID = Model.Attribute()

    OrderNumber = Model.Attribute()

    Mandatory = Model.Attribute()

    CollectionExceptionConditionOID = Model.Attribute()

    Description = Model.OneElement()


class StudyEventGroupDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventGroupDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    ArmOID = Model.Attribute()

    EpochOID = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    WorkflowRef = Model.OneElement()

    Coding = Model.ManyElements()

    StudyEventGroupRef = Model.OneElement()

    StudyEventRef = Model.OneElement()


class StudyEventRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventRef
    """

    StudyEventOID = Model.Attribute()

    OrderNumber = Model.Attribute()

    Mandatory = Model.Attribute()

    CollectionExceptionConditionOID = Model.Attribute()


class StudyEventDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Repeating = Model.Attribute()

    Type = Model.Attribute()

    Category = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    ItemGroupRef = Model.ManyElements()

    WorkflowRef = Model.OneElement()

    Coding = Model.ManyElements()

    Alias = Model.ManyElements()


class ItemGroupRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupRef
    """

    ItemGroupOID = Model.Attribute()

    MethodOID = Model.Attribute()

    OrderNumber = Model.Attribute()

    Mandatory = Model.Attribute()

    CollectionExceptionConditionOID = Model.Attribute()


class ItemGroupDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Repeating = Model.Attribute()

    RepeatingLimit = Model.Attribute()

    IsReferenceData = Model.Attribute()

    Structure = Model.Attribute()

    ArchiveLocationID = Model.Attribute()

    DatasetName = Model.Attribute()

    Domain = Model.Attribute()

    Type = Model.Attribute()

    Purpose = Model.Attribute()

    StandardOID = Model.Attribute()

    IsNonStandard = Model.Attribute()

    HasNoData = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    Class = Model.ManyElements()

    Coding = Model.ManyElements()

    WorkflowRef = Model.ManyElements()

    Origin = Model.ManyElements()

    Alias = Model.ManyElements()

    Leaf = Model.ManyElements()

    ItemGroupRef = Model.OneElement()

    ItemRef = Model.OneElement()


class Class(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Class
    """

    Name = Model.Attribute()

    SubClass = Model.ManyElements()


class SubClass(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SubClass
    """


class ItemRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemRef
    """

    ItemOID = Model.Attribute()

    KeySequence = Model.Attribute()

    IsNonStandard = Model.Attribute()

    HasNoData = Model.Attribute()

    MethodOID = Model.Attribute()

    UnitsItemOID = Model.Attribute()

    Repeat = Model.Attribute()

    Other = Model.Attribute()

    Role = Model.Attribute()

    RoleCodeListOID = Model.Attribute()

    Core = Model.Attribute()

    PreSpecifiedValue = Model.Attribute()

    OrderNumber = Model.Attribute()

    Mandatory = Model.Attribute()

    CollectionExceptionConditionOID = Model.Attribute()

    Origin = Model.ManyElements()

    WhereClauseRef = Model.ManyElements()


class Origin(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Origin
    """

    Type = Model.Attribute()

    Source = Model.Attribute()

    Description = Model.OneElement()

    SourceItems = Model.OneElement()

    Coding = Model.ManyElements()

    DocumentRef = Model.ManyElements()


class SourceItems(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItems
    """

    SourceItem = Model.ManyElements()

    Coding = Model.ManyElements()


class SourceItem(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItem
    """

    ItemOID = Model.Attribute()

    ItemGroupOID = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    StudyOID = Model.Attribute()

    leafID = Model.Attribute()

    Name = Model.Attribute()

    Resource = Model.ManyElements()

    Coding = Model.ManyElements()


class Resource(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Resource
    """

    Type = Model.Attribute()

    Name = Model.Attribute()

    Attribute = Model.Attribute()

    Label = Model.Attribute()

    Selection = Model.ManyElements()


class Selection(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Selection
    """

    Path = Model.Attribute()


class ItemDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ItemDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    DataType = Model.Attribute()

    Length = Model.Attribute()

    DisplayFormat = Model.Attribute()

    VariableSet = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    Definition = Model.OneElement()

    Question = Model.OneElement()

    Prompt = Model.OneElement()

    CRFCompletionInstructions = Model.OneElement()

    ImplementationNotes = Model.OneElement()

    CDISCNotes = Model.OneElement()

    RangeCheck = Model.ManyElements()

    CodeListRef = Model.ManyElements()

    ValueListRef = Model.ManyElements()

    Coding = Model.ManyElements()

    Alias = Model.ManyElements()


class Question(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Question
    """

    TranslatedText = Model.ManyElements()


class Definition(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Definition
    """

    TranslatedText = Model.ManyElements()


class Prompt(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Prompt
    """

    TranslatedText = Model.ManyElements()


class CRFCompletionInstructions(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CRFCompletionInstructions
    """

    TranslatedText = Model.ManyElements()


class ImplementationNotes(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ImplementationNotes
    """

    TranslatedText = Model.ManyElements()


class CDISCNotes(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CDISCNotes
    """

    TranslatedText = Model.ManyElements()


class RangeCheck(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/RangeCheck
    """

    Comparator = Model.Attribute()

    SoftHard = Model.Attribute()

    ItemOID = Model.Attribute()

    ErrorMessage = Model.ManyElements()


class CheckValue(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CheckValue
    """


class ErrorMessage(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ErrorMessage
    """

    TranslatedText = Model.ManyElements()


class CodeListRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CodeListRef
    """

    CodeListOID = Model.Attribute()


class ValueListRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ValueListRef
    """

    ValueListOID = Model.Attribute()


class CodeList(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CodeList
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    DataType = Model.Attribute()

    CommentOID = Model.Attribute()

    StandardOID = Model.Attribute()

    IsNonStandard = Model.Attribute()

    Description = Model.OneElement()

    CodeListItem = Model.ManyElements()

    Coding = Model.ManyElements()

    Alias = Model.ManyElements()


class CodeListItem(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CodeListItem
    """

    CodedValue = Model.Attribute()

    Rank = Model.Attribute()

    Other = Model.Attribute()

    OrderNumber = Model.Attribute()

    ExtendedValue = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    Decode = Model.OneElement()

    Coding = Model.ManyElements()

    Alias = Model.ManyElements()


class Decode(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Decode
    """

    TranslatedText = Model.ManyElements()


class MethodDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/MethodDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Type = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    MethodSignature = Model.ManyElements()

    FormalExpression = Model.ManyElements()

    Alias = Model.ManyElements()

    DocumentRef = Model.ManyElements()


class MethodSignature(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/MethodSignature
    """

    Parameter = Model.ManyElements()

    ReturnValue = Model.ManyElements()


class Parameter(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Parameter
    """

    Name = Model.Attribute()

    DataType = Model.Attribute()

    Definition = Model.Attribute()

    OrderNumber = Model.Attribute()


class ReturnValue(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ReturnValue
    """

    Name = Model.Attribute()

    DataType = Model.Attribute()

    Definition = Model.Attribute()

    OrderNumber = Model.Attribute()


class ConditionDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ConditionDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    CommentOID = Model.Attribute()

    Description = Model.OneElement()

    MethodSignature = Model.ManyElements()

    FormalExpression = Model.ManyElements()

    Alias = Model.ManyElements()


class FormalExpression(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/FormalExpression
    """

    Context = Model.Attribute()


class Code(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Code
    """


class ExternalCodeLib(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ExternalCodeLib
    """

    Library = Model.Attribute()

    Method = Model.Attribute()

    Version = Model.Attribute()

    ref = Model.Attribute()

    href = Model.Attribute()


class CommentDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/CommentDef
    """

    OID = Model.Attribute()

    Description = Model.OneElement()

    DocumentRef = Model.ManyElements()


class ODM(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ODM
    """

    FileType = Model.Attribute()

    Granularity = Model.Attribute()

    Context = Model.Attribute()

    FileOID = Model.Attribute()

    CreationDateTime = Model.Attribute()

    PriorFileOID = Model.Attribute()

    AsOfDateTime = Model.Attribute()

    ODMVersion = Model.Attribute()

    Originator = Model.Attribute()

    SourceSystem = Model.Attribute()

    SourceSystemVersion = Model.Attribute()

    Description = Model.ManyElements()

    Study = Model.ManyElements()

    AdminData = Model.ManyElements()

    ReferenceData = Model.ManyElements()

    ClinicalData = Model.ManyElements()

    Association = Model.ManyElements()


class Association(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Association
    """

    StudyOID = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    # 手动处理了，因为标准定义了2个相同的子元素
    KeySet = Model.ManyElements()

    Annotation = Model.OneElement()


class KeySet(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/KeySet
    """

    StudyOID = Model.Attribute()

    SubjectKey = Model.Attribute()

    MetaDataVersionOID = Model.Attribute()

    StudyEventOID = Model.Attribute()

    StudyEventRepeatKey = Model.Attribute()

    ItemGroupOID = Model.Attribute()

    ItemGroupRepeatKey = Model.Attribute()

    ItemOID = Model.Attribute()


class Annotation(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Annotation
    """

    SeqNum = Model.Attribute()

    TransactionType = Model.Attribute()

    ID = Model.Attribute()

    Comment = Model.OneElement()

    Coding = Model.ManyElements()

    Flag = Model.ManyElements()


class Comment(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Comment
    """

    SponsorOrSite = Model.Attribute()

    TranslatedText = Model.ManyElements()


class Flag(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Flag
    """

    FlagValue = Model.OneElement()

    FlagType = Model.OneElement()


class FlagValue(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/FlagValue
    """

    CodeListOID = Model.Attribute()


class FlagType(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/FlagType
    """

    CodeListOID = Model.Attribute()


class Coding(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Coding
    """

    Code = Model.Attribute()

    System = Model.Attribute()

    SystemName = Model.Attribute()

    SystemVersion = Model.Attribute()

    Label = Model.Attribute()

    href = Model.Attribute()

    ref = Model.Attribute()

    CommentOID = Model.Attribute()


class Query(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Query
    """

    OID = Model.Attribute()

    Source = Model.Attribute()

    Target = Model.Attribute()

    Type = Model.Attribute()

    State = Model.Attribute()

    LastUpdateDatetime = Model.Attribute()

    Name = Model.Attribute()

    Value = Model.OneElement()

    AuditRecord = Model.ManyElements()


class Value(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Value
    """

    SeqNum = Model.Attribute()


class Protocol(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Protocol
    """

    Description = Model.OneElement()

    StudySummary = Model.OneElement()

    StudyStructure = Model.OneElement()

    TrialPhase = Model.OneElement()

    StudyTimings = Model.OneElement()

    StudyIndications = Model.OneElement()

    StudyInterventions = Model.OneElement()

    StudyObjectives = Model.OneElement()

    StudyEndPoints = Model.OneElement()

    StudyTargetPopulation = Model.OneElement()

    StudyEstimands = Model.OneElement()

    InclusionExclusionCriteria = Model.OneElement()

    StudyEventGroupRef = Model.ManyElements()

    WorkflowRef = Model.OneElement()

    Alias = Model.ManyElements()


class StudyStructure(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyStructure
    """

    Description = Model.OneElement()

    Arm = Model.ManyElements()

    Epoch = Model.ManyElements()

    WorkflowRef = Model.OneElement()


class TrialPhase(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/TrialPhase
    """

    Value = Model.Attribute()

    Description = Model.OneElement()


class StudyIndications(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIndications
    """

    StudyIndication = Model.ManyElements()


class StudyIndication(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIndication
    """

    OID = Model.Attribute()

    Description = Model.OneElement()

    Coding = Model.ManyElements()


class StudyInterventions(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyInterventions
    """

    StudyIntervention = Model.ManyElements()


class StudyIntervention(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIntervention
    """

    OID = Model.Attribute()

    Description = Model.OneElement()

    Coding = Model.ManyElements()


class StudyObjectives(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyObjectives
    """

    StudyObjective = Model.ManyElements()


class StudyObjective(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyObjective
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Level = Model.Attribute()

    Description = Model.OneElement()

    StudyEndPointRef = Model.ManyElements()


class StudyEndPointRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPointRef
    """

    StudyEndPointOID = Model.Attribute()

    OrderNumber = Model.Attribute()


class StudyEndPoints(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPoints
    """

    StudyEndPoint = Model.ManyElements()


class StudyEndPoint(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPoint
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Type = Model.Attribute()

    Level = Model.Attribute()

    Description = Model.OneElement()

    FormalExpression = Model.ManyElements()


class StudyTargetPopulation(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTargetPopulation
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Description = Model.OneElement()

    Coding = Model.ManyElements()

    FormalExpression = Model.ManyElements()


class StudyEstimands(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEstimands
    """

    StudyEstimand = Model.ManyElements()


class StudyEstimand(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEstimand
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Level = Model.Attribute()

    Description = Model.OneElement()

    StudyTargetPopulationRef = Model.OneElement()

    StudyInterventionRef = Model.OneElement()

    StudyEndPointRef = Model.OneElement()

    IntercurrentEvent = Model.ManyElements()

    SummaryMeasure = Model.OneElement()


class InclusionExclusionCriteria(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/InclusionExclusionCriteria
    """

    InclusionCriteria = Model.OneElement()

    ExclusionCriteria = Model.OneElement()


class InclusionCriteria(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/InclusionCriteria
    """

    Criterion = Model.ManyElements()


class ExclusionCriteria(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ExclusionCriteria
    """

    Criterion = Model.ManyElements()


class StudyTargetPopulationRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTargetPopulationRef
    """

    StudyTargetPopulationOID = Model.Attribute()


class StudyInterventionRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyInterventionRef
    """

    StudyInterventionOID = Model.Attribute()


class IntercurrentEvent(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/IntercurrentEvent
    """

    Description = Model.OneElement()


class SummaryMeasure(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SummaryMeasure
    """

    Description = Model.OneElement()


class Arm(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Arm
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Description = Model.OneElement()

    WorkflowRef = Model.OneElement()


class Epoch(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Epoch
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    SequenceNumber = Model.Attribute()

    Description = Model.OneElement()


class WorkflowRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowRef
    """

    WorkflowOID = Model.Attribute()


class StudySummary(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudySummary
    """

    StudyParameter = Model.ManyElements()


class StudyParameter(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyParameter
    """

    OID = Model.Attribute()

    Term = Model.Attribute()

    ShortName = Model.Attribute()

    ParameterValue = Model.ManyElements()

    Coding = Model.ManyElements()


class ParameterValue(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ParameterValue
    """

    Value = Model.Attribute()

    Coding = Model.ManyElements()


class StudyTimings(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTimings
    """

    StudyTiming = Model.ManyElements()


class StudyTiming(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTiming
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    AbsoluteTimingConstraint = Model.ManyElements()

    RelativeTimingConstraint = Model.ManyElements()

    TransitionTimingConstraint = Model.ManyElements()

    DurationTimingConstraint = Model.ManyElements()


class TransitionTimingConstraint(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/TransitionTimingConstraint
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    TransitionOID = Model.Attribute()

    MethodOID = Model.Attribute()

    Type = Model.Attribute()

    TimepointTarget = Model.Attribute()

    TimepointPreWindow = Model.Attribute()

    TimepointPostWindow = Model.Attribute()

    Description = Model.OneElement()


class AbsoluteTimingConstraint(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/AbsoluteTimingConstraint
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    StudyEventGroupOID = Model.Attribute()

    StudyEventOID = Model.Attribute()

    TimepointTarget = Model.Attribute()

    TimepointPreWindow = Model.Attribute()

    TimepointPostWindow = Model.Attribute()

    Description = Model.OneElement()


class RelativeTimingConstraint(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/RelativeTimingConstraint
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    PredecessorOID = Model.Attribute()

    SuccessorOID = Model.Attribute()

    Type = Model.Attribute()

    TimepointRelativeTarget = Model.Attribute()

    TimepointPreWindow = Model.Attribute()

    TimepointPostWindow = Model.Attribute()

    Description = Model.OneElement()


class DurationTimingConstraint(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/DurationTimingConstraint
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    StructuralElementOID = Model.Attribute()

    DurationTarget = Model.Attribute()

    DurationPreWindow = Model.Attribute()

    DurationPostWindow = Model.Attribute()

    Description = Model.OneElement()


class WorkflowDef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowDef
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Description = Model.OneElement()

    WorkflowStart = Model.OneElement()

    WorkflowEnd = Model.ManyElements()

    Transition = Model.OneElement()

    Branching = Model.OneElement()


class WorkflowStart(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowStart
    """

    StartOID = Model.Attribute()


class Transition(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Transition
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    SourceOID = Model.Attribute()

    TargetOID = Model.Attribute()

    StartConditionOID = Model.Attribute()

    EndConditionOID = Model.Attribute()


class Branching(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Branching
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    Type = Model.Attribute()

    TargetTransition = Model.ManyElements()

    DefaultTransition = Model.ManyElements()


class TargetTransition(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/TargetTransition
    """

    TargetTransitionOID = Model.Attribute()

    ConditionOID = Model.Attribute()


class DefaultTransition(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/DefaultTransition
    """

    TargetTransitionOID = Model.Attribute()


class WorkflowEnd(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowEnd
    """

    EndOID = Model.Attribute()


class Criterion(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Criterion
    """

    OID = Model.Attribute()

    Name = Model.Attribute()

    ConditionOID = Model.Attribute()

    Description = Model.OneElement()

    Coding = Model.ManyElements()


class Specification:
    """
    定义 CDISC ODM V2 的节点，该文件属于结构的声明文件，真实实现在 cdisc 中
    """
    Association: Association
    KeySet: KeySet
    Annotation: Annotation
    Comment: Comment
    Flag: Flag
    FlagValue: FlagValue
    FlagType: FlagType
    Coding: Coding
    Query: Query
    Value: Value
    User: User
    UserName: UserName
    Prefix: Prefix
    Suffix: Suffix
    FullName: FullName
    GivenName: GivenName
    FamilyName: FamilyName
    Image: Image
    Organization: Organization
    Location: Location
    Address: Address
    Telecom: Telecom
    StreetName: StreetName
    HouseNumber: HouseNumber
    City: City
    StateProv: StateProv
    Country: Country
    PostalCode: PostalCode
    GeoPosition: GeoPosition
    OtherText: OtherText
    MetaDataVersionRef: MetaDataVersionRef
    SignatureDef: SignatureDef
    Meaning: Meaning
    LegalReason: LegalReason
    ClinicalData: ClinicalData
    SubjectData: SubjectData
    SiteRef: SiteRef
    InvestigatorRef: InvestigatorRef
    StudyEventData: StudyEventData
    ItemGroupData: ItemGroupData
    ItemData: ItemData
    AuditRecord: AuditRecord
    UserRef: UserRef
    LocationRef: LocationRef
    DateTimeStamp: DateTimeStamp
    ReasonForChange: ReasonForChange
    SourceID: SourceID
    Signature: Signature
    SignatureRef: SignatureRef
    FormalExpression: FormalExpression
    Code: Code
    ExternalCodeLib: ExternalCodeLib
    CommentDef: CommentDef
    StudyStructure: StudyStructure
    TrialPhase: TrialPhase
    StudyIndications: StudyIndications
    StudyIndication: StudyIndication
    StudyInterventions: StudyInterventions
    StudyIntervention: StudyIntervention
    StudyObjectives: StudyObjectives
    StudyObjective: StudyObjective
    StudyEndPointRef: StudyEndPointRef
    StudyEndPoints: StudyEndPoints
    StudyEndPoint: StudyEndPoint
    StudyTargetPopulation: StudyTargetPopulation
    StudyEstimands: StudyEstimands
    StudyEstimand: StudyEstimand
    InclusionExclusionCriteria: InclusionExclusionCriteria
    InclusionCriteria: InclusionCriteria
    ExclusionCriteria: ExclusionCriteria
    StudyTargetPopulationRef: StudyTargetPopulationRef
    StudyInterventionRef: StudyInterventionRef
    IntercurrentEvent: IntercurrentEvent
    SummaryMeasure: SummaryMeasure
    Arm: Arm
    Epoch: Epoch
    WorkflowRef: WorkflowRef
    StudySummary: StudySummary
    StudyParameter: StudyParameter
    ParameterValue: ParameterValue
    StudyTimings: StudyTimings
    StudyTiming: StudyTiming
    TransitionTimingConstraint: TransitionTimingConstraint
    AbsoluteTimingConstraint: AbsoluteTimingConstraint
    RelativeTimingConstraint: RelativeTimingConstraint
    DurationTimingConstraint: DurationTimingConstraint
    WorkflowDef: WorkflowDef
    WorkflowStart: WorkflowStart
    Transition: Transition
    Branching: Branching
    TargetTransition: TargetTransition
    DefaultTransition: DefaultTransition
    WorkflowEnd: WorkflowEnd
    Criterion: Criterion

    def first(self): return self

    def find(self): return self

    def index(self, i): return self
