# helpers.py
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
from importlib import resources as importlib_resources
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Tuple

import akerbp.mlops as akerbp_mlops
from akerbp.mlops.cdf import helpers as cdf
from akerbp.mlops.core.config import ENV_VARS, ServiceSettings
from akerbp.mlops.core.exceptions import (
    DeploymentError,
    TestError,
    VirtualEnvironmentError,
)
from akerbp.mlops.core.helpers import subprocess_wrapper
from akerbp.mlops.core.logger import get_logger
from akerbp.mlops.deployment import platforms

logger = get_logger(__name__)

envs = ENV_VARS
env = envs.model_env
service_name = envs.service_name
platform_methods = platforms.get_methods()


def is_unix() -> bool:
    """Checks whether the working OS is unix-based or not

    Returns:
        bool: True if os is unix-based
    """
    return os.name == "posix"


def get_repo_origin() -> str:
    """Get origin of the git repo

    Returns:
        (str): origin
    """
    origin = subprocess.check_output(
        ["git", "remote", "get-url", "--push", "origin"], encoding="UTF-8"
    ).rstrip()
    return origin


def replace_string_file(s_old: str, s_new: str, file: Path) -> None:
    """
    Replaces all occurrences of s_old with s_new in a specifyied file

    Args:
        s_old (str): old string
        s_new (str): new string
        file (Path): file to replace the string in
    """
    with file.open("r+") as f:
        data = f.read()
        if s_old not in data:
            logger.warning(f"Didn't find '{s_old}' in {file}")
        data = data.replace(s_old, s_new)
        new = os.linesep.join([s for s in data.splitlines() if s.strip()])
        f.seek(0)
        f.write(new)
        f.truncate()


def set_mlops_import(
    req_file: Path, platform: str, deployment_folder: Optional[str] = None
) -> None:
    """Set correct package version in requirements.txt

    Args:
        req_file (Path): path to requirements.txt for the model to deploy
        deployment_folder (Optional[str], optional): path to a deployment folder. Defaults to None.
            If this is set, the function assumes that the current version of the
            mlops package should be built and the version should be set to a wheel path.
    """
    if deployment_folder is not None:
        package_version = build_mlops_wheel(deployment_folder)
        set_to = f"./{package_version}[{platform}]"
        replace_string_file(
            "akerbp.mlops==MLOPS_VERSION",
            set_to,
            req_file,
        )
        logger.info(
            f"Set akerbp.mlops dependency to {package_version} in requirements.txt"
        )
    else:
        package_version = akerbp_mlops.__version__
        set_to = f"akerbp.mlops[{platform}]=={package_version}"
        replace_string_file(
            "akerbp.mlops==MLOPS_VERSION",
            set_to,
            req_file,
        )
        logger.info(f"Set akerbp.mlops==MLOPS_VERSION to {set_to} in requirements.txt")


def build_mlops_wheel(deployment_folder: str) -> str:
    """Build akerbp.mlops wheel in a virtual environment

    Warning:
        This function assumes that the current version of the mlops package
        is a cloned copy of the mlops repo. It will not work if the package
        is installed from PyPI!

    Args:
        venv_dir (str): path to deployment folder where the wheel should be copied

    Returns:
        str: the wheel's filename.
    """
    # Get root of mlops repo
    root = str(Path(akerbp_mlops.__file__).parents[3])
    # Ensure the root contains pyproject.toml
    if not os.path.isfile(root + "/pyproject.toml"):
        raise DeploymentError("Failed to find pyproject.toml in root")
    # Build wheel
    logger.info("Building akerbp.mlops wheel")
    subprocess_wrapper([sys.executable, "-m", "build"], cwd=root)
    # Search for wheel name
    for file in os.listdir(root + "/dist"):
        if file.endswith(".whl"):
            wheel_name = file
            break
    else:
        # Remove local build artifacts
        logger.info("Removing local build artifacts")
        shutil.rmtree(root + "/dist")
        raise DeploymentError("Failed to build akerbp.mlops wheel")

    # Copy wheel to venv
    source = root + "/dist/" + wheel_name
    logger.info("Copying %s to virtual environment", source)
    shutil.copy(source, deployment_folder)

    # Remove local build artifacts
    logger.info("Removing local build artifacts")
    shutil.rmtree(root + "/dist")

    return str(Path(wheel_name).resolve().name)


