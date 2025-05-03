"""
Test script to verify the package installation and executable functionality.
"""

import subprocess
import sys
import os
import shutil

def main():
    print("Testing map-solver-playground package installation...")
    
    # Build the package
    print("\nBuilding the package...")
    result = subprocess.run(["python", "-m", "pip", "install", "-e", "."], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error building the package:")
        print(result.stderr)
        return False
    
    print("Package built and installed successfully.")
    
    # Check if the executable was created
    print("\nChecking for map-solver.exe...")
    scripts_dir = os.path.join(sys.prefix, "Scripts")
    exe_path = os.path.join(scripts_dir, "map-solver.exe")
    
    if os.path.exists(exe_path):
        print(f"map-solver.exe found at: {exe_path}")
    else:
        print(f"map-solver.exe not found at: {exe_path}")
        return False
    
    print("\nPackage installation test completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)