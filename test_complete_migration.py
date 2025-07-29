#!/usr/bin/env python3
"""
Complete migration test to simulate GUI behavior
"""
import os
import sys

# Add the project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_complete_migration_workflow():
    """Test the complete migration workflow as it would run in the GUI"""
    print("🧪 Complete Migration Workflow Test")
    print("=" * 50)
    
    # Test Redgate
    print("🔴 Starting Redgate migration...")
    try:
        from redgate_simulator import RedgateSimulator
        
        simulator = RedgateSimulator()
        migrations_path = os.path.join(project_root, "redgate", "migrations")
        print(f"📁 Using migration path: {migrations_path}")
        
        results = simulator.deploy_migration_package(migrations_path)
        for result in results:
            print(f"  {result}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
    
    # Test Liquibase
    print("🟣 Starting Liquibase migration...")
    try:
        import subprocess
        
        # Change to liquibase directory and run update
        liquibase_dir = os.path.join(project_root, "liquibase")
        original_dir = os.getcwd()
        
        os.chdir(liquibase_dir)
        result = subprocess.run(
            ["liquibase", "update"],
            capture_output=True,
            text=True,
            timeout=30
        )
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print("✅ Liquibase update successful")
            # Parse output for summary
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'UPDATE SUMMARY' in line or 'Run:' in line or 'Previously run:' in line or 'Total change sets:' in line:
                    print(line)
        else:
            print(f"❌ Liquibase failed: {result.stderr}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
    
    # Test Bytebase
    print("🔵 Starting Bytebase migration...")
    try:
        from bytebase_api import BytebaseAPI
        
        api = BytebaseAPI()
        
        # Create project
        project = api.create_project("gui-migration-test")
        print(f"✅ Project created: {project.get('title', 'Unknown')}")
        
        # Execute migration folder
        migrations_path = os.path.join(project_root, "bytebase", "migrations")
        results = api.execute_migration_folder(migrations_path)
        
        for result in results:
            print(f"  {result}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()
    print("🎯 Migration workflow test completed!")

if __name__ == "__main__":
    test_complete_migration_workflow()
