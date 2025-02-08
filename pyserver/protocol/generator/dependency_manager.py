from typing import Any, List

try:
    from models import (
        Enumeration,
        Structure,
        Property,
        TypeAlias,
        Request,
        Notification,
        Base,
        Reference,
        Array,
        Tuple,
        Map,
        Literal,
        StringLiteral,
        Or,
        And,
    )
except ImportError:
    from .models import (
        Enumeration,
        Structure,
        Property,
        TypeAlias,
        Request,
        Notification,
        Base,
        Reference,
        Array,
        Tuple,
        Map,
        Literal,
        StringLiteral,
        Or,
        And,
    )


class Manager:
    def __init__(self, elements: Any) -> None:
        self._elements = elements
        self._dependency_map = {}

    def _flatten(self, sequences: List[Any]) -> List[Any]:
        flattened = []
        for item in sequences:
            if isinstance(item, list):
                flattened.extend(self._flatten(item))
            else:
                flattened.append(item)
        return flattened

    def get_dependencies(self) -> List[str]:
        dependencies = [self._get_element_dependency(e) for e in self._elements]

        ordered_dependencies = []
        for dep in self._flatten(dependencies):
            if dep not in ordered_dependencies:
                ordered_dependencies.append(dep)

        return ordered_dependencies

    def get_ordered_elements(self) -> List[Any]:
        elements = []

        for dep in self.get_dependencies():
            for el in self._elements:
                if el.name == dep:
                    elements.append(el)

        return elements

    def _get_element_dependency(self, element: Any) -> List[str]:
        if not element:
            return ""

        func = {
            # class
            Enumeration: self._get_from_enumeration,
            Structure: self._get_from_structure,
            Property: self._get_from_property,
            TypeAlias: self._get_from_typealias,
            Request: self._get_from_request,
            Notification: self._get_from_notification,
            # element
            Base: self._get_from_base,
            Reference: self._get_from_reference,
            Array: self._get_from_array,
            Tuple: self._get_from_tuple,
            Map: self._get_from_map,
            Literal: self._get_from_literal,
            StringLiteral: self._get_from_stringLiteral,
            Or: self._get_from_or,
            And: self._get_from_and,
        }
        try:
            return func[type(element)](element)
        except KeyError as err:
            raise KeyError(f"unable find gererator for {err}") from err

    def _get_from_enumeration(self, element: Enumeration) -> List[str]:
        if deps := self._dependency_map.get(element.name):
            return deps

        deps = self._get_element_dependency(element.type) + [element.name]
        self._dependency_map[element.name] = deps
        return deps

    def _get_from_structure(self, element: Structure) -> List[str]:
        if deps := self._dependency_map.get(element.name):
            return deps

        properties_type = [
            self._get_element_dependency(i) for i in element.properties
        ]
        extends_type = [self._get_element_dependency(i) for i in element.extends]
        mixins_type = [self._get_element_dependency(i) for i in element.mixins]
        deps = properties_type + extends_type + mixins_type + [element.name]
        self._dependency_map[element.name] = deps
        return deps

    def _get_from_property(self, element: Property) -> List[str]:
        return self._get_element_dependency(element.type)

    def _get_from_typealias(self, element: TypeAlias) -> List[str]:
        if deps := self._dependency_map.get(element.name):
            return deps

        deps = self._get_element_dependency(element.type) + [element.name]
        self._dependency_map[element.name] = deps
        return deps

    def _get_from_request(self, element: Request) -> List[str]:
        pass

    def _get_from_notification(self, element: Notification) -> List[str]:
        pass

    def _get_from_base(self, element: Base) -> List[str]:
        return [element.name]

    nesting_reference = set()

    def _get_from_reference(self, element: Reference) -> List[str]:

        if deps := self._dependency_map.get(element.name):
            return deps

        if element.name in self.nesting_reference:
            return []

        reference = None
        for el in self._elements:
            try:
                el_name = el.name
            except AttributeError:
                continue

            if el_name == element.name:
                if isinstance(el, Reference):
                    continue

                reference = el
                break

        deps = []
        if not reference:
            print("reference not found:", element.name)
        else:
            self.nesting_reference.add(element.name)
            deps = self._get_element_dependency(reference)
            self.nesting_reference.remove(element.name)

        self._dependency_map[element.name] = deps
        return deps

    def _get_from_array(self, element: Array) -> List[str]:
        return self._get_element_dependency(element.element)

    def _get_from_tuple(self, element: Tuple) -> List[str]:
        return [self._get_element_dependency(i) for i in element.items]

    def _get_from_map(self, element: Map) -> List[str]:
        key = self._get_element_dependency(element.key)
        value = self._get_element_dependency(element.value)
        return key + value

    def _get_from_literal(self, element: Literal) -> List[str]:
        return []

    def _get_from_stringLiteral(self, element: StringLiteral) -> List[str]:
        return []

    def _get_from_or(self, element: Or) -> List[str]:
        return [self._get_element_dependency(i) for i in element.items]

    def _get_from_and(self, element: Any) -> List[str]:
        return [self._get_element_dependency(i) for i in element.items]
