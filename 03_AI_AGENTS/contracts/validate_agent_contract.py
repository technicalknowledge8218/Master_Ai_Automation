"""
validate_agent_contract.py
MASTER-AI Agent Contract & Response Validation Engine

Validates agent tasks, requests, responses, and artifact handoffs against
MASTER-AI schemas without requiring third-party dependencies.
"""

import sys
import os
import json
import re
from typing import Dict, Any, List, Tuple

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas")


def load_schema(schema_name: str) -> Dict[str, Any]:
    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema not found at {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_dict_schema(data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
    """Recursively validates a dict against JSON schema rules (type, required, enum, pattern, items)."""
    errors: List[str] = []

    expected_type = schema.get("type")
    if expected_type:
        type_map = {
            "object": dict,
            "array": list,
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool
        }
        py_type = type_map.get(expected_type)
        if py_type and not isinstance(data, py_type):
            errors.append(f"{path}: expected type '{expected_type}', got '{type(data).__name__}'")
            return errors

    if isinstance(data, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                errors.append(f"{path}: missing required property '{field}'")

        properties = schema.get("properties", {})
        additional_properties = schema.get("additionalProperties", True)

        for key, value in data.items():
            if key in properties:
                prop_schema = properties[key]
                sub_errors = validate_dict_schema(value, prop_schema, path=f"{path}.{key}")
                errors.extend(sub_errors)
            elif additional_properties is False:
                errors.append(f"{path}: unexpected property '{key}' (additionalProperties is false)")

    elif isinstance(data, list):
        items_schema = schema.get("items")
        min_items = schema.get("minItems")
        if min_items is not None and len(data) < min_items:
            errors.append(f"{path}: expected at least {min_items} items, got {len(data)}")

        if items_schema:
            for idx, item in enumerate(data):
                sub_errors = validate_dict_schema(item, items_schema, path=f"{path}[{idx}]")
                errors.extend(sub_errors)

    elif isinstance(data, str):
        enum_vals = schema.get("enum")
        if enum_vals is not None and data not in enum_vals:
            errors.append(f"{path}: value '{data}' not in allowed enum {enum_vals}")

        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, data):
            errors.append(f"{path}: value '{data}' does not match pattern '{pattern}'")

        min_len = schema.get("minLength")
        if min_len is not None and len(data) < min_len:
            errors.append(f"{path}: length {len(data)} is less than minimum {min_len}")

    return errors


def validate_agent_response(response_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates an agent response payload."""
    schema = load_schema("agent_response_schema.json")
    errors = validate_dict_schema(response_data, schema)
    return len(errors) == 0, errors


def validate_agent_request(request_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates an agent request payload."""
    schema = load_schema("agent_request_schema.json")
    errors = validate_dict_schema(request_data, schema)
    return len(errors) == 0, errors


def validate_task(task_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates a task payload."""
    schema = load_schema("task_schema.json")
    errors = validate_dict_schema(task_data, schema)
    return len(errors) == 0, errors


def validate_artifact_handoff(handoff_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates an artifact handoff payload."""
    schema = load_schema("artifact_handoff_schema.json")
    errors = validate_dict_schema(handoff_data, schema)
    return len(errors) == 0, errors


def validate_failure_report(failure_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates a failure report payload."""
    schema = load_schema("failure_report_schema.json")
    errors = validate_dict_schema(failure_data, schema)
    return len(errors) == 0, errors


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_agent_contract.py <response|request|task|handoff|failure> <file_path>")
        sys.exit(1)

    contract_type = sys.argv[1].lower()
    file_path = sys.argv[2]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    validators = {
        "response": validate_agent_response,
        "request": validate_agent_request,
        "task": validate_task,
        "handoff": validate_artifact_handoff,
        "failure": validate_failure_report
    }

    validator = validators.get(contract_type)
    if not validator:
        print(f"Unknown contract type '{contract_type}'. Choose from {list(validators.keys())}")
        sys.exit(1)

    passed, errors = validator(data)
    if passed:
        print(f"VALIDATION_PASSED: {contract_type.upper()} conforms to schema.")
        sys.exit(0)
    else:
        print(f"VALIDATION_FAILED: {len(errors)} error(s) found:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
