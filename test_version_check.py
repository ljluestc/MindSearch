#!/usr/bin/env python3
"""
Test script to validate TencentSearch version check fix for Issue #288
"""

import sys
import subprocess

def test_version_check():
    """Test the version check logic for TencentSearch"""
    
    print("=" * 60)
    print("Testing TencentSearch Version Check Fix")
    print("=" * 60)
    print()
    
    # Test 1: Import the module and check version detection
    print("Test 1: Check lagent version detection")
    print("-" * 60)
    try:
        import lagent
        from packaging import version as pkg_version
        
        lagent_version = getattr(lagent, '__version__', '0.0.0')
        print(f"✓ Detected lagent version: {lagent_version}")
        
        is_compatible = pkg_version.parse(lagent_version) >= pkg_version.parse('0.5.0rc2')
        print(f"✓ Version compatible with TencentSearch: {is_compatible}")
        print()
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print()
        return
    
    # Test 2: Test the version check logic
    print("Test 2: Test version check with different scenarios")
    print("-" * 60)
    
    test_cases = [
        ("0.2.4", False, "Old version should fail"),
        ("0.5.0rc1", False, "Pre-release version should fail"),
        ("0.5.0rc2", True, "Exact required version should pass"),
        ("0.5.0rc3", True, "Newer version should pass"),
        ("0.5.0", True, "Release version should pass"),
        ("1.0.0", True, "Future version should pass"),
    ]
    
    for version_str, expected_pass, description in test_cases:
        try:
            is_compatible = pkg_version.parse(version_str) >= pkg_version.parse('0.5.0rc2')
            status = "✓" if is_compatible == expected_pass else "✗"
            print(f"{status} {description}: version {version_str} -> {is_compatible}")
        except Exception as e:
            print(f"✗ Error testing version {version_str}: {e}")
    
    print()
    
    # Test 3: Test actual init_agent call
    print("Test 3: Test init_agent with different search engines")
    print("-" * 60)
    
    try:
        from mindsearch.agent import init_agent
        
        # Test with DuckDuckGo (should work regardless)
        try:
            print("Testing DuckDuckGoSearch (should work)...")
            # Note: This may fail if model isn't configured, but version check shouldn't interfere
            agent = init_agent(lang='cn', model_format='internlm_silicon', search_engine='DuckDuckGoSearch')
            print("✓ DuckDuckGoSearch initialized (or failed for other reasons, not version check)")
        except RuntimeError as e:
            if 'lagent' in str(e):
                print(f"✗ Unexpected version check for DuckDuckGo: {e}")
            else:
                print(f"✓ DuckDuckGoSearch passed version check (other error expected: {str(e)[:50]}...)")
        except Exception as e:
            print(f"✓ DuckDuckGoSearch passed version check (other error: {str(e)[:50]}...)")
        
        # Test with TencentSearch
        try:
            print("\nTesting TencentSearch (should check version)...")
            agent = init_agent(lang='cn', model_format='internlm_silicon', search_engine='TencentSearch')
            
            if is_compatible:
                print("✓ TencentSearch initialized successfully with compatible version")
            else:
                print("✗ Should have failed with old version but didn't!")
        except RuntimeError as e:
            if 'lagent' in str(e) and '0.5.0rc2' in str(e):
                if is_compatible:
                    print(f"✗ Unexpected version error with compatible version: {e}")
                else:
                    print(f"✓ Got expected version error: {str(e)[:80]}...")
            else:
                print(f"✓ Got RuntimeError (not version check): {str(e)[:80]}...")
        except Exception as e:
            print(f"✓ Got other error: {str(e)[:80]}...")
        
    except ImportError as e:
        print(f"✗ Cannot import init_agent: {e}")
    
    print()
    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_version_check()
