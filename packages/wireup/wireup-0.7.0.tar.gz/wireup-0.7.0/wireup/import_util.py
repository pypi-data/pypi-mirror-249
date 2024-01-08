from __future__ import annotations

import fnmatch
import pkgutil
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Generator
    from types import ModuleType

    from wireup import DependencyContainer


__T = TypeVar("__T")


def warmup_container(dependency_container: DependencyContainer, service_modules: list[ModuleType]) -> None:
    """Import all modules provided in `service_modules` and initializes all registered singleton services.

    !!! note
        For long-lived processes this should be executed once at startup.
    """
    for module in service_modules:
        for _ in _find_classes_in_module(module):
            pass

    dependency_container.warmup()


def _find_classes_in_module(module: ModuleType, pattern: str = "*") -> Generator[type[__T], None, None]:
    """Return a list of object types found in a given module that matches the pattern in the argument.

    :param module: The module under which to recursively look for types.
    :param pattern: A fnmatch pattern which the type name will be tested against.
    """
    for _, modname, __ in pkgutil.walk_packages(module.__path__, prefix=module.__name__ + "."):
        mod = __import__(modname, fromlist="dummy")

        for name in dir(mod):
            obj = getattr(mod, name)

            if isinstance(obj, type) and obj.__module__ == mod.__name__ and fnmatch.fnmatch(obj.__name__, pattern):
                yield obj


def register_all_in_module(container: DependencyContainer, module: ModuleType, pattern: str = "*") -> None:
    """Register all modules inside a given module.

    Useful when your services reside in one place, and you'd like to avoid having to `@container.register` each of them.
    Alternatively this can be used if you want to use the library without having to rely on decorators.

    See Also: `DependencyContainer.context` to manually wire dependencies without having to use annotations.

    :param container: Dependency container to register services in.
    :param module: The package name to recursively search for classes.
    :param pattern: A pattern that will be fed to fnmatch to determine if a class will be registered or not.
    """
    klass: type[Any]
    for klass in _find_classes_in_module(module, pattern):
        container.register(klass)
