from pathlib import Path
from typing import List
from akerbp.mlops.core.config import client_secrets as secrets
from akerbp.mlops.cdf.helpers import get_client
from akerbp.mlops.core.config import read_project_settings
from akerbp.mlops.core.helpers import input_data_validation, response_validation

required_input = ["WELL", "DEN", "AC", "NEU", "PEF"]

client = get_client(
    client_id=secrets["id-read"],
    client_secret=secrets["secret-read"],
    tenant_id=secrets["tenant-id"],
    base_url=secrets["base-url"],
)

client_write = get_client(
    client_id=secrets["id-write"],
    client_secret=secrets["secret-write"],
    tenant_id=secrets["tenant-id"],
    base_url=secrets["base-url"],
)


def test_input_data_validation_correct_input_logs_return_true(
    required_input: List = required_input,
):
    input_with_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_logs,
    )
    assert validated


def test_input_data_validation_correct_input_logs_not_standard_return_true(
    required_input: List = required_input,
):
    input_with_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "WELL": [],
                    "RHOB": [],
                    "DTC": [],
                    "NPHI": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_logs,
    )
    assert validated


def test_input_data_validation_correct_input_logs_multiple_wells_return_true(
    required_input: List = required_input,
):
    input_with_multiple_logs = {
        "input": [
            {
                "well": "well1",
                "input_logs": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well2",
                "input_logs": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_multiple_logs,
    )
    assert validated


def test_input_data_validation_wrong_logs_return_false(
    required_input: List = required_input,
):
    input_with_wrong_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "WELL": [],
                    "ACS": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_wrong_logs,
    )
    assert not validated


def test_input_data_validation_wrong_logs_multiple_wells_return_false(
    required_input: List = required_input,
):
    input_with_wrong_logs_multiple_wells = {
        "input": [
            {
                "well": "well1",
                "input_logs": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well2",
                "input_logs": {
                    "WELL": [],
                    "ACS": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_wrong_logs_multiple_wells,
    )
    assert not validated


def test_input_data_validation_wrongly_specified_input_logs_return_false(
    required_input: List = required_input,
):
    input_wrongly_specified_input_logs = {
        "input": [
            {
                "well": "well-123",
                "required_input": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_wrongly_specified_input_logs,
    )
    assert not validated


def test_input_data_validation_wrongly_specified_input_logs_multiple_wells_return_false(
    required_input: List = required_input,
):
    input_wrongly_specidied_input_logs_multiple_wells = {
        "input": [
            {
                "well": "well-1",
                "input_curves": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well-2",
                "required_input_curves": {
                    "WELL": [],
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_wrongly_specidied_input_logs_multiple_wells,
    )
    assert not validated


def test_input_data_validation_with_well_and_kwargs_only_return_true(
    required_input: List = required_input,
):
    input_with_well_and_kwargs_only = {
        "input": [{"well": "well-123", "keyword_arguments": {}}]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_well_and_kwargs_only,
    )
    assert validated


def test_input_data_validation_with_well_only_return_true(
    required_input: List = required_input,
):
    input_with_well_only = {"input": [{"well": "well-123"}]}
    validated = input_data_validation(
        required_input=required_input,
        input=input_with_well_only,
    )
    assert validated


def test_input_data_validation_no_required_input_read_from_settings_file_only_well_in_payload(
    yaml_settings=Path("test/test_settings/single_model_no_required_input.yaml"),
):
    input_with_well_only = {"input": [{"well": "well-123"}]}
    no_required_input = []
    project_settings = read_project_settings(yaml_file=yaml_settings)
    for setting in project_settings:
        required_input = eval(setting.info["prediction"]["metadata"]["required_input"])
        validated = input_data_validation(
            required_input=required_input,
            input=input_with_well_only,
        )
        if validated:
            no_required_input.append(True)
        else:
            no_required_input.append(False)
    assert sum(no_required_input) == len(no_required_input)


def test_input_data_validation_no_required_input_read_from_settings_file_logs_in_payload(
    yaml_settings=Path("test/test_settings/single_model_no_required_input.yaml"),
):
    input_with_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "WELL": [],
                    "ACS": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    no_required_input = []
    project_settings = read_project_settings(yaml_file=yaml_settings)
    for setting in project_settings:
        required_input = eval(setting.info["prediction"]["metadata"]["required_input"])
        validated = input_data_validation(
            required_input=required_input,
            input=input_with_logs,
        )
        if validated:
            no_required_input.append(True)
        else:
            no_required_input.append(False)
    assert sum(no_required_input) == len(no_required_input)


def test_input_data_validation_AC_DEN_NEU_required_input_read_from_settings_file_logs_in_payload_returns_true(
    yaml_settings=Path("test/test_settings/single_model_required_input.yaml"),
):
    payload_with_AC_DEN_NEU = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "AC": [],
                    "DEN": [],
                    "NEU": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    required_input_in_payload = []
    project_settings = read_project_settings(yaml_file=yaml_settings)
    for setting in project_settings:
        required_input = eval(setting.info["prediction"]["metadata"]["required_input"])
        validated = input_data_validation(
            required_input=required_input,
            input=payload_with_AC_DEN_NEU,
        )
        if validated:
            required_input_in_payload.append(True)
        else:
            required_input_in_payload.append(False)
    assert sum(required_input_in_payload) == len(required_input_in_payload)


def test_input_data_validation_AC_DEN_NEU_required_input_read_from_settings_file_missing_logs_in_payload_returns_false(
    yaml_settings=Path("test/test_settings/single_model_required_input.yaml"),
):
    payload_with_AC_DEN = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "AC": [],
                    "DEN": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    required_input_in_payload = []
    project_settings = read_project_settings(yaml_file=yaml_settings)
    for setting in project_settings:
        required_input = eval(setting.info["prediction"]["metadata"]["required_input"])
        validated = input_data_validation(
            required_input=required_input,
            input=payload_with_AC_DEN,
        )
        if validated:
            required_input_in_payload.append(True)
        else:
            required_input_in_payload.append(False)
    assert sum(required_input_in_payload) < len(required_input_in_payload)


def test_input_data_validation_AC_DEN_NEU_required_input_read_from_settings_file_additional_logs_in_payload_returns_true(
    yaml_settings=Path("test/test_settings/single_model_required_input.yaml"),
):
    payload_with_additional_curves = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "AC": [],
                    "DEN": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    required_input_in_payload = []
    project_settings = read_project_settings(yaml_file=yaml_settings)
    for setting in project_settings:
        required_input = eval(setting.info["prediction"]["metadata"]["required_input"])
        validated = input_data_validation(
            required_input=required_input,
            input=payload_with_additional_curves,
        )
        if validated:
            required_input_in_payload.append(True)
        else:
            required_input_in_payload.append(False)
    assert sum(required_input_in_payload) == len(required_input_in_payload)


def test_response_validation_return_true_for_correct_structure():
    response_with_correct_curves_and_structure = [
        {
            "DEPTH": [1, 2, 3],
            "well_name": "test",
            "DEN": [0.5, 0.6, 0.7],
            "NEU": [0.8, 0.9, 1.0],
        }
    ]

    assert response_validation(
        response=response_with_correct_curves_and_structure,
    )


def test_response_validation_return_false_for_incorrect_structure():
    response_with_correct_curves_and_incorrect_structure = [
        {
            "DEPTH": [1, 2, 3],
            "WELL": "test",
            "DEN": [0.5, 0.6, 0.7],
            "NEU": [0.8, 0.9, 1.0],
        }
    ]

    assert not response_validation(
        response=response_with_correct_curves_and_incorrect_structure,
    )
