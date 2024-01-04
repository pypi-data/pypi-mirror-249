import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Address(Meta.CdiscODMEntity):
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