def to_folder(path: Path, folder_path: Path) -> None:
    """
    Copy folders, files or package data to a given folder.
    Note that if target exists it will be overwritten.

    Args:
        path: supported formats
            - file/folder path (Path): e,g, Path("my/folder")
            - module file (tuple/list): e.g. ("my.module", "my_file"). Module
            path has to be a string, but file name can be a Path object.
        folder_path (Path): folder to copy to
    """
    if isinstance(path, (tuple, list)):
        module_path, file = path
        file = str(file)
        if importlib_resources.is_resource(module_path, file):
            with importlib_resources.path(module_path, file) as file_path:
                shutil.copy(file_path, folder_path)
        else:
            raise ValueError(f"Didn't find {path[1]} in {path[0]}")
    elif path.is_dir():
        shutil.copytree(
            path,
            folder_path / path,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
        )
    elif path.is_file():
        shutil.copy(path, folder_path)
    else:
        raise ValueError(f"{path} should be a file, folder or package resource")


def get_deployment_folder_content(
    deployment_folder: Path,
) -> Dict:
    """Returns the content of the deployment folder as a dictionary with keys being
    directories/subdirectories, and values the corresponding content.
    If venv_dir is passed as an argument we ignore the content of the corresponding virtual environment

    Args:
        deployment_folder (Path): path to deployment_folderfolder

    Returns:
        Dict: content of deployment folder
    """
    dirwalk = os.walk(deployment_folder)
    content = {}
    for root, dirs, files in dirwalk:
        if "__pycache__" in root.split("/"):
            continue
        if ".pytest_cache" in root.split("/"):
            continue
        dirs = [d for d in dirs if d not in ["__pycache__", ".pytest_cache"]]
        content[root] = files
        if len(dirs) > 0:
            content[root].extend(dirs)
            for subdir in dirs:
                content[os.path.join(root, subdir)] = files
        else:
            content[root] = files
    return content


def copy_to_deployment_folder(lst: Dict, deployment_folder: Path) -> None:
    """
    Copy a list of files/folders to a deployment folder

    Args:
        lst (dict): key is the nickname of the file/folder (used for
        logger) and the value is the path (see `to_folder` for supported
        formats)
        deployment_folder (Path): Path object for the deployment folder

    """
    for k, v in lst.items():
        if v:
            logger.debug(f"{k} => deployment folder")
            to_folder(v, deployment_folder)
        else:
            logger.warning(f"{k} has no value")


def update_pip(venv_dir: str, **kwargs) -> None:
    is_unix_os = kwargs.get("is_unix_os", True)
    setup_venv = kwargs.get("setup_venv", True)
    if setup_venv:
        if is_unix_os:
            sys.executable = os.path.join(venv_dir, "bin", "python")
            c = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
            ]
        else:
            sys.executable = os.path.join(venv_dir, "Scripts", "python")
            c = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
            ]
    else:
        c = ["python", "-m", "pip", "install", "--upgrade", "pip"]
    logger.info("Updating pip")
    subprocess_wrapper(c)


