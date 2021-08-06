import importlib
import inspect
import logging

from Core.shared.utils import ErrorCodes


def _get_storage_connector(storage_config: dict):
    path_split = storage_config.get("connector").split(".")
    path = ".".join(path_split[:-1])
    module = importlib.import_module(path)
    return getattr(module, path_split[-1])


def _get_repository(repository_item):
    repository_name, repository_path = repository_item
    path_split = repository_path.split(".")
    path = ".".join(path_split[:-1])
    module = importlib.import_module(path)
    return repository_name, getattr(module, path_split[-1])


def _prepare_storages(config_manager):
    """ Prepares the repositories and connects them to the database by using Connector classes """
    declared_storages = config_manager.get_field("storage")
    storages = {}
    for storage_name, storage_config in declared_storages.items():
        connector = _get_storage_connector(storage_config)
        connection = connector(
            connection_details=storage_config.get("connection_details")
        ).connect()
        for repository_item in storage_config.get("repositories").items():
            repository_name, repository_class = _get_repository(repository_item)
            repository_class = repository_class(session=connection)
            storages[repository_name] = {"class": repository_class}

    return storages


def _prepare_dependencies(storages, additional_dep, cog):
    """populates deps dict containing all of the needed dependencies by cog"""
    deps = {}
    argspec = inspect.getfullargspec(cog.setup)
    for key in argspec[0]:
        if key in storages.keys():
            deps[key] = storages[key]["class"]
        elif key in additional_dep.keys():
            deps[key] = additional_dep[key]
        else:
            print(f"Could not find anything for {key}")
    return deps


def _collect_dependencies(config_manager):
    """loads the dependencies listed in configuration file"""
    dependencies = config_manager.get_field("dependencies")
    additional_dep = {}

    for dependency in dependencies:
        imported_dependency = importlib.import_module(dependencies[dependency])
        # the thing that importlib imports is a module, so we have to somehow initialize it, the best way is by a
        # global setup function. If the module has no such function, then it's not supposed to be auto-imported
        try:
            additional_dep[dependency] = imported_dependency.setup()
        except AttributeError:
            print(
                ErrorCodes.bcolors.WARNING
                + f"WARNING: dependency {imported_dependency} has no setup function and thus can not be added automatically"
                + ErrorCodes.bcolors.ENDC
            )

    return additional_dep


def _setup_logger_handler(logger, handler) -> logging.Logger:
    """prepares logger to let others log their info"""

    logger.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    return logger
