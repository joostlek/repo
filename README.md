# Manifest Integration Type Management Tool

This repository contains a tool to manage `integration_type` fields in `manifest.json` files for integrations with `config_flow` enabled.

## Overview

The tool helps users review and update manifest.json files by:
- Finding all integrations with `config_flow: true` that are missing `integration_type`
- Prompting users to select the appropriate type (device, service, or hub)
- Updating manifests with proper JSON formatting and alphabetical ordering
- Validating changes with the hassfest validation script
- Creating individual git commits for each updated integration

## Requirements

- Python 3.7+
- Git

## Usage

### Running the Tool

```bash
python3 manage_integration_type.py
```

The tool will:
1. Scan the `integrations/` directory for manifest.json files
2. Identify manifests with `config_flow: true` but missing `integration_type`
3. Prompt you for each integration:
   ```
   Select the `integration_type` for `integration_name`
     1. device
     2. service
     3. hub
     0. skip
   >
   ```
4. Update the manifest with the selected type
5. Validate the changes
6. Commit each change individually

### Input Options

You can use either:
- **Numbers**: `1` (device), `2` (service), `3` (hub), `0` (skip)
- **Text**: `device`, `service`, `hub`, `skip`

### Integration Types

- **device**: For integrations that represent physical or virtual devices
- **service**: For integrations that provide services
- **hub**: For integrations that act as hubs or bridges to other devices

### Validation

The tool includes a validation script that checks:
- JSON syntax validity
- Required fields (domain, name, documentation, requirements)
- integration_type values (must be device, service, or hub)
- Alphabetical ordering of keys (except domain and name)

Run validation manually:
```bash
python3 -m script
```

## Project Structure

```
.
├── manage_integration_type.py    # Main interactive tool
├── script/
│   ├── __init__.py
│   └── __main__.py               # Validation script (hassfest)
├── integrations/                 # Integration folders
│   ├── sample_device/
│   │   └── manifest.json
│   ├── sample_service/
│   │   └── manifest.json
│   └── sample_hub/
│       └── manifest.json
└── README.md
```

## Example Workflow

```bash
$ python3 manage_integration_type.py
======================================================================
Manifest Integration Type Management Tool
======================================================================

Found 3 manifest(s) that need integration_type added:
  - sample_device
  - sample_service
  - sample_hub

----------------------------------------------------------------------

Select the `integration_type` for `sample_device`
  1. device
  2. service
  3. hub
  0. skip
> 1
Setting integration_type to 'device' for sample_device
✓ Updated /path/to/integrations/sample_device/manifest.json
✓ Validation passed
✓ Committed changes for sample_device

----------------------------------------------------------------------
...

======================================================================
Summary:
  Updated: 3
  Skipped: 0
  Failed:  0
======================================================================

Running full validation with python3 -m script.hassfest...

Validating 4 manifest files...
✓ sample_device: Validation successful
✓ sample_service: Validation successful
✓ sample_hub: Validation successful
✓ no_config_flow: Validation successful

✓ All 4 manifests are valid
```

## Manifest Format

After updating, manifests will have the `integration_type` field inserted in alphabetical order (ignoring `domain` and `name` which stay at the top):

```json
{
  "domain": "sample_device",
  "name": "Sample Device",
  "codeowners": ["@joostlek"],
  "config_flow": true,
  "documentation": "https://example.com/sample_device",
  "integration_type": "device",
  "iot_class": "local_polling",
  "requirements": ["requests==2.28.0"],
  "version": "1.0.0"
}
```
