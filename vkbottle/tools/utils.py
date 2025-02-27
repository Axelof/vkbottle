import asyncio
import importlib
import os
import re
from collections.abc import Coroutine, Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, TypeVar

from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle.framework.abc_blueprint import ABCBlueprint

T = TypeVar("T")


# This feature is not used in production
# but can be useful for customization
# purposes
def run_in_task(coroutine: Coroutine[Any, Any, Any]) -> asyncio.Task:
    """Gets loop and runs add makes task from the given coroutine"""

    loop = asyncio.get_running_loop()
    return loop.create_task(coroutine)


def run_sync(coroutine: Coroutine[Any, Any, T]) -> T:
    return ThreadPoolExecutor().submit(asyncio.run, coroutine).result()  # type: ignore


def load_blueprints_from_package(package_name: str) -> Iterator["ABCBlueprint"]:
    """Gets blueprints from package
    >>> for bp in load_blueprints_from_package("blueprints"):
    >>>     bp.load(...)
    """

    logger.warning(
        "Blueprints was deprecated and will be removed in future releases, read about new code separation method in documentation: \n"
        "https://vkbottle.readthedocs.io/ru/latest/tutorial/code-separation/"
    )
    bp_paths = []
    for filename in os.listdir(package_name):
        if filename.startswith("__"):
            continue
        elif not filename.endswith(".py"):
            yield from load_blueprints_from_package(os.path.join(package_name, filename))
            continue

        with open(os.path.join(package_name, filename), encoding="utf-8") as file:
            bp_names = re.findall(
                r"^(\w+) = (?:Bot|User|)Blueprint\(", file.read(), flags=re.MULTILINE
            )

            if len(bp_names) != 1:
                msg = f"Invalid blueprint declaration in file: {filename}"
                raise ValueError(msg)
            bp_paths.append((filename[:-3], bp_names[0]))

    for bp_path in bp_paths:
        module, bp_name = bp_path
        module_name = package_name.replace(f".{os.sep}", ".").replace(os.sep, ".")
        bp_module = importlib.import_module(f"{module_name}.{module}")
        yield getattr(bp_module, bp_name)
