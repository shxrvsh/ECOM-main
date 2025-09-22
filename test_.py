import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This is a pytest fixture. It sets up the browser for each test function.
# It runs before each test and the 'yield' passes control to the test.
# After the test is done, the code after 'yield' is executed for cleanup.
import pytest

from testrail_client import TestRailClient

# Configure TestRail
TR = TestRailClient(
    base_url="https://shxrvsh.testrail.io", 
    user="22i256@psgtech.ac.in", 
    api_key="/soPmKYAFP.HNfFFwkNC-9NAYYReCB42JmlSyaXKz", 
    run_id=2   # 👈 replace 1 with your actual Test Run ID from TestRail
)

# Map your test cases to TestRail Case IDs
CASE_IDS = {
    "test_add_task_positive": 1,         # C101
    "test_add_task_negative_empty": 2,   # C102
    "test_mark_task_complete": 3,        # C103
    "test_unmark_task_complete": 4,      # C104
    "test_delete_task_confirm": 5,       # C105
    "test_delete_task_cancel": 6         # C106
}

@pytest.fixture
def driver():
    # --- Setup ---
    driver = webdriver.Chrome()
    file_path = os.path.abspath('index.html')
    driver.get('file://' + file_path)
    driver.maximize_window()
    yield driver
    # --- Teardown ---
    driver.quit()

# Test Case: TC_ADD_01
def test_add_task_positive(driver):
    """
    Tests adding a valid task.
    """
    case_id = CASE_IDS["test_add_task_positive"]
    try:
        # Find input, type text, and click add
        task_input = driver.find_element(By.ID, 'taskInput')
        task_input.send_keys('Buy milk')
        add_button = driver.find_element(By.ID, 'addTaskBtn')
        add_button.click()

        # Verification: Wait until the task appears in the list
        wait = WebDriverWait(driver, 10)
        new_task = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Buy milk')]")))
        
        # Assert that the task is displayed
        assert new_task.is_displayed()
        assert "Buy milk" in new_task.text
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise

# Test Case: TC_ADD_03
def test_add_task_negative_empty(driver):
    """
    Tests that an empty task cannot be added and an alert appears.
    """
    case_id = CASE_IDS["test_add_task_negative_empty"]
    try:
        # Find and click the add button without typing anything
        add_button = driver.find_element(By.ID, 'addTaskBtn')
        add_button.click()

        # Verification: Wait for the alert to be present
        wait = WebDriverWait(driver, 10)
        alert = wait.until(EC.alert_is_present())

        # Assert the alert text is correct
        assert alert.text == "Please enter a task."
        
        # Close the alert
        alert.accept()
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise
    
# Test Case: TC_MARK_01
def test_mark_task_complete(driver):
    """
    Tests that a task can be marked as complete.
    """
    case_id = CASE_IDS["test_mark_task_complete"]
    try:
        # First, add a task to work with
        driver.find_element(By.ID, 'taskInput').send_keys('Read a book')
        driver.find_element(By.ID, 'addTaskBtn').click()
        
        # Locate the task and click it to mark as complete
        wait = WebDriverWait(driver, 10)
        task_to_mark = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Read a book')]")))
        task_to_mark.click()
        
        # Verification: Check if the 'completed' class has been added to the element
        assert "completed" in task_to_mark.get_attribute("class")
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise

# Test Case: TC_MARK_02
def test_unmark_task_complete(driver):
    """
    Tests that a completed task can be toggled back to active.
    """
    case_id = CASE_IDS["test_unmark_task_complete"]
    try:
        # Add a task and mark it as complete
        driver.find_element(By.ID, 'taskInput').send_keys('Finish report')
        driver.find_element(By.ID, 'addTaskBtn').click()
        wait = WebDriverWait(driver, 10)
        task_to_unmark = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Finish report')]")))
        task_to_unmark.click() # First click to complete
        
        # Now, click it again to un-mark it
        task_to_unmark.click() # Second click to un-mark
        
        # Verification: Check that the 'completed' class is no longer present
        assert "completed" not in task_to_unmark.get_attribute("class")
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise

# Test Case: TC_DEL_04
def test_delete_task_confirm(driver):
    """
    Tests that a task is deleted when the user confirms the action.
    """
    case_id = CASE_IDS["test_delete_task_confirm"]
    try:
        # Add a task
        driver.find_element(By.ID, 'taskInput').send_keys('Task to delete')
        driver.find_element(By.ID, 'addTaskBtn').click()
        wait = WebDriverWait(driver, 10)
        task_to_delete = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Task to delete')]")))
        
        # Find the delete button WITHIN that task element and click it
        delete_button = task_to_delete.find_element(By.TAG_NAME, 'button')
        delete_button.click()
        
        # Switch to the confirmation alert and accept it
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        
        # Verification: Wait until the task element is no longer present (is stale)
        assert wait.until(EC.staleness_of(task_to_delete))
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise

# Test Case: TC_DEL_05
def test_delete_task_cancel(driver):
    """
    Tests that a task is NOT deleted when the user cancels the action.
    """
    case_id = CASE_IDS["test_delete_task_cancel"]
    try:
        # Add a task
        driver.find_element(By.ID, 'taskInput').send_keys('Task to keep')
        driver.find_element(By.ID, 'addTaskBtn').click()
        wait = WebDriverWait(driver, 10)
        task_to_keep = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Task to keep')]")))
        
        # Click the delete button
        delete_button = task_to_keep.find_element(By.TAG_NAME, 'button')
        delete_button.click()
        
        # Switch to the alert and DISMISS it (click 'Cancel')
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()
        
        # Verification: Assert that the task is still displayed on the page
        assert task_to_keep.is_displayed()
        TR.add_result(case_id, status_id=1, comment="Test passed")
    except Exception as e:
        TR.add_result(case_id, status_id=5, comment=f"Test failed: {e}")
        raise