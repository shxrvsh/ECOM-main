# E-commerce Application Testing Guide

This guide explains how to test your e-commerce application using the simplified Selenium test script.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install Python packages
pip3 install -r requirements.txt

# Or use the setup script
chmod +x setup_test_env.sh
./setup_test_env.sh
```

### 2. Start Your Application
Make sure both parts of your application are running:
- **Backend**: `http://localhost:5050`
- **Frontend**: `http://localhost:3000`

### 3. Run the Test
```bash
python3 ecommerce_test_simple.py
```

## 📋 What the Test Does

The script automatically tests these features:

1. **🔑 Login** - Logs in with test credentials (user@test.com / test123)
2. **🛍️ Browse Products** - Goes to the products page
3. **➕ Add to Cart** - Adds 2 products to the shopping cart
4. **🛒 View Cart** - Checks that items are in the cart
5. **🗑️ Clear Cart** - Removes all items from the cart
6. **✅ Verify** - Confirms the cart is empty

## 🛠️ Requirements

- **Python 3.6+**
- **Google Chrome browser**
- **Internet connection** (for downloading ChromeDriver)

## 📁 Files

- `ecommerce_test_simple.py` - **Main test script** (use this one!)
- `ecommerce_test.py` - Advanced version with unittest framework
- `requirements.txt` - Python package dependencies
- `setup_test_env.sh` - Setup script for Unix/Mac

## 🔧 Troubleshooting

### Common Issues:

1. **"Chrome not found"**
   - Install Google Chrome browser

2. **"Port already in use"**
   - Make sure your app is running on the correct ports
   - Check if another application is using ports 3000 or 5050

3. **"Element not found"**
   - Make sure your application is fully loaded
   - Check that the frontend is running on port 3000

4. **"Login failed"**
   - Verify the test credentials work manually
   - Check that the backend is running on port 5050

## 📚 How It Works

The script uses **Selenium WebDriver** to:
- Control a Chrome browser automatically
- Find elements on web pages using CSS selectors
- Click buttons and fill forms
- Wait for pages to load
- Handle alerts and popups

## 🎯 Test Results

- **✅ Success**: All steps completed successfully
- **❌ Failure**: One or more steps failed
- **⚠️ Warning**: Something unexpected happened but didn't fail

## 🔄 Running Multiple Times

You can run the test multiple times to verify consistency. The script automatically:
- Opens a fresh browser session each time
- Cleans up after itself
- Provides detailed feedback for each step

## 📖 Learning More

This script demonstrates basic Selenium concepts:
- **Element Location**: Finding buttons, forms, and text
- **User Interactions**: Clicking, typing, waiting
- **Error Handling**: Graceful failure and cleanup
- **Page Navigation**: Moving between different pages

For more advanced testing, check out the [QA Touch Selenium tutorial](https://www.qatouch.com/blog/selenium-with-python-tutorial/).
