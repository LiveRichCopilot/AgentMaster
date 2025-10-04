"""
Complete Verification System - Phase 2.6
Tests build integrity, backend functionality, AND frontend in a real browser
"""

import asyncio
import requests
from pathlib import Path
from typing import Tuple, List


class VerificationSystem:
    """
    Comprehensive verification with 3 layers:
    1. Build Integrity - All files exist and have content
    2. Backend Functionality - API endpoints work
    3. Frontend Functionality - UI works in real browser
    """
    
    def __init__(self, workspace_dir: str, port: int = 5001):
        self.workspace = Path(workspace_dir)
        self.port = port
        self.url = f"http://localhost:{port}"
        
    def verify_build_integrity(self, required_files: List[str]) -> Tuple[bool, List[str]]:
        """
        Verify ALL required files exist and have content
        """
        print(f"\n{'='*70}")
        print(f"🔍 VERIFICATION 1/3: Build Integrity")
        print(f"{'='*70}\n")
        
        errors = []
        
        for file_path in required_files:
            full_path = self.workspace / file_path
            
            # Check file exists
            if not full_path.exists():
                error = f"❌ Missing file: {file_path}"
                print(error)
                errors.append(error)
                continue
            
            # Check file has content (with file-specific thresholds)
            try:
                content = full_path.read_text()
                
                # File-specific minimum sizes
                min_size = 50  # Default
                if file_path == "requirements.txt":
                    min_size = 3  # Just needs "Flask" or similar
                elif file_path.endswith(".txt"):
                    min_size = 5
                
                if len(content.strip()) < min_size:
                    error = f"❌ File too small/empty: {file_path} ({len(content)} chars, min: {min_size})"
                    print(error)
                    errors.append(error)
                    continue
                    
                print(f"✅ {file_path} ({len(content)} chars)")
                
            except Exception as e:
                error = f"❌ Cannot read {file_path}: {e}"
                print(error)
                errors.append(error)
        
        if errors:
            print(f"\n❌ Build integrity check FAILED: {len(errors)} issues")
            return (False, errors)
        else:
            print(f"\n✅ Build integrity check PASSED")
            return (True, [])
    
    def verify_backend_functionality(self) -> Tuple[bool, List[str]]:
        """
        Verify backend API endpoints work
        """
        print(f"\n{'='*70}")
        print(f"🔍 VERIFICATION 2/3: Backend Functionality")
        print(f"{'='*70}\n")
        
        errors = []
        
        # Test 1: Home page
        try:
            print(f"Test: GET {self.url}")
            response = requests.get(self.url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Home page loads (200 OK)")
            else:
                error = f"❌ Home page failed: {response.status_code}"
                print(error)
                errors.append(error)
                
        except Exception as e:
            error = f"❌ Cannot connect to {self.url}: {e}"
            print(error)
            errors.append(error)
            return (False, errors)
        
        # Test 2: Chat endpoint
        try:
            print(f"\nTest: POST {self.url}/chat")
            response = requests.post(
                f"{self.url}/chat",
                json={"message": "test"},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Chat endpoint works (200 OK)")
            else:
                error = f"❌ Chat endpoint failed: {response.status_code}"
                print(error)
                errors.append(error)
                
        except Exception as e:
            error = f"❌ Chat endpoint error: {e}"
            print(error)
            errors.append(error)
        
        if errors:
            print(f"\n❌ Backend functionality check FAILED: {len(errors)} issues")
            return (False, errors)
        else:
            print(f"\n✅ Backend functionality check PASSED")
            return (True, [])
    
    async def verify_frontend_functionality(self) -> Tuple[bool, List[str]]:
        """
        Verify frontend works in a REAL BROWSER using Playwright
        This is the critical test that catches UI bugs
        """
        print(f"\n{'='*70}")
        print(f"🔍 VERIFICATION 3/3: Frontend Functionality (Browser)")
        print(f"{'='*70}\n")
        
        errors = []
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                # Launch browser
                print(f"🌐 Launching Chromium browser...")
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Capture console errors
                console_errors = []
                page.on('console', lambda msg: 
                    console_errors.append(msg.text) if msg.type == 'error' else None
                )
                
                # Navigate to app
                print(f"📄 Loading {self.url}...")
                try:
                    await page.goto(self.url, timeout=10000, wait_until='networkidle')
                    print(f"✅ Page loaded")
                except Exception as e:
                    error = f"❌ Page failed to load: {e}"
                    print(error)
                    errors.append(error)
                    await browser.close()
                    return (False, errors)
                
                # Check for JavaScript errors
                if console_errors:
                    error = f"❌ JavaScript errors detected: {console_errors}"
                    print(error)
                    errors.append(error)
                else:
                    print(f"✅ No JavaScript errors")
                
                # Check for required UI elements
                required_elements = [
                    ('#chat-container', 'Chat container'),
                    ('#message-form', 'Message form'),
                    ('#message-input', 'Message input'),
                    ('button[type="submit"]', 'Send button')
                ]
                
                print(f"\n🔍 Checking UI elements...")
                for selector, name in required_elements:
                    element = await page.query_selector(selector)
                    if element:
                        print(f"✅ Found: {name}")
                    else:
                        error = f"❌ Missing: {name} (selector: {selector})"
                        print(error)
                        errors.append(error)
                
                # Try to interact with the form
                print(f"\n🖱️  Testing user interaction...")
                try:
                    input_field = await page.query_selector('#message-input')
                    if input_field:
                        await input_field.fill('Test message')
                        print(f"✅ Can type in input field")
                    else:
                        error = f"❌ Cannot find input field for interaction"
                        errors.append(error)
                except Exception as e:
                    error = f"❌ Interaction failed: {e}"
                    print(error)
                    errors.append(error)
                
                await browser.close()
                
        except ImportError:
            error = f"❌ Playwright not installed. Run: pip install playwright && playwright install chromium"
            print(error)
            errors.append(error)
            return (False, errors)
        except Exception as e:
            error = f"❌ Browser testing failed: {e}"
            print(error)
            errors.append(error)
            return (False, errors)
        
        if errors:
            print(f"\n❌ Frontend functionality check FAILED: {len(errors)} issues")
            return (False, errors)
        else:
            print(f"\n✅ Frontend functionality check PASSED")
            return (True, [])
    
    async def run_all_verifications(self, required_files: List[str]) -> Tuple[bool, List[str]]:
        """
        Run all 3 verification layers
        Returns: (success, list_of_errors)
        """
        print(f"\n{'🔍'*35}")
        print(f"COMPREHENSIVE VERIFICATION SUITE")
        print(f"{'🔍'*35}\n")
        
        all_errors = []
        
        # Layer 1: Build Integrity
        success1, errors1 = self.verify_build_integrity(required_files)
        all_errors.extend(errors1)
        
        # Only continue if build is complete
        if not success1:
            return (False, all_errors)
        
        # Layer 2: Backend Functionality
        success2, errors2 = self.verify_backend_functionality()
        all_errors.extend(errors2)
        
        # Layer 3: Frontend Functionality (browser test)
        success3, errors3 = await self.verify_frontend_functionality()
        all_errors.extend(errors3)
        
        # Final verdict
        overall_success = success1 and success2 and success3
        
        print(f"\n{'='*70}")
        print(f"VERIFICATION SUMMARY")
        print(f"{'='*70}")
        print(f"Build Integrity:          {'✅ PASS' if success1 else '❌ FAIL'}")
        print(f"Backend Functionality:    {'✅ PASS' if success2 else '❌ FAIL'}")
        print(f"Frontend Functionality:   {'✅ PASS' if success3 else '❌ FAIL'}")
        print(f"{'='*70}")
        print(f"OVERALL: {'✅ ALL CHECKS PASSED' if overall_success else f'❌ FAILED ({len(all_errors)} issues)'}")
        print(f"{'='*70}\n")
        
        return (overall_success, all_errors)

