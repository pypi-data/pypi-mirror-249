import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Association(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Association
    """
    
    StudyOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()

    # 手动修改，因为标准定义了2个相同的子元素
    KeySet = Model.ManyElements()

    Annotation = Model.OneElement()
    
