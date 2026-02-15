import importlib
import pkgutil
import inspect
import sys
import os
from typing import Dict, Type, Optional, List
from libs.core_kernel.interfaces.platform import BasePlatformAdapter

class PluginManager:
    """
    Dynamic plugin loader for platform adapters.
    Scans the `plugins/platforms` package and registers any class
    inheriting from BasePlatformAdapter.
    """
    
    _instance = None
    _registry: Dict[str, Type[BasePlatformAdapter]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls) -> "PluginManager":
        if cls._instance is None:
            return cls()
        return cls._instance

    def discover(self, plugins_package: str = "plugins.platforms"):
        """
        Walks through the `plugins.platforms` package and imports all submodules.
        Classes inheriting from BasePlatformAdapter are automatically registered
        via the import process because we inspect the module after import.
        """
        print(f"INFO: Discovering plugins in {plugins_package}")
        
        # Ensure the project root is in sys.path so we can import plugins
        project_root = os.getcwd()
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            package = importlib.import_module(plugins_package)
        except ImportError as e:
            print(f"ERROR: Could not import {plugins_package}: {e}")
            return

        # Iterate over all modules in the plugins package
        if hasattr(package, "__path__"):
             for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if is_pkg:
                    full_name = f"{plugins_package}.{name}.adapter"
                    try:
                        module = importlib.import_module(full_name)
                        self._register_from_module(module)
                    except ImportError as e:
                         # It's okay if a folder doesn't have an adapter.py, just skip
                         print(f"WARN: Could not import adapter from {name}: {e}")
                         pass

    def _register_from_module(self, module):
        """
        Inspects a module for BasePlatformAdapter subclasses and registers them.
        """
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) 
                and issubclass(obj, BasePlatformAdapter) 
                and obj is not BasePlatformAdapter):
                
                platform_name = getattr(obj, "platform_name", None)
                if platform_name:
                    self._registry[platform_name] = obj
                    print(f"INFO: Registered platform adapter: {platform_name} [{name}]")
                else:
                    print(f"WARN: Class {name} has no platform_name, skipping.")

    def get_adapter_class(self, platform_name: str) -> Optional[Type[BasePlatformAdapter]]:
        return self._registry.get(platform_name)

    def list_platforms(self) -> List[str]:
        return list(self._registry.keys())
