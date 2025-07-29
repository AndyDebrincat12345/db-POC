#!/usr/bin/env python3
"""
Test script to verify the specific migration errors are fixed
"""
import os
import sys

# Add the project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_redgate_migration():
    """Test Redgate migration with the fixed path handling"""
    print("🔴 Testing Redgate migration...")
    
    try:
        from redgate_simulator import RedgateSimulator
        
        # Create simulator instance
        simulator = RedgateSimulator()
        
        # Test the exact path that was causing issues
        migrations_path = os.path.join(project_root, "redgate", "migrations")
        print(f"📁 Using migration path: {migrations_path}")
        
        # Deploy migration package
        results = simulator.deploy_migration_package(migrations_path)
        
        print("✅ Redgate migration completed successfully!")
        for result in results:
            print(f"   {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Redgate migration failed: {str(e)}")
        return False

def test_bytebase_migration():
    """Test Bytebase migration with the fixed API handling"""
    print("🔵 Testing Bytebase migration...")
    
    try:
        from bytebase_api import BytebaseAPI
        
        # Create API instance
        api = BytebaseAPI()
        
        # Test authentication
        api.authenticate()
        print("✅ Bytebase authentication successful")
        
        # Test project creation (the issue that was causing JSON errors)
        project = api.create_project("Test POC Database")
        print(f"✅ Bytebase project creation successful: {project.get('title', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Bytebase migration failed: {str(e)}")
        return False

def main():
    """Run all migration tests"""
    print("🧪 Testing Migration Error Fixes")
    print("=" * 40)
    
    redgate_ok = test_redgate_migration()
    print()
    bytebase_ok = test_bytebase_migration()
    
    print()
    print("📊 Results:")
    print("-" * 20)
    print(f"Redgate: {'✅ FIXED' if redgate_ok else '❌ STILL FAILING'}")
    print(f"Bytebase: {'✅ FIXED' if bytebase_ok else '❌ STILL FAILING'}")
    
    if redgate_ok and bytebase_ok:
        print("🎯 ✅ ALL MIGRATION ERRORS FIXED!")
        return True
    else:
        print("🎯 ❌ Some issues remain")
        return False

if __name__ == "__main__":
    main()
