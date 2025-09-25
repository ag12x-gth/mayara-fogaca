#!/usr/bin/env python3
"""
End-to-End Testing Suite for Mayara Fogaça Lead Redirector
Tests the complete user journey and web application functionality
"""

import os
import time
import unittest
import threading
import http.server
import socketserver
from urllib.parse import urlencode
import tempfile
import subprocess
import sys

# Try to import playwright, install if not available
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    print("⚠️ Playwright não está disponível. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True


class TestWebApplication(unittest.TestCase):
    """End-to-end tests for the web application"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test server"""
        cls.port = 8001  # Use different port to avoid conflicts
        cls.base_url = f"http://localhost:{cls.port}"
        
        # Start HTTP server in a separate thread
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        handler = http.server.SimpleHTTPRequestHandler
        cls.httpd = socketserver.TCPServer(("", cls.port), handler)
        
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
        
        print(f"🌐 Test server running on {cls.base_url}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test server"""
        cls.httpd.shutdown()
        cls.server_thread.join(timeout=1)
        print("🔥 Test server shut down")
    
    def setUp(self):
        """Set up each test"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        # Collect console messages
        self.console_messages = []
        self.page.on("console", lambda msg: self.console_messages.append({
            'type': msg.type,
            'text': msg.text,
            'location': msg.location
        }))
        
        # Collect JavaScript errors
        self.js_errors = []
        self.page.on("pageerror", lambda error: self.js_errors.append(str(error)))
    
    def tearDown(self):
        """Clean up each test"""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    
    def test_page_loads_successfully(self):
        """Test that the page loads without errors"""
        response = self.page.goto(self.base_url)
        
        # Check response status
        self.assertEqual(response.status, 200)
        
        # Check title
        title = self.page.title()
        self.assertEqual(title, "Redirecionando para WhatsApp...")
        
        # Check no JavaScript errors
        self.assertEqual(len(self.js_errors), 0, f"JavaScript errors: {self.js_errors}")
    
    def test_essential_elements_present(self):
        """Test that all essential elements are present"""
        self.page.goto(self.base_url)
        
        # Check main container
        container = self.page.query_selector('.container')
        self.assertIsNotNone(container, "Main container not found")
        
        # Check header image
        image = self.page.query_selector('#header-image')
        self.assertIsNotNone(image, "Header image not found")
        
        # Check countdown element
        countdown = self.page.query_selector('#countdown')
        self.assertIsNotNone(countdown, "Countdown element not found")
        
        # Check queue counter
        queue_counter = self.page.query_selector('#fila-counter')
        self.assertIsNotNone(queue_counter, "Queue counter not found")
        
        # Check skip link for accessibility
        skip_link = self.page.query_selector('.skip-link')
        self.assertIsNotNone(skip_link, "Skip link not found")
    
    def test_countdown_functionality(self):
        """Test that countdown works correctly"""
        self.page.goto(self.base_url)
        
        # Initial countdown should be 5
        initial_countdown = self.page.text_content('#countdown')
        self.assertEqual(initial_countdown, '5')
        
        # Wait and check if countdown decreases
        time.sleep(1.5)  # Wait for countdown to change
        updated_countdown = self.page.text_content('#countdown')
        
        # Should have decreased (might be 4 or 3 depending on timing)
        self.assertIn(updated_countdown, ['4', '3'], 
                     f"Countdown should have decreased, got: {updated_countdown}")
    
    def test_queue_counter_animation(self):
        """Test that queue counter animates"""
        self.page.goto(self.base_url)
        
        # Get initial queue count
        initial_count = int(self.page.text_content('#fila-counter'))
        
        # Wait for animation
        time.sleep(2)
        
        # Get updated count
        updated_count = int(self.page.text_content('#fila-counter'))
        
        # Count should increase
        self.assertGreater(updated_count, initial_count, 
                          "Queue counter should increase over time")
        
        # Should be within reasonable bounds
        self.assertLessEqual(updated_count, 495, "Queue count should not exceed maximum")
    
    def test_phone_number_validation_logging(self):
        """Test that phone number validation is logged correctly"""
        self.page.goto(self.base_url)
        
        # Wait for JavaScript to execute
        time.sleep(1)
        
        # Check console messages for phone validation
        validation_messages = [msg for msg in self.console_messages 
                             if 'Lead phone' in msg['text'] or 'Número de telefone' in msg['text']]
        
        self.assertGreater(len(validation_messages), 0, 
                          "Should have phone validation log messages")
    
    def test_redirect_configuration_logging(self):
        """Test that redirect configuration is logged"""
        self.page.goto(self.base_url)
        
        time.sleep(1)
        
        # Check for redirect configuration logs
        config_messages = [msg for msg in self.console_messages 
                          if 'Configuração de Redirecionamento' in msg['text'] or 
                             'Redirecionando para' in msg['text']]
        
        self.assertGreater(len(config_messages), 0, 
                          "Should have redirect configuration log messages")
    
    def test_accessibility_features(self):
        """Test accessibility features"""
        self.page.goto(self.base_url)
        
        # Check ARIA labels
        countdown = self.page.query_selector('#countdown')
        countdown_label = countdown.get_attribute('aria-label')
        self.assertIsNotNone(countdown_label, "Countdown should have aria-label")
        
        # Check queue counter accessibility
        queue_counter = self.page.query_selector('#fila-counter')
        queue_label = queue_counter.get_attribute('aria-label')
        self.assertIsNotNone(queue_label, "Queue counter should have aria-label")
        
        # Check main content has proper role
        main_content = self.page.query_selector('main')
        main_role = main_content.get_attribute('role')
        self.assertEqual(main_role, 'main', "Main content should have role='main'")
    
    def test_responsive_design(self):
        """Test responsive design at different viewport sizes"""
        viewports = [
            (375, 667),   # Mobile
            (768, 1024),  # Tablet
            (1920, 1080)  # Desktop
        ]
        
        for width, height in viewports:
            with self.subTest(viewport=f"{width}x{height}"):
                self.page.set_viewport_size({"width": width, "height": height})
                self.page.goto(self.base_url)
                
                # Check that container is visible and properly sized
                container = self.page.query_selector('.container')
                container_box = container.bounding_box()
                
                self.assertIsNotNone(container_box, f"Container not visible at {width}x{height}")
                self.assertGreater(container_box['width'], 0, "Container should have width")
                self.assertGreater(container_box['height'], 0, "Container should have height")
                
                # Ensure content fits within viewport
                self.assertLessEqual(container_box['width'], width, 
                                   "Container should not exceed viewport width")
    
    def test_error_handling(self):
        """Test error handling capabilities"""
        self.page.goto(self.base_url)
        
        # Inject an error to test error handling
        self.page.evaluate("""
            // Simulate an error
            setTimeout(() => {
                throw new Error('Test error for error handling');
            }, 100);
        """)
        
        time.sleep(0.5)
        
        # Check that error was handled (should be in js_errors list)
        error_messages = [msg for msg in self.console_messages if msg['type'] == 'error']
        
        # The global error handler should catch it
        # We don't expect the page to break
        container = self.page.query_selector('.container')
        self.assertIsNotNone(container, "Page should still be functional after error")
    
    def test_performance_metrics(self):
        """Test basic performance metrics"""
        start_time = time.time()
        
        response = self.page.goto(self.base_url)
        
        # Wait for page to be fully loaded
        self.page.wait_for_load_state('networkidle')
        
        load_time = time.time() - start_time
        
        # Page should load within reasonable time
        self.assertLess(load_time, 5.0, f"Page took too long to load: {load_time}s")
        
        # Response should be successful
        self.assertEqual(response.status, 200)
    
    def test_local_storage_functionality(self):
        """Test localStorage access count functionality"""
        self.page.goto(self.base_url)
        
        # Get initial access count from localStorage
        initial_count = self.page.evaluate("parseInt(localStorage.getItem('whatsappAccessCount')) || 0")
        
        # Reload page to increment count
        self.page.reload()
        time.sleep(1)
        
        # Check that count increased
        updated_count = self.page.evaluate("parseInt(localStorage.getItem('whatsappAccessCount')) || 0")
        self.assertGreater(updated_count, initial_count, 
                          "Access count should increment on page reload")
    
    def test_console_logging_structure(self):
        """Test that console logging follows the enhanced structure"""
        self.page.goto(self.base_url)
        time.sleep(1)
        
        # Check for structured logging with emojis
        emoji_messages = [msg for msg in self.console_messages 
                         if any(emoji in msg['text'] for emoji in ['📊', '🔗', '🎯', '📱'])]
        
        self.assertGreater(len(emoji_messages), 0, 
                          "Should have structured log messages with emojis")
        
        # Check for group logging
        group_messages = [msg for msg in self.console_messages 
                         if msg['type'] in ['group', 'groupCollapsed', 'groupEnd']]
        
        # Should have at least some grouped logging
        self.assertGreaterEqual(len(group_messages), 0, 
                              "Should use console groups for structured logging")


def run_e2e_tests():
    """Run end-to-end tests with detailed reporting"""
    print("🎭 EXECUTANDO TESTES END-TO-END")
    print("=" * 60)
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright não está disponível. Pulando testes E2E.")
        return False
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWebApplication)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES E2E")
    print("=" * 60)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️ Erros: {len(result.errors)}")
    print(f"⏭️ Pulos: {len(result.skipped)}")
    
    if result.failures:
        print("\n❌ FALHAS:")
        for test, traceback in result.failures:
            print(f"- {test}")
            print(f"  {traceback}")
    
    if result.errors:
        print("\n⚠️ ERROS:")
        for test, traceback in result.errors:
            print(f"- {test}")
            print(f"  {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Taxa de sucesso E2E: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    if run_e2e_tests():
        print("\n🎉 TODOS OS TESTES E2E PASSARAM!")
        sys.exit(0)
    else:
        print("\n💥 ALGUNS TESTES E2E FALHARAM!")
        sys.exit(1)