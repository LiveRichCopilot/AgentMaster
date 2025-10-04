#!/usr/bin/env python3
"""
Test CloudExpert IAM Permissions
Check if the service account has required permissions before testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from jai_cortex.sub_agents.cloud_expert import (
    check_project_status,
    list_enabled_services,
    check_cloud_storage_buckets,
    check_firestore_database,
    PROJECT_ID
)


class MockToolContext:
    """Mock ToolContext for testing"""
    pass


def test_permissions():
    """Test each CloudExpert tool to check IAM permissions"""
    
    print("=" * 80)
    print("🔐 CLOUDEXPERT IAM PERMISSIONS TEST")
    print("=" * 80)
    print(f"\nProject ID: {PROJECT_ID}\n")
    
    ctx = MockToolContext()
    results = {
        'passed': [],
        'failed': [],
        'permission_needed': []
    }
    
    # Test 1: Project Status
    print("1️⃣  Testing: check_project_status()")
    print("-" * 80)
    result = check_project_status(ctx)
    if result['status'] == 'success':
        print(f"✅ SUCCESS: {result['message']}")
        print(f"   Project Name: {result.get('project_name', 'N/A')}")
        print(f"   Project State: {result.get('state', 'N/A')}")
        results['passed'].append('check_project_status')
    else:
        print(f"❌ FAILED: {result['message']}")
        results['failed'].append('check_project_status')
        if 'Permission denied' in result['message']:
            results['permission_needed'].append({
                'tool': 'check_project_status',
                'role': 'roles/resourcemanager.projectViewer',
                'command': f'gcloud projects add-iam-policy-binding {PROJECT_ID} --member="serviceAccount:YOUR_SERVICE_ACCOUNT" --role="roles/resourcemanager.projectViewer"'
            })
    print()
    
    # Test 2: List Services
    print("2️⃣  Testing: list_enabled_services()")
    print("-" * 80)
    result = list_enabled_services(ctx)
    if result['status'] == 'success':
        print(f"✅ SUCCESS: {result['message']}")
        print(f"   Total Services: {result.get('total_enabled', 0)}")
        print(f"   Key Services: {', '.join(result.get('key_services_enabled', []))}")
        results['passed'].append('list_enabled_services')
    else:
        print(f"❌ FAILED: {result['message']}")
        results['failed'].append('list_enabled_services')
        if 'Permission denied' in result['message']:
            results['permission_needed'].append({
                'tool': 'list_enabled_services',
                'role': 'roles/serviceusage.serviceUsageViewer',
                'command': f'gcloud projects add-iam-policy-binding {PROJECT_ID} --member="serviceAccount:YOUR_SERVICE_ACCOUNT" --role="roles/serviceusage.serviceUsageViewer"'
            })
    print()
    
    # Test 3: Cloud Storage
    print("3️⃣  Testing: check_cloud_storage_buckets()")
    print("-" * 80)
    result = check_cloud_storage_buckets(ctx)
    if result['status'] == 'success':
        print(f"✅ SUCCESS: {result['message']}")
        print(f"   Total Buckets: {result.get('total_buckets', 0)}")
        if result.get('buckets'):
            for bucket in result['buckets'][:3]:
                print(f"   • {bucket['name']} ({bucket['location']})")
        results['passed'].append('check_cloud_storage_buckets')
    else:
        print(f"❌ FAILED: {result['message']}")
        results['failed'].append('check_cloud_storage_buckets')
        if 'Permission denied' in result['message']:
            results['permission_needed'].append({
                'tool': 'check_cloud_storage_buckets',
                'role': 'roles/storage.objectViewer',
                'command': f'gcloud projects add-iam-policy-binding {PROJECT_ID} --member="serviceAccount:YOUR_SERVICE_ACCOUNT" --role="roles/storage.objectViewer"'
            })
    print()
    
    # Test 4: Firestore
    print("4️⃣  Testing: check_firestore_database()")
    print("-" * 80)
    result = check_firestore_database('agent-master-database', ctx)
    if result['status'] == 'success':
        print(f"✅ SUCCESS: {result['message']}")
        print(f"   Total Collections: {result.get('total_collections', 0)}")
        if result.get('collections'):
            for coll in result['collections'][:5]:
                print(f"   • {coll['name']} ({coll['sample_doc_count']} docs)")
        results['passed'].append('check_firestore_database')
    else:
        print(f"❌ FAILED: {result['message']}")
        results['failed'].append('check_firestore_database')
        if 'Permission denied' in result['message']:
            results['permission_needed'].append({
                'tool': 'check_firestore_database',
                'role': 'roles/datastore.user',
                'command': f'gcloud projects add-iam-policy-binding {PROJECT_ID} --member="serviceAccount:YOUR_SERVICE_ACCOUNT" --role="roles/datastore.user"'
            })
    print()
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {len(results['passed'])}/{len(results['passed']) + len(results['failed'])} tools")
    print(f"❌ Failed: {len(results['failed'])}/{len(results['passed']) + len(results['failed'])} tools")
    print()
    
    if results['passed']:
        print("✅ Working Tools:")
        for tool in results['passed']:
            print(f"   • {tool}")
        print()
    
    if results['failed']:
        print("❌ Failed Tools:")
        for tool in results['failed']:
            print(f"   • {tool}")
        print()
    
    if results['permission_needed']:
        print("🔧 REQUIRED FIXES:")
        print("=" * 80)
        print("\nYour service account needs these IAM roles:")
        print()
        for perm in results['permission_needed']:
            print(f"Tool: {perm['tool']}")
            print(f"Role Needed: {perm['role']}")
            print(f"Fix Command:")
            print(f"  {perm['command']}")
            print()
        
        print("💡 TIP: Find your service account email with:")
        print("  gcloud iam service-accounts list")
        print()
        print("Or check which account ADK is using:")
        print("  gcloud auth list")
        print()
    else:
        print("🎉 ALL TOOLS HAVE PROPER IAM PERMISSIONS!")
        print()
        print("✅ CloudExpert is ready to use in JAi Cortex")
        print("✅ All tools can access GCP APIs")
        print("✅ No IAM changes needed")
        print()
        print("🚀 You can now test CloudExpert at:")
        print("   http://localhost:8000/dev-ui/?app=jai_cortex")
    
    return len(results['failed']) == 0


if __name__ == "__main__":
    success = test_permissions()
    sys.exit(0 if success else 1)

