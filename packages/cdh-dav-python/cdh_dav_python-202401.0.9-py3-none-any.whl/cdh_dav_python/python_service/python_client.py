import importlib
import inspect


class PythonClient:
    @staticmethod
    def list_classes(module_name):
        """
        Lists all classes in a given module.

        :param module_name: Name of the module to inspect.
        """
        try:
            module = importlib.import_module(module_name)
            classes = [
                name for name, obj in inspect.getmembers(module) if inspect.isclass(obj)
            ]
            return classes
        except ImportError:
            return f"Module '{module_name}' not found."

    @staticmethod
    def list_user_defined_classes(module_name):
        """
        Lists user-defined classes in a given module, ignoring special attributes.

        :param module_name: Name of the module to inspect.
        :return: List of user-defined class names.
        """
        try:
            module = importlib.import_module(module_name)
            class_list = []
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and not name.startswith("_"):
                    class_list.append(name)
            return class_list
        except ImportError:
            return f"Module '{module_name}' not found."
