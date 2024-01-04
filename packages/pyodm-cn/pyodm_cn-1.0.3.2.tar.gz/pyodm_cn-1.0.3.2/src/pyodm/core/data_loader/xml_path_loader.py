from pyodm.core.support.abstract_path_loader import AbstractPathDataLoader

from lxml import etree


class XmlPathLoader(AbstractPathDataLoader):
    def load(self):
        return etree.parse(self.file)
