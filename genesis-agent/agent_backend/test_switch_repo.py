#!/usr/bin/env python3
"""
Test CodeMaster's GitHub integration with the Switch repository
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


def main():
    print("=" * 80)
    print("🔍 ANALYZING YOUR SWITCH REPOSITORY")
    print("=" * 80)
    
    repo_url = "https://github.com/LiveRichCopilot/switch.git"
    
    print(f"\n📦 Cloning and analyzing: {repo_url}")
    print("⏳ This may take 10-30 seconds depending on repo size...\n")
    
    ctx = MockToolContext()
    result = analyze_github_repo(repo_url, ctx)
    
    if result['status'] == 'success':
        print("✅ SUCCESS! Repository analyzed:")
        print("=" * 80)
        print(f"\n📊 REPOSITORY STATISTICS:")
        print(f"   Repository Name: {result['repository']}")
        print(f"   Total Files: {result['statistics']['total_files']}")
        print(f"   Total Directories: {result['statistics']['total_directories']}")
        print(f"   Total Lines of Code: {result['statistics']['total_lines']:,}")
        print(f"   Primary Language: {result['primary_language']}")
        
        print(f"\n📝 LANGUAGES DETECTED:")
        for lang, count in result['statistics']['languages'].items():
            print(f"   • {lang}: {count} files")
        
        print(f"\n🔑 KEY FILES FOUND:")
        for file in result['key_files']:
            print(f"   • {file}")
        
        # Try to read a key file
        if result['key_files']:
            print("\n" + "=" * 80)
            print("📄 READING FIRST KEY FILE")
            print("=" * 80)
            
            first_file = result['key_files'][0]
            print(f"\n📖 Reading: {first_file}\n")
            
            file_result = read_github_file(repo_url, first_file, ctx)
            
            if file_result['status'] == 'success':
                print(f"✅ File read successfully!")
                print(f"   Lines: {file_result['metadata']['lines']}")
                print(f"   Size: {file_result['metadata']['size_bytes']} bytes")
                print(f"\n   First 800 characters:")
                print("   " + "-" * 76)
                content_preview = file_result['content'][:800]
                for line in content_preview.split('\n'):
                    print(f"   {line}")
                print("   " + "-" * 76)
            else:
                print(f"⚠️  Could not read file: {file_result['message']}")
        
        print("\n" + "=" * 80)
        print("🎉 GITHUB INTEGRATION WORKS!")
        print("=" * 80)
        print("\n💡 Now you can ask JAi Cortex:")
        print(f"   • 'Analyze {repo_url}'")
        print(f"   • 'Read the {result['key_files'][0] if result['key_files'] else '[filename]'}'")
        print(f"   • 'Scan this repo for security issues'")
        print(f"   • 'Review the code quality'")
        
        return 0
        
    else:
        print(f"❌ ERROR: {result['message']}")
        print("\n💡 Possible issues:")
        print("   • Repository might be private (needs to be public)")
        print("   • Network connection issue")
        print("   • Invalid repository URL")
        return 1


if __name__ == "__main__":
    sys.exit(main())

