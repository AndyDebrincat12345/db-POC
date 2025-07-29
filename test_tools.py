#!/usr/bin/env python3
"""
Quick Test Script for Migration Tools
Test all three tools individually to debug issues
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_bytebase():
    """Test Bytebase connection"""
    print("🔵 Testing Bytebase...")
    try:
        from bytebase_api import BytebaseAPI
        api = BytebaseAPI()
        result = api.authenticate()
        print(f"✅ Bytebase authentication: {result}")
        return True
    except Exception as e:
        print(f"❌ Bytebase error: {e}")
        return False

def test_liquibase():
    """Test Liquibase"""
    print("🟣 Testing Liquibase...")
    try:
        import subprocess
        os.chdir('liquibase')
        result = subprocess.run(['liquibase', '--version'], capture_output=True, text=True, shell=True)
        os.chdir('..')
        if result.returncode == 0:
            print(f"✅ Liquibase version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Liquibase error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Liquibase error: {e}")
        return False

def test_redgate():
    """Test Redgate simulator"""
    print("🔴 Testing Redgate...")
    try:
        from redgate_simulator import RedgateSimulator
        simulator = RedgateSimulator()
        
        # Test database connection
        conn = simulator.get_connection()
        conn.close()
        print("✅ Redgate database connection successful")
        
        # Test migration path
        migrations_path = os.path.abspath("redgate/migrations")
        print(f"📁 Migration path: {migrations_path}")
        print(f"📁 Path exists: {os.path.exists(migrations_path)}")
        
        if os.path.exists(migrations_path):
            files = [f for f in os.listdir(migrations_path) if f.endswith('.sql')]
            print(f"📄 SQL files found: {len(files)}")
            for f in files:
                print(f"  - {f}")
        
        return True
    except Exception as e:
        print(f"❌ Redgate error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Migration Tools Test Suite")
    print("=" * 50)
    
    results = {
        'bytebase': test_bytebase(),
        'liquibase': test_liquibase(), 
        'redgate': test_redgate()
    }
    
    print("\n📊 Test Results:")
    print("-" * 30)
    for tool, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{tool.capitalize()}: {status}")
    
    all_pass = all(results.values())
    print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if all_pass else '❌ SOME TESTS FAILED'}")

if __name__ == "__main__":
    main()
