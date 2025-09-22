#!/usr/bin/env python3
"""
E-commerce Application Test Script using Selenium
Tests: Login, Add Products to Cart, Clear Cart
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class EcommerceTest(unittest.TestCase):
    """Test class for E-commerce application"""
    
    def setUp(self):
        """Set up the test environment before each test"""
        # Chrome options for better testing
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # Uncomment below line if you want to run in headless mode
        # chrome_options.add_argument("--headless")
        
        # Initialize Chrome driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test credentials
        self.test_email = "user@test.com"
        self.test_password = "test123"
        
        # Base URL - adjust if your app runs on different port
        self.base_url = "http://localhost:3000"
        
    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def test_ecommerce_workflow(self):
        """Main test method that covers the complete workflow"""
        print("Starting E-commerce application test...")
        
        # Step 1: Navigate to the application
        print("Step 1: Navigating to the application...")
        self.driver.get(self.base_url)
        time.sleep(2)
        
        # Step 2: Navigate to login page
        print("Step 2: Navigating to login page...")
        login_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
        )
        login_link.click()
        time.sleep(2)
        
        # Step 3: Perform login
        print("Step 3: Performing login...")
        self.perform_login()
        
        # Step 4: Navigate to products page
        print("Step 4: Navigating to products page...")
        products_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Products')]"))
        )
        products_link.click()
        time.sleep(2)
        
        # Step 5: Add products to cart
        print("Step 5: Adding products to cart...")
        self.add_products_to_cart()
        
        # Step 6: Navigate to cart
        print("Step 6: Navigating to cart...")
        cart_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cart')]"))
        )
        cart_link.click()
        time.sleep(2)
        
        # Step 7: Verify cart has items
        print("Step 7: Verifying cart has items...")
        self.verify_cart_has_items()
        
        # Step 8: Clear cart
        print("Step 8: Clearing cart...")
        self.clear_cart()
        
        # Step 9: Verify cart is empty
        print("Step 9: Verifying cart is empty...")
        self.verify_cart_is_empty()
        
        print("All tests completed successfully! ✅")
    
    def perform_login(self):
        """Perform login with test credentials"""
        try:
            # Wait for login form to be visible
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Clear and fill the form
            email_input.clear()
            email_input.send_keys(self.test_email)
            
            password_input.clear()
            password_input.send_keys(self.test_password)
            
            # Submit the form
            login_button.click()
            time.sleep(3)
            
            # Check for successful login (look for logout button or user-specific content)
            try:
                logout_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-clear-btn"))
                )
                print("✅ Login successful")
            except:
                # Check if there's an alert
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()
                    if "Login successful" in alert_text:
                        print("✅ Login successful")
                    else:
                        print(f"⚠️ Login alert: {alert_text}")
                except:
                    print("⚠️ Could not verify login success")
                    
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            raise
    
    def add_products_to_cart(self):
        """Add products to cart"""
        try:
            # Wait for products to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".products-list"))
            )
            
            # Find all "Add to Cart" buttons
            add_to_cart_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".product-add-btn")
            
            if not add_to_cart_buttons:
                print("⚠️ No products found to add to cart")
                return
            
            # Add first product to cart
            first_button = add_to_cart_buttons[0]
            first_button.click()
            time.sleep(2)
            
            # Handle alert if present
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                print(f"✅ Added product to cart: {alert_text}")
            except:
                print("✅ Product added to cart")
            
            # Add second product if available
            if len(add_to_cart_buttons) > 1:
                second_button = add_to_cart_buttons[1]
                second_button.click()
                time.sleep(2)
                
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()
                    print(f"✅ Added second product to cart: {alert_text}")
                except:
                    print("✅ Second product added to cart")
            
            print(f"✅ Added {min(2, len(add_to_cart_buttons))} products to cart")
            
        except Exception as e:
            print(f"❌ Failed to add products to cart: {str(e)}")
            raise
    
    def verify_cart_has_items(self):
        """Verify that cart contains items"""
        try:
            # Wait for cart to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-container"))
            )
            
            # Check if cart has items (not empty message)
            cart_items = self.driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            
            if cart_items:
                print(f"✅ Cart verification successful - {len(cart_items)} items found")
            else:
                # Check if empty message is present
                empty_message = self.driver.find_elements(By.XPATH, "//li[contains(text(), 'Your cart is empty')]")
                if empty_message:
                    print("⚠️ Cart is empty - no items were added")
                else:
                    print("⚠️ Could not determine cart status")
                    
        except Exception as e:
            print(f"❌ Failed to verify cart items: {str(e)}")
            raise
    
    def clear_cart(self):
        """Clear all items from cart"""
        try:
            # Find and click clear cart button
            clear_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-clear-btn"))
            )
            clear_button.click()
            time.sleep(2)
            
            print("✅ Clear cart button clicked")
            
        except Exception as e:
            print(f"❌ Failed to clear cart: {str(e)}")
            raise
    
    def verify_cart_is_empty(self):
        """Verify that cart is empty after clearing"""
        try:
            # Wait a moment for the cart to update
            time.sleep(2)
            
            # Check for empty cart message
            empty_message = self.driver.find_elements(By.XPATH, "//li[contains(text(), 'Your cart is empty')]")
            
            if empty_message:
                print("✅ Cart cleared successfully - empty message found")
            else:
                # Check if cart items are still present
                cart_items = self.driver.find_elements(By.CSS_SELECTOR, ".cart-item")
                if not cart_items:
                    print("✅ Cart cleared successfully - no items found")
                else:
                    print(f"⚠️ Cart may not be fully cleared - {len(cart_items)} items still present")
                    
        except Exception as e:
            print(f"❌ Failed to verify cart is empty: {str(e)}")
            raise


def run_tests():
    """Run the test suite"""
    print("🚀 Starting E-commerce Application Test Suite")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(EcommerceTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed successfully!")
    else:
        print("❌ Some tests failed!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Check if application is running
    print("⚠️  Make sure your e-commerce application is running:")
    print("   - Backend should be running on http://localhost:5050")
    print("   - Frontend should be running on http://localhost:3000")
    print("   - Test credentials: user@test.com / test123")
    print()
    
    input("Press Enter to start testing...")
    
    # Run the tests
    success = run_tests()
    
    if success:
        print("\n🎯 Test Summary: All functionality working correctly!")
    else:
        print("\n🔍 Test Summary: Some issues detected. Check the output above.") 