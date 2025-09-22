#!/usr/bin/env python3
"""
Simple E-commerce Application Test Script using Selenium
This script tests: Login, Add Products to Cart, Clear Cart

Based on best practices from QA Touch Selenium tutorial
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests

class TestRailClient:
    def __init__(self, base_url, user, api_key, run_id):
        self.base_url = base_url.rstrip('/')
        self.user = user
        self.api_key = api_key
        self.run_id = run_id
        self.headers = {'Content-Type': 'application/json'}
        self.auth = (self.user, self.api_key)

    def add_result_for_case(self, case_id, status_id, comment=''):
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{self.run_id}/{case_id}"
        payload = {
            "status_id": status_id,
            "comment": comment
        }
        try:
            response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            print(f"✅ Reported result to TestRail: case_id={case_id}, status_id={status_id}")
        except Exception as e:
            print(f"❌ Failed to report result to TestRail: {str(e)}")

# TestRail configuration
testrail_client = TestRailClient(
    base_url="https://shxrvsh.testrail.io",
    user="22i256@psgtech.ac.in",
    api_key="/soPmKYAFP.HNfFFwkNC-9NAYYReCB42JmlSyaXKz",
    run_id=4
)

# Mapping of test steps to TestRail case IDs
CASE_IDS = {
    "login": 7,
    "add_products": 8,
    "check_cart": 9,
    "clear_cart": 10
}


def setup_chrome_driver():
    """Set up and return a Chrome WebDriver with basic options"""
    print("🔧 Setting up Chrome driver...")
    
    # Basic Chrome options for testing
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Create Chrome driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Set wait times
    driver.implicitly_wait(10)
    
    print("✅ Chrome driver ready!")
    return driver


def login_to_app(driver, email, password):
    """Login to the e-commerce application"""
    print(f"🔐 Logging in with email: {email}")
    
    try:
        # Find login form elements
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Clear and fill the form
        email_input.clear()
        email_input.send_keys(email)
        
        password_input.clear()
        password_input.send_keys(password)
        
        # Click login button
        login_button.click()
        time.sleep(3)
        
        # Check if login was successful - try multiple verification methods
        login_successful = False
        
        # Method 1: Check for immediate alert
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            if "Login successful" in alert_text:
                print("✅ Login successful! (alert confirmed)")
                login_successful = True
            else:
                print(f"⚠️ Login alert: {alert_text}")
        except:
            pass
        
        # Method 2: Manually reload page and look for logout button
        if not login_successful:
            try:
                print("🔄 Manually reloading page to see logout button...")
                driver.refresh()
                time.sleep(3)
                logout_button = driver.find_element(By.CSS_SELECTOR, ".cart-clear-btn")
                print("✅ Login successful! (logout button found after reload)")
                login_successful = True
            except:
                pass
        
        # Method 3: Try to access protected pages to verify login
        if not login_successful:
            try:
                print("🔍 Trying to access protected pages to verify login...")
                # Try to access cart page directly
                current_url = driver.current_url
                base_url = f"{driver.current_url.split('/')[0]}//{driver.current_url.split('/')[2]}"
                driver.get(f"{base_url}/cart")
                time.sleep(2)
                
                # Check if we see cart content (not redirected to login)
                cart_elements = driver.find_elements(By.CSS_SELECTOR, ".cart-container, .cart-title")
                if cart_elements:
                    print("✅ Login successful! (can access protected pages)")
                    login_successful = True
                
                # Go back to previous page
                driver.get(current_url)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Protected page check failed: {str(e)}")
        
        # Method 4: Final attempt - reload and check for logout button
        if not login_successful:
            try:
                print("🔄 Final attempt: Reloading page and checking for logout button...")
                driver.refresh()
                time.sleep(3)
                
                # Look for logout button
                logout_button = driver.find_element(By.CSS_SELECTOR, ".cart-clear-btn")
                print("✅ Login successful! (logout button found on final reload)")
                login_successful = True
            except:
                pass
        
        if not login_successful:
            print("⚠️ Could not verify login success with any method")
            return False
        
        return True
                
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return False


def add_products_to_cart(driver):
    """Add products to the shopping cart"""
    print("🛒 Adding products to cart...")
    
    try:
        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".products-list"))
        )
        
        # Find all "Add to Cart" buttons
        add_buttons = driver.find_elements(By.CSS_SELECTOR, ".product-add-btn")
        
        if not add_buttons:
            print("⚠️ No products found to add to cart")
            return 0
        
        # Add first product to cart
        print("Adding first product...")
        add_buttons[0].click()
        time.sleep(2)
        
        # Handle alert if present
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("✅ First product added to cart")
        except:
            print("✅ First product added to cart")
        
        # Add second product if available
        if len(add_buttons) > 1:
            print("Adding second product...")
            add_buttons[1].click()
            time.sleep(2)
            
            try:
                alert = driver.switch_to.alert
                alert.accept()
                print("✅ Second product added to cart")
            except:
                print("✅ Second product added to cart")
        
        products_added = min(2, len(add_buttons))
        print(f"✅ Added {products_added} products to cart")
        return products_added
        
    except Exception as e:
        print(f"❌ Failed to add products to cart: {str(e)}")
        return 0


def check_cart_items(driver):
    """Check how many items are in the cart"""
    print("🔍 Checking cart contents...")
    
    try:
        # Wait for cart to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-container"))
        )
        
        # Count cart items
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
        
        if cart_items:
            print(f"✅ Cart has {len(cart_items)} items")
            return len(cart_items)
        else:
            # Check if empty message is present
            empty_message = driver.find_elements(By.XPATH, "//li[contains(text(), 'Your cart is empty')]")
            if empty_message:
                print("📭 Cart is empty")
                return 0
            else:
                print("⚠️ Could not determine cart status")
                return -1
                
    except Exception as e:
        print(f"❌ Failed to check cart: {str(e)}")
        return -1


def clear_cart(driver):
    """Clear all items from the cart"""
    print("🗑️ Clearing cart...")
    
    try:
        # Find and click clear cart button
        clear_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-clear-btn"))
        )
        clear_button.click()
        time.sleep(2)
        
        print("✅ Clear cart button clicked")
        return True
        
    except Exception as e:
        print(f"❌ Failed to clear cart: {str(e)}")
        return False


def verify_cart_empty(driver):
    """Verify that cart is empty after clearing"""
    print("🔍 Verifying cart is empty...")
    
    try:
        # Wait a moment for the cart to update
        time.sleep(2)
        
        # Check for empty cart message
        empty_message = driver.find_elements(By.XPATH, "//li[contains(text(), 'Your cart is empty')]")
        
        if empty_message:
            print("✅ Cart cleared successfully!")
            return True
        else:
            # Check if cart items are still present
            cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            if not cart_items:
                print("✅ Cart cleared successfully!")
                return True
            else:
                print(f"⚠️ Cart may not be fully cleared - {len(cart_items)} items still present")
                return False
                
    except Exception as e:
        print(f"❌ Failed to verify cart is empty: {str(e)}")
        return False


def run_ecommerce_test():
    """Main function to run the complete e-commerce test"""
    print("🚀 Starting E-commerce Application Test")
    print("=" * 50)
    
    # Test credentials
    test_email = "user@test.com"
    test_password = "test123"
    
    # Application URL
    app_url = "http://localhost:3000"
    
    driver = None
    
    try:
        # Step 1: Set up Chrome driver
        driver = setup_chrome_driver()
        
        # Step 2: Navigate to the application
        print("\n📱 Step 1: Opening the application...")
        driver.get(app_url)
        time.sleep(2)
        
        # Step 3: Navigate to login page
        print("\n🔑 Step 2: Going to login page...")
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
        )
        login_link.click()
        time.sleep(2)
        
        # Step 4: Perform login
        print("\n👤 Step 3: Logging in...")
        login_result = login_to_app(driver, test_email, test_password)
        if login_result:
            testrail_client.add_result_for_case(CASE_IDS["login"], 1, "Login successful")
        else:
            testrail_client.add_result_for_case(CASE_IDS["login"], 5, "Login failed")
            print("❌ Test failed: Could not login")
            return False
        

        
        # Step 5: Navigate to products page
        print("\n🛍️ Step 4: Going to products page...")
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Products')]"))
        )
        products_link.click()
        time.sleep(2)
        
        # Step 6: Add products to cart
        print("\n➕ Step 5: Adding products to cart...")
        products_added = add_products_to_cart(driver)
        if products_added == 0:
            testrail_client.add_result_for_case(CASE_IDS["add_products"], 5, "Failed to add products to cart")
            print("❌ Test failed: Could not add products to cart")
            return False
        else:
            testrail_client.add_result_for_case(CASE_IDS["add_products"], 1, f"Added {products_added} products to cart")
        
        # Step 7: Navigate to cart
        print("\n🛒 Step 6: Going to cart...")
        cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cart')]"))
        )
        cart_link.click()
        time.sleep(2)
        
        # Step 8: Verify cart has items
        print("\n✅ Step 7: Checking cart has items...")
        cart_items = check_cart_items(driver)
        if cart_items <= 0:
            testrail_client.add_result_for_case(CASE_IDS["check_cart"], 5, "Cart verification failed")
            print("❌ Test failed: Cart verification failed")
            return False
        else:
            testrail_client.add_result_for_case(CASE_IDS["check_cart"], 1, f"Cart has {cart_items} items")
        
        # Step 9: Clear cart
        print("\n🗑️ Step 8: Clearing cart...")
        clear_result = clear_cart(driver)
        verify_empty_result = False
        if clear_result:
            verify_empty_result = verify_cart_empty(driver)
        
        if clear_result and verify_empty_result:
            testrail_client.add_result_for_case(CASE_IDS["clear_cart"], 1, "Cart cleared successfully")
        else:
            testrail_client.add_result_for_case(CASE_IDS["clear_cart"], 5, "Failed to clear cart or verify empty")
            print("❌ Test failed: Could not clear cart or verify empty")
            return False
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        # Attempt to report failure for all remaining test cases if possible
        try:
            testrail_client.add_result_for_case(CASE_IDS.get("login", 0), 5, f"Test failed with error: {str(e)}")
            testrail_client.add_result_for_case(CASE_IDS.get("add_products", 0), 5, f"Test failed with error: {str(e)}")
            testrail_client.add_result_for_case(CASE_IDS.get("check_cart", 0), 5, f"Test failed with error: {str(e)}")
            testrail_client.add_result_for_case(CASE_IDS.get("clear_cart", 0), 5, f"Test failed with error: {str(e)}")
        except:
            pass
        print(f"\n❌ Test failed with error: {str(e)}")
        return False
        
    finally:
        # Always close the browser
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()


def main():
    """Main function to run the test"""
    print("⚠️  IMPORTANT: Make sure your e-commerce application is running!")
    print("   - Backend: http://localhost:5050")
    print("   - Frontend: http://localhost:3000")
    print("   - Test credentials: user@test.com / test123")
    print()
    
    input("Press Enter to start testing...")
    
    # Run the test
    success = run_ecommerce_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎯 RESULT: All tests passed! Your e-commerce app is working correctly.")
    else:
        print("🔍 RESULT: Some tests failed. Check the output above for details.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
