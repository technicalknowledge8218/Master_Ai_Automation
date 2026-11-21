#!/usr/bin/env python3
"""
validate_design_system.py - Master AI Universal Design System & Token Validator
Validates DESIGN_TOKENS.json, DESIGN_SYSTEM_REGISTRY.json, and UNIVERSAL_DESIGN_SYSTEM.md.
"""

import os
import sys
import json
from pathlib import Path

def validate_design_system():
    workspace_root = Path(__file__).resolve().parent.parent.parent
    tokens_path = workspace_root / "06_UI_UX_DESIGN" / "tokens" / "DESIGN_TOKENS.json"
    registry_path = workspace_root / "06_UI_UX_DESIGN" / "design_systems" / "DESIGN_SYSTEM_REGISTRY.json"
    spec_path = workspace_root / "06_UI_UX_DESIGN" / "design_systems" / "UNIVERSAL_DESIGN_SYSTEM.md"

    errors = []
    print(f"[+] Validating Design System in: {workspace_root / '06_UI_UX_DESIGN'}")

    # 1. Validate Tokens
    if not tokens_path.exists():
        errors.append(f"Missing tokens file: {tokens_path}")
    else:
        try:
            with open(tokens_path, "r", encoding="utf-8") as f:
                tokens_data = json.load(f)
            tokens_dict = tokens_data.get("tokens", {})
            required_sections = ["colors", "typography", "spacing", "breakpoints", "radii", "shadows", "motion", "z_indices"]
            for s in required_sections:
                if s not in tokens_dict:
                    errors.append(f"Tokens missing required section: '{s}'")
            print(f"  [✓] DESIGN_TOKENS.json valid ({len(tokens_dict)} token categories)")
        except Exception as e:
            errors.append(f"Invalid DESIGN_TOKENS.json: {e}")

    # 2. Validate Component Registry
    if not registry_path.exists():
        errors.append(f"Missing registry file: {registry_path}")
    else:
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                reg_data = json.load(f)
            components = reg_data.get("components", [])
            if len(components) < 5:
                errors.append(f"Expected at least 5 components in registry, got {len(components)}")
            for comp in components:
                for req_key in ["id", "name", "category", "variants", "states"]:
                    if req_key not in comp:
                        errors.append(f"Component {comp.get('id', 'unknown')} missing key '{req_key}'")
            print(f"  [✓] DESIGN_SYSTEM_REGISTRY.json valid ({len(components)} components registered)")
        except Exception as e:
            errors.append(f"Invalid DESIGN_SYSTEM_REGISTRY.json: {e}")

    # 3. Validate Markdown Spec
    if not spec_path.exists():
        errors.append(f"Missing markdown specification: {spec_path}")
    else:
        content = spec_path.read_text(encoding="utf-8")
        required_terms = ["WCAG 2.2 AAA", "DESIGN_TOKENS.json", "Button", "Input", "Modal", "aria-"]
        for term in required_terms:
            if term not in content:
                errors.append(f"Specification missing required term: '{term}'")
        print(f"  [✓] UNIVERSAL_DESIGN_SYSTEM.md valid ({len(content.splitlines())} lines)")

    if errors:
        print("[!] Validation FAILED with errors:")
        for err in errors:
            print(f"    - {err}")
        return False

    print("[✓] ALL DESIGN SYSTEM ASSETS PASSED VALIDATION.")
    return True

if __name__ == "__main__":
    success = validate_design_system()
    sys.exit(0 if success else 1)
