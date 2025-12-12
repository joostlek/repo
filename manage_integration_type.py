#!/usr/bin/env python3
"""Tool to manage integration_type in manifest.json files.

This tool helps users add integration_type to manifest.json files for integrations
that have config_flow enabled.
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


class ManifestManager:
    """Manages manifest.json files for integrations."""
    
    INTEGRATION_TYPES = ["device", "service", "hub"]
    
    def __init__(self, repo_root: Path):
        """Initialize the manifest manager.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        self.integrations_dir = repo_root / "integrations"
    
    def find_manifests_needing_update(self) -> list[Path]:
        """Find all manifest.json files that have config_flow but no integration_type.
        
        Returns:
            List of paths to manifest.json files that need updating
        """
        manifests_to_update = []
        
        if not self.integrations_dir.exists():
            print(f"Error: Integrations directory not found at {self.integrations_dir}")
            return []
        
        for manifest_path in self.integrations_dir.glob("*/manifest.json"):
            try:
                with open(manifest_path) as f:
                    data = json.load(f)
                
                # Check if config_flow is true and integration_type is missing
                if data.get("config_flow") is True and "integration_type" not in data:
                    manifests_to_update.append(manifest_path)
            except Exception as e:
                print(f"Warning: Could not read {manifest_path}: {e}")
        
        return manifests_to_update
    
    def prompt_for_integration_type(self, integration_name: str) -> Optional[str]:
        """Prompt the user to select an integration type.
        
        Args:
            integration_name: Name of the integration
            
        Returns:
            Selected integration type or None if skipped
        """
        print(f"\nSelect the `integration_type` for `{integration_name}`")
        print(f"Options: {', '.join(self.INTEGRATION_TYPES)}")
        print("Enter 'skip' to skip this integration")
        
        while True:
            choice = input("> ").strip().lower()
            
            if choice == "skip":
                return None
            
            if choice in self.INTEGRATION_TYPES:
                return choice
            
            print(f"Invalid choice. Please select one of: {', '.join(self.INTEGRATION_TYPES)}, or 'skip'")
    
    def update_manifest(self, manifest_path: Path, integration_type: str) -> bool:
        """Update a manifest.json file with the integration_type.
        
        The integration_type is inserted in alphabetical order, ignoring domain and name keys.
        
        Args:
            manifest_path: Path to the manifest.json file
            integration_type: Type to add (device, service, or hub)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(manifest_path) as f:
                data = json.load(f)
            
            # Add integration_type
            data["integration_type"] = integration_type
            
            # Sort keys alphabetically, but keep domain and name at the top
            sorted_data = {}
            
            # Add domain and name first if they exist
            if "domain" in data:
                sorted_data["domain"] = data.pop("domain")
            if "name" in data:
                sorted_data["name"] = data.pop("name")
            
            # Add remaining keys in alphabetical order
            for key in sorted(data.keys()):
                sorted_data[key] = data[key]
            
            # Write back to file with proper formatting
            with open(manifest_path, 'w') as f:
                json.dump(sorted_data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            
            return True
        except Exception as e:
            print(f"Error updating {manifest_path}: {e}")
            return False
    
    def validate_manifest(self, manifest_path: Path) -> bool:
        """Validate a manifest file.
        
        Args:
            manifest_path: Path to the manifest.json file
            
        Returns:
            True if validation passed, False otherwise
        """
        try:
            with open(manifest_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON: {e}")
            return False
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return False
        
        # Required fields
        required_fields = ["domain", "name", "documentation", "requirements"]
        for field in required_fields:
            if field not in data:
                print(f"✗ Missing required field: {field}")
                return False
        
        # Validate integration_type if present
        if "integration_type" in data:
            if data["integration_type"] not in self.INTEGRATION_TYPES:
                print(f"✗ Invalid integration_type: {data['integration_type']}")
                return False
        
        # Check if config_flow requires integration_type
        if data.get("config_flow") is True and "integration_type" not in data:
            print("✗ Manifest with config_flow: true must have integration_type")
            return False
        
        print("✓ Validation passed")
        return True
    
    def commit_changes(self, manifest_path: Path, integration_name: str) -> bool:
        """Commit changes to git.
        
        Args:
            manifest_path: Path to the manifest.json file
            integration_name: Name of the integration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Stage the file
            subprocess.run(
                ["git", "add", str(manifest_path)],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            
            # Commit with message
            commit_message = f"Add integration_type to `manifest.json` for {integration_name}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            
            print(f"✓ Committed changes for {integration_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")
            if e.stderr:
                print(e.stderr)
            return False
    
    def run_full_validation(self) -> bool:
        """Run the full hassfest validation on all manifests.
        
        Returns:
            True if validation passed, False otherwise
        """
        try:
            result = subprocess.run(
                [sys.executable, "-m", "script"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error running validation: {e}")
            return False
    
    def run(self):
        """Run the interactive manifest management tool."""
        print("=" * 70)
        print("Manifest Integration Type Management Tool")
        print("=" * 70)
        print()
        
        # Find manifests that need updating
        manifests = self.find_manifests_needing_update()
        
        if not manifests:
            print("No manifests found that need updating.")
            print("All manifests either have integration_type or don't have config_flow enabled.")
            return 0
        
        print(f"Found {len(manifests)} manifest(s) that need integration_type added:")
        for manifest in manifests:
            print(f"  - {manifest.parent.name}")
        print()
        
        # Process each manifest
        updated_count = 0
        skipped_count = 0
        failed_count = 0
        
        for manifest_path in manifests:
            integration_name = manifest_path.parent.name
            print("-" * 70)
            
            # Prompt for integration type
            integration_type = self.prompt_for_integration_type(integration_name)
            
            if integration_type is None:
                print(f"Skipping {integration_name}")
                skipped_count += 1
                continue
            
            print(f"Setting integration_type to '{integration_type}' for {integration_name}")
            
            # Update the manifest
            if not self.update_manifest(manifest_path, integration_type):
                failed_count += 1
                continue
            
            print(f"✓ Updated {manifest_path}")
            
            # Validate the manifest
            if not self.validate_manifest(manifest_path):
                print(f"Warning: Validation failed for {integration_name}")
                print("The file has been updated but may have issues.")
                failed_count += 1
                continue
            
            # Commit the changes
            if not self.commit_changes(manifest_path, integration_name):
                failed_count += 1
                continue
            
            updated_count += 1
        
        # Print summary
        print()
        print("=" * 70)
        print("Summary:")
        print(f"  Updated: {updated_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"  Failed:  {failed_count}")
        print("=" * 70)
        
        # Run full validation if any updates were made
        if updated_count > 0:
            print()
            print("Running full validation with python3 -m script.hassfest...")
            print()
            if not self.run_full_validation():
                print()
                print("Warning: Full validation failed. Please review the errors above.")
                return 1
        
        return 0 if failed_count == 0 else 1


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent
    manager = ManifestManager(repo_root)
    return manager.run()


if __name__ == "__main__":
    sys.exit(main())
