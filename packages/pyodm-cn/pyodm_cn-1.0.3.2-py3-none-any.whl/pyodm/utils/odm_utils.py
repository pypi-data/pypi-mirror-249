from pyodm.model.definition.cdisc_model import CdiscModel
from pyodm.model.meta.cdisc_odm_entity import CdiscODMEntity
from pyodm.model.definition import Attribute, OneElement, ManyElements
from pyodm.utils.class_utils import ClassUtils


class OdmUtils:
    @staticmethod
    def append(target, odm_element):
        target.array.append(odm_element)
        return target

    @staticmethod
    def merge(base, merged_entity):

        for x_name, x_element in vars(base).items():

            entity_element = ClassUtils.get(merged_entity, x_name)
            if x_name == '_value' and entity_element is not None:
                base.set_value(ClassUtils.get(merged_entity, x_name))

            if not OdmUtils.is_cdisc_model(entity_element): continue
            if entity_element is None: continue
            # if entity_element is None or entity_element.no_use(): continue
            if OdmUtils.is_attribute(x_element) and OdmUtils.is_attribute(entity_element):
                if not entity_element.no_use() and x_element.no_use():
                    x_element.set_value(entity_element.get_value())
                    x_element.set_name(x_name)
            elif OdmUtils.is_one_element(x_element):
                #  如果是 OneElement 的话，则表示该Element 并末使用，跳过该Element
                entity_element = ClassUtils.get(merged_entity, x_name)
                if entity_element is not None and not OdmUtils.is_one_element(entity_element):
                    setattr(base, x_name, entity_element)

            elif OdmUtils.is_many_elements(x_element) and OdmUtils.is_many_elements(entity_element):
                if not x_element.no_use():
                    length = len(x_element.array)
                    for e in entity_element.array:
                        is_like = False
                        for i in range(length):
                            if OdmUtils.like(x_element.array[i], e):
                                OdmUtils.merge(x_element.array[i], e)
                                is_like = True
                                continue
                        if not is_like:
                            OdmUtils.append(x_element, e)
                else:
                    for e in entity_element.array:
                        OdmUtils.append(x_element, e)
                    x_element.set_name(x_name)

            elif OdmUtils.is_entity(x_element) and OdmUtils.is_entity(entity_element):
                # 实例化了 ODM 对象
                if x_element.get_value() != entity_element.get_value():
                    x_element.set_value(entity_element.get_value())
                OdmUtils.merge(x_element, entity_element)
        return base

    @staticmethod
    def like(target, odm_element):
        """
        判断 odm_element 与 target 是否属性相似
        target的属性为 odm_element 的子集　或 odm_element 的属性为 target子集 返回　True, 否则 False
        举例
        target 属性 A B, odm_element 属性 A B 返回 True
        target 属性 A B, odm_element 属性 A B C D 返回 True
        target 属性 A D, odm_element 属性 A B 返回 False
        target 属性 A,B, odm_element 属性 A 返回 True

        :param target:
        :type target:
        :param odm_element:
        :type odm_element:
        :return:
        :rtype:
        """
        target_attributes = list(filter(lambda e: OdmUtils.is_attribute(e) and not e.no_use(), vars(target).values()))
        odm_attributes = list(filter(lambda e: OdmUtils.is_attribute(e) and not e.no_use(), vars(odm_element).values()))
        # 如果 Element 都 没有属性
        if not target_attributes and not odm_attributes: return True
        if not target_attributes: return False
        for attribute in target_attributes:
            if OdmUtils.useless(odm_element, attribute.get_name()): continue
            if attribute.get_value() != odm_element.__dict__.get(attribute.get_name()).get_value():
                return False
        return True

    @staticmethod
    def is_attribute(element):
        return isinstance(element, Attribute)

    @staticmethod
    def is_one_element(element):
        return isinstance(element, OneElement)

    @staticmethod
    def is_many_elements(element):
        return isinstance(element, ManyElements)

    @staticmethod
    def is_entity(element):
        return isinstance(element, CdiscODMEntity)

    @staticmethod
    def is_cdisc_model(element):
        return isinstance(element, CdiscModel) or OdmUtils.is_entity(element)

    @staticmethod
    def useless(element, sub_name):
        """
        判断 sub_name 在 element中是否存在，或没有使用
        :param element:
        :type element:
        :param sub_name:
        :type sub_name:
        :return:
        :rtype:
        """
        return element.__dict__.get(sub_name) is None or element.__dict__.get(sub_name).no_use()

    @staticmethod
    def add(base, element_entity):
        setattr(base, element_entity.get_name(), element_entity)