def install_requirements(req_file: str, venv_dir: str, **kwargs) -> None:
    """install model requirements

    Args:
        req_file (str): path to requirements file
    """
    with_deps = kwargs.get("with_deps", True)
    setup_venv = kwargs.get("setup_venv", False)
    is_unix_os = is_unix()
    update_pip(
        venv_dir=venv_dir,
        is_unix_os=is_unix_os,
        setup_venv=setup_venv,
    )
    logger.info(f"Installing python requirement file {req_file}:")
    # Cat file contents to log
    with open(req_file, "r") as f:
        logger.info(f.read())
    if with_deps:
        if setup_venv:
            if is_unix_os:
                sys.executable = os.path.join(venv_dir, "bin", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
            else:
                sys.executable = os.path.join(venv_dir, "Scripts", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
        else:
            c = ["pip", "install", "-r", os.path.abspath(req_file)]
    else:
        if setup_venv:
            if is_unix_os:
                sys.executable = os.path.join(venv_dir, "bin", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "-r",
                    os.path.abspath(req_file),
                ]
            else:
                sys.executable = os.path.join(venv_dir, "Scripts", "python")
                c = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.abspath(req_file),
                ]
        else:
            c = ["pip", "install", "--no-deps", "-r", os.path.abspath(req_file)]
    subprocess_wrapper(c, retry=3)


def create_venv(venv_name: str) -> str:
    venv_dir = os.path.join(os.getcwd(), venv_name)
    logger.info(f"Creating virtual environment {venv_name}")
    venv.create(venv_dir, with_pip=True)
    if os.path.isdir(venv_dir):
        logger.info(f"Successfully created virtual environment {venv_name}")
    else:
        raise VirtualEnvironmentError("Virtual environment was not created")
    return venv_dir


def delete_venv(venv_name: str) -> None:
    logger.info(f"Deleting virtual environment {venv_name}")
    subprocess_wrapper(["rm", "-rf", os.path.abspath(venv_name)])
    if not os.path.isdir(os.path.abspath(venv_name)):
        logger.info(f"Virtual environment {venv_name} sucsessfully deleted")
    else:
        raise VirtualEnvironmentError("Virtual environment not deleted")


def set_up_requirements(c: ServiceSettings, **kwargs) -> str:
    """
    Set up a "requirements.txt" file at the top of the deployment folder
    (assumed to be the current directory), update config and install
    dependencies (unless in dev)

    Args:
        c (ServiceSettings): service settings a specified in the config file

    Keyword Args:
        install (bool): Whether to install the dependencies, defaults to True
    """
    logger.info("Create requirement file")
    install_reqs = kwargs.get("install", True)
    with_deps = kwargs.get("with_deps", True)
    venv_name = kwargs.get("venv_name", "mlops-venv")
    setup_venv = kwargs.get("setup_venv", False)
    unit_testing = kwargs.get("unit_testing", False)
    if setup_venv:
        venv_dir = create_venv(venv_name=venv_name)
    else:
        venv_dir = str(os.getcwd())

    if not unit_testing:
        shutil.copyfile(c.req_file, "requirements.txt")
        c.req_file = Path("requirements.txt").resolve()

    if env != "dev" or install_reqs:
        install_requirements(
            c.req_file, venv_dir=venv_dir, with_deps=with_deps, setup_venv=setup_venv
        )
    else:
        logger.info("Skipping installation of requirements.txt")

    return venv_dir  # type: ignore


def deployment_folder_path(model: str) -> Path:
    """Generate path to deployment folder, which is on the form "mlops_<model>"

    Args:
        model (str): model name

    Returns:
        Path: path to the deployment folder
    """
    return Path(f"mlops_{model}")


def rm_deployment_folder(model: str) -> None:
    logger.info("Deleting deployment folder")
    deployment_folder = deployment_folder_path(model)
    if deployment_folder.exists():
        shutil.rmtree(deployment_folder)


def run_tests(c: ServiceSettings, **kwargs) -> Any:
    """Helper function that runs unit tests and returns a test payload
    if run during deployment

    Args:
        c (ServiceSettings): Service settings object containing model settings

    Keyword Args:
        setup_venv (bool): whether to setup an ephemeral virtual environment.
            Defaults to False
    Raises:
        TestError: If unit tests are failing

    Returns:
        Union[Dict[str, Any], None]: Return test payload if test file is specified in 'mlops_settings.yaml'
    """
    if c.test_file:
        deploy = kwargs.get("deploy", True)
        setup_venv = kwargs.get("setup_venv", False)
        executable = None
        if setup_venv:
            logger.info("Setting up ephemeral virtual environment")
            venv_dir = set_up_requirements(
                c,
                install=True,
                setup_venv=setup_venv,
            )
            if is_unix():
                executable = os.path.join(venv_dir, "bin", "python")
            else:
                executable = os.path.join(venv_dir, "Scripts", "python")
        else:
            set_up_requirements(c, install=True)
        test_command = [
            sys.executable if executable is None else executable,
            "-m",
            "akerbp.mlops.services.test_service",
        ]
        logger.info(f"Running tests for model {c.model_name}")
        failed_test = False
        try:
            output = subprocess.check_output(test_command, encoding="UTF-8")
        except subprocess.CalledProcessError as e:
            output = e.output
            failed_test = True
        model_input = None
        for log_line in output.splitlines():  # type: ignore
            log_line = log_line.strip()
            if log_line == "":
                pass
            elif log_line == "warnings.warn(":
                pass
            elif log_line.startswith('{"input": ['):
                # Extract payload for downstream testing of deployed model
                model_input = json.loads(log_line)
                if deploy:
                    logger.info(
                        "Payload for downstream testing of deployed model obtained"
                    )
            else:
                # Remove the date and time from piped log
                log_line = re.sub(
                    "\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} -",
                    "",
                    log_line,
                )
                logger.info(log_line.strip())
        if failed_test:
            raise TestError("Unit tests failed :( See the above traceback")
        if model_input is None and deploy:
            raise TestError(
                "Test was not able to extract the payload for downstream testing of deployed model"
            )
        logger.info("Unit tests passed :)")
        if setup_venv:
            delete_venv(venv_name=venv_dir.split("/")[-1])
            logger.info("Ephemeral virtual environment deleted")
        return model_input
    else:
        logger.warning(
            "No test file specified in 'mlops_settings.yaml', skipping tests"
        )
        return {}


def do_deploy(
    c: ServiceSettings,
    env: str,
    service_name: str,
    function_name: str,
    deployment_folder: str,
    platform_methods: Dict = platform_methods,
    **kwargs,
) -> None:
    # Run unit tests and get test payload before deploying
    logger.info(
        f"Running tests for model {c.human_friendly_model_name} before deploying to {env}"
    )
    setup_venv = kwargs.pop("setup_venv", False)
    if setup_venv:
        test_payload = run_tests(c, setup_venv=setup_venv)
    else:
        test_payload = run_tests(c, setup_venv=setup_venv)

    # Get content of deployment folder
    deployment_folder_content = get_deployment_folder_content(
        deployment_folder=Path(".")
    )
    logger.info(
        f"Deployment folder '{deployment_folder}' now contains the following: {deployment_folder_content}"
    )
    external_id = function_name
    platform = c.platform
    python_runtime = c.python_version
    deploy_function, _, test_function = platform_methods[platform]
    logger.info(f"Starting deployment of model {c.model_name} to {env}")
    # Get the latest artifact version uploaded to CDF Files and tag the model metadata with this version number
    if platform == "cdf":
        latest_artifact_version = cdf.get_latest_artifact_version(
            external_id=external_id
        )
        if c.artifact_version is None:
            logger.info(
                f"Latest artifact version in {env} is {latest_artifact_version}"
            )
            artifact_version = latest_artifact_version
        else:
            artifact_version = c.artifact_version
    elif platform == "gc":
        pass
    else:
        raise NotImplementedError(
            f"Functionality for deploying models to platform {platform} is not implemented!"
        )

    logger.info(
        f"Deploying function {c.human_friendly_model_name} with external id {external_id} to {platform}"
    )

    # Tag model metadata with version number
    model_info = c.info[service_name]
    model_info["metadata"]["version"] = str(artifact_version)
    try:
        deploy_function(
            c.human_friendly_model_name,
            external_id,
            info=model_info,
            python_runtime=python_runtime,
        )
    except Exception as e:
        raise DeploymentError(f"Deployment failed with message: \n{str(e)}") from e
    if c.test_file:
        logger.info(f"Make a test call to function with external id {external_id}")
        try:
            test_function(external_id, test_payload)
        except Exception as e:
            raise TestError(
                f"Test of deployed model failed with message: \n{str(e)}"
            ) from e
    else:
        logger.warning(
            f"No test file was set up. End-to-end test skipped for function {external_id}"
        )

    if platform == "cdf" and env == "prod":
        # Create a schedule for keeping the latest function warm in prod
        logger.info(
            f"Creating a schedule for keeping the function {external_id} warm on weekdays during extended working hours"
        )
        cdf.setup_schedule_for_latest_model_in_prod(
            external_id=function_name,
        )
        # Redeploy latest function with a predictable external id (model-service-env)
        numbered_external_id = function_name + "-" + str(latest_artifact_version)
        logger.info(
            f"Redeploying numbered model {c.human_friendly_model_name} with external id {external_id} to {platform} in {env}"
        )
        redeploy_model_with_numbered_external_id(
            c,
            numbered_external_id=numbered_external_id,
            test_payload=test_payload,
            info=model_info,
        )

    if platform == "cdf":
        logger.info("Initiating garbage collection of old models in CDF")
        cdf.garbage_collection(
            c,
            function_name,
            env,
            remove_artifacts=c.model_name == "mlopsdemo",
        )


def redeploy_model_with_numbered_external_id(
    c: ServiceSettings,
    numbered_external_id: str,
    test_payload: Any,
    info: Dict[str, Union[str, Dict[str, str]]],
    platform_methods: Dict = platform_methods,
) -> None:
    deploy_function, _, test_function = platform_methods[c.platform]

    try:
        deploy_function(
            c.human_friendly_model_name,
            numbered_external_id,
            info=info,
            python_runtime=c.python_version,
        )

    except Exception as e:
        raise DeploymentError(
            f"Redeployment of numbered model failed with message:  \n{str(e)}"
        ) from e

    if c.test_file:
        try:
            test_function(numbered_external_id, test_payload)
        except Exception as e:
            raise TestError(
                f"Testing the newly redeployed latest model failed with message: \n{str(e)}"
            ) from e
    else:
        logger.warning("No test file was specified in the settings, skipping tests")


def create_temporary_copy(path: Path) -> Path:
    logger.info("Creating a temporary copy of %s", path)
    _, temp_path = tempfile.mkstemp()
    shutil.copy2(path, temp_path)
    return Path(temp_path).resolve()


def requirements_to_dict(path_to_requirements: Path) -> Dict[str, str]:
    """Convert a requirements file to a dictionary

    Args:
        path_to_requirements (Path): path to requirements file

    Returns:
        Dict[str, str]: dictionary with package name as key and version as value
    """
    requirements = {}
    with open(path_to_requirements, "r") as f:
        for line in f.readlines():
            if "==" in line:
                package, version = line.split("==")
                requirements[package] = version.strip()
    return requirements


def check_mismatch_in_model_requirements(
    main_model_requirements: Dict[str, str],
    helper_model_requirements: Dict[str, str],
    packages_to_check: List[str],
) -> Tuple[bool, List[str]]:
    """Check if there is a mismatch between main and helper model requirements for a given list of packages
    Returns True if there is a mismatch in at least one of the listed packages, False otherwise

    Args:
        main_model_requirements (Dict[str, str]): _description_
        helper_model_requirements (Dict[str, str]): _description_

    Returns:
        bool: Whether there is a mismatch between main and helper model requirements
    """
    mismatched_requirements = []
    mismatched_packages = []
    for key in main_model_requirements.keys():
        if key in helper_model_requirements.keys() and key in packages_to_check:
            if main_model_requirements[key] != helper_model_requirements[key]:
                mismatched_requirements.append(True)
                mismatched_packages.append(key)
            else:
                mismatched_requirements.append(False)

    if sum(mismatched_requirements) > 0:
        return True, mismatched_packages
    else:
        return False, []
