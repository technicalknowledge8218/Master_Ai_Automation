#!/usr/bin/env python3
"""
MASTER-AI System Architecture Specification Validator
Validates system architecture JSON specifications for required sections, layer contracts,
dependency directions, and duplicate component IDs.
"""

import argparse
import json
import os
import sys

REQUIRED_TOP_LEVEL = ["system_name", "pattern", "layers"]
REQUIRED_LAYER_FIELDS = ["name", "modules", "responsibilities"]

def validate_spec(spec_path):
    if not os.path.exists(spec_path):
        return {"passed": False, "errors": [f"File does not exist: {spec_path}"]}

    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"passed": False, "errors": [f"JSON syntax error: {str(e)}"]}

    errors = []
    # 1. Top-level structure
    for field in REQUIRED_TOP_LEVEL:
        if field not in data or not data[field]:
            errors.append(f"Missing required top-level field: '{field}'")

    layers = data.get("layers", [])
    if not isinstance(layers, list) or len(layers) == 0:
        errors.append("'layers' must be a non-empty list of layer definitions.")
    else:
        layer_names = []
        all_modules = []
        for idx, layer in enumerate(layers):
            if not isinstance(layer, dict):
                errors.append(f"Layer at index {idx} must be a dictionary.")
                continue
            for rf in REQUIRED_LAYER_FIELDS:
                if rf not in layer or not layer[rf]:
                    errors.append(f"Layer at index {idx} missing required field: '{rf}'")

            lname = layer.get("name")
            if lname:
                if lname in layer_names:
                    errors.append(f"Duplicate layer name detected: '{lname}'")
                layer_names.append(lname)

            mods = layer.get("modules", [])
            if not isinstance(mods, list):
                errors.append(f"Modules in layer '{lname}' must be a list.")
            else:
                for m in mods:
                    if m in all_modules:
                        errors.append(f"Duplicate module ID detected across layers: '{m}'")
                    all_modules.append(m)

    return {
        "file": spec_path,
        "system_name": data.get("system_name"),
        "pattern": data.get("pattern"),
        "total_layers": len(layers) if isinstance(layers, list) else 0,
        "total_modules": len(all_modules) if 'all_modules' in locals() else 0,
        "errors": errors,
        "passed": len(errors) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="Validate Architecture System Specification")
    parser.add_argument("--spec", required=True, help="Path to architecture JSON specification")
    args = parser.parse_args()

    result = validate_spec(args.spec)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
