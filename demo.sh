#!/bin/bash
# Demo script to showcase the manifest integration type management tool

echo "=========================================="
echo "Demo: Manifest Integration Type Tool"
echo "=========================================="
echo ""

echo "Step 1: Check current manifest status"
echo "--------------------------------------"
python3 -m script
echo ""

echo "Step 2: Show integrations needing updates"
echo "--------------------------------------"
# Create a simple script to list manifests needing updates
python3 -c "
from pathlib import Path
import json

repo_root = Path('.')
integrations_dir = repo_root / 'integrations'

manifests_to_update = []
for manifest_path in integrations_dir.glob('*/manifest.json'):
    try:
        with open(manifest_path) as f:
            data = json.load(f)
        if data.get('config_flow') is True and 'integration_type' not in data:
            manifests_to_update.append(manifest_path.parent.name)
    except:
        pass

if manifests_to_update:
    print(f'Found {len(manifests_to_update)} integration(s) needing integration_type:')
    for name in manifests_to_update:
        print(f'  - {name}')
else:
    print('All integrations are up to date!')
"
echo ""

echo "Step 3: Instructions for interactive use"
echo "--------------------------------------"
echo "To update manifests interactively, run:"
echo "  python3 manage_integration_type.py"
echo ""
echo "You will be prompted to select integration_type for each integration:"
echo "  1. device   - Physical or virtual devices"
echo "  2. service  - Service integrations"
echo "  3. hub      - Hub or bridge integrations"
echo "  0. skip     - Skip this integration"
echo ""
echo "You can enter either numbers (1, 2, 3, 0) or text (device, service, hub, skip)"
echo ""

echo "Step 4: Example automated update"
echo "--------------------------------------"
echo "For automated testing, you can pipe input to the script:"
echo "  echo -e '1\\n2\\n3' | python3 manage_integration_type.py"
echo "  # Or use text: echo -e 'device\\nservice\\nhub' | python3 manage_integration_type.py"
echo ""

echo "Demo complete!"
