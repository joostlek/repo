"""Validation script for Home Assistant manifest files."""
import json
import sys
from pathlib import Path


def validate_manifest(manifest_path: Path) -> tuple[bool, str]:
    """Validate a manifest.json file.
    
    Args:
        manifest_path: Path to the manifest.json file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(manifest_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Required fields
    required_fields = ["domain", "name", "documentation", "requirements"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate integration_type if present
    if "integration_type" in data:
        valid_types = ["device", "service", "hub"]
        if data["integration_type"] not in valid_types:
            return False, f"Invalid integration_type: {data['integration_type']}. Must be one of {valid_types}"
    
    # Check if config_flow requires integration_type
    if data.get("config_flow") is True and "integration_type" not in data:
        return False, "Manifest with config_flow: true must have integration_type"
    
    # Validate JSON structure (keys should be sorted except domain and name)
    keys = list(data.keys())
    # Extract domain and name if they exist
    special_keys = []
    other_keys = []
    for key in keys:
        if key in ["domain", "name"]:
            special_keys.append(key)
        else:
            other_keys.append(key)
    
    # Check if other keys are sorted
    sorted_other_keys = sorted(other_keys)
    if other_keys != sorted_other_keys:
        return False, f"Keys must be in alphabetical order (except domain and name). Expected: {special_keys + sorted_other_keys}"
    
    return True, "Validation successful"


def main():
    """Main validation function."""
    # Find all manifest.json files
    repo_root = Path(__file__).parent.parent
    manifests = list(repo_root.glob("integrations/*/manifest.json"))
    
    if not manifests:
        print("No manifest files found")
        return 0
    
    print(f"Validating {len(manifests)} manifest files...")
    errors = []
    
    for manifest_path in manifests:
        is_valid, message = validate_manifest(manifest_path)
        if not is_valid:
            errors.append(f"{manifest_path.parent.name}: {message}")
            print(f"❌ {manifest_path.parent.name}: {message}")
        else:
            print(f"✓ {manifest_path.parent.name}: {message}")
    
    if errors:
        print(f"\n{len(errors)} validation error(s) found")
        return 1
    
    print(f"\n✓ All {len(manifests)} manifests are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
