#!/usr/bin/env python3
"""
Quick test of CodeMaster's GitHub integration tools
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from jai_cortex.sub_agents.code_master import analyze_github_repo, read_github_file
from google.adk.tools import ToolContext


class MockToolContext:
    """Mock ToolContext for testing"""
    pass


def test_analyze_repo():
    """Test repository analysis"""
    print("=" * 80)
    print("TEST 1: Analyzing a small public repository")
    print("=" * 80)
    
    # Test with a small, popular repo
    repo_url = "https://github.com/psf/requests"
    
    print(f"\n📦 Cloning and analyzing: {repo_url}")
    print("This may take a few seconds...\n")
    
    ctx = MockToolContext()
    result = analyze_github_repo(repo_url, ctx)
    
    if result['status'] == 'success':
        print("✅ SUCCESS! Repository analyzed:")
        print(f"   Repository: {result['repository']}")
        print(f"   Total Files: {result['statistics']['total_files']}")
        print(f"   Total Lines: {result['statistics']['total_lines']}")
        print(f"   Primary Language: {result['primary_language']}")
        print(f"\n   Languages detected:")
        for lang, count in result['statistics']['languages'].items():
            print(f"      - {lang}: {count} files")
        print(f"\n   Key files found:")
        for file in result['key_files'][:5]:  # Show first 5
            print(f"      - {file}")
        return True
    else:
        print(f"❌ ERROR: {result['message']}")
        return False


def test_read_file():
    """Test reading a specific file"""
    print("\n" + "=" * 80)
    print("TEST 2: Reading a specific file from the repository")
    print("=" * 80)
    
    repo_url = "https://github.com/psf/requests"
    file_path = "README.md"
    
    print(f"\n📄 Reading file: {file_path}")
    print("This may take a few seconds...\n")
    
    ctx = MockToolContext()
    result = read_github_file(repo_url, file_path, ctx)
    
    if result['status'] == 'success':
        print("✅ SUCCESS! File read:")
        print(f"   File: {result['file_path']}")
        print(f"   Lines: {result['metadata']['lines']}")
        print(f"   Size: {result['metadata']['size_bytes']} bytes")
        print(f"\n   First 500 characters:")
        print("   " + "-" * 76)
        content_preview = result['content'][:500]
        for line in content_preview.split('\n'):
            print(f"   {line}")
        print("   " + "-" * 76)
        return True
    else:
        print(f"❌ ERROR: {result['message']}")
        return False


def main():
    """Run all tests"""
    print("\n🚀 Testing CodeMaster GitHub Integration Tools")
    print("=" * 80)
    
    # Test 1: Analyze repo
    test1_passed = test_analyze_repo()
    
    # Test 2: Read file
    test2_passed = test_read_file()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Test 1 (analyze_github_repo): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (read_github_file):    {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! GitHub integration is working!")
        print("\n💡 Now you can use these in JAi Cortex:")
        print("   - 'Analyze https://github.com/psf/requests'")
        print("   - 'Read the README.md from that repo'")
        print("   - 'Scan the main file for security issues'")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

