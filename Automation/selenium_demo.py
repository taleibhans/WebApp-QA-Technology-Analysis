"""
Portfolio QA/Technology Analyst Project
Selenium Automation Script – Stable Version with Comments
Features:
- Uses webdriver-manager to automatically handle ChromeDriver
- Explicit waits for reliable element detection
- Positive & negative login tests
- Screenshot capture for each test
- Pauses at the end to review browser state
Author: Talei Ibhanesebhor
"""

# ---- IMPORTS ----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# ---- CONFIGURATION ----
APP_URL = "https://demoqa.com/login"  # URL of the web application to test
USERNAME = "testuser"                 # Placeholder username for valid login
PASSWORD = "Test@123"                 # Placeholder password for valid login
WAIT_TIME = 10                         # Maximum wait time in seconds for explicit waits
SCREENSHOT_DIR = "screenshots"         # Folder to store screenshots

# Create screenshots folder if it doesn't exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ---- HELPER FUNCTION: Capture Screenshot ----
def capture_screenshot(driver, name):
    """
    Takes a screenshot of the current browser window and saves it with a given name.
    """
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")

# ---- SETUP: Launch Chrome Browser ----
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()                 # Maximize window for consistent screenshots
wait = WebDriverWait(driver, WAIT_TIME) # Explicit wait object for element detection

# ---- TEST 1: VALID LOGIN ----
driver.get(APP_URL)  # Navigate to the login page
try:
    # Enter valid credentials
    driver.find_element(By.ID, "userName").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login").click()

    # Wait for logout button or profile indicator to appear (login success)
    try:
        logout_btn = wait.until(EC.presence_of_element_located((By.ID, "logout")))
        print("✅ Valid Login Test Passed")
        capture_screenshot(driver, "valid_login_pass")
    except:
        # If logout button not found, check for error message
        error_msg = driver.find_element(By.ID, "name").text
        print(f"❌ Valid Login Test Failed | Message: {error_msg}")
        capture_screenshot(driver, "valid_login_fail")
except Exception as e:
    # Handle unexpected errors during valid login test
    print(f"❌ Valid Login Test Error: {e}")
    capture_screenshot(driver, "valid_login_error")

# ---- TEST 2: NEGATIVE LOGIN ----
driver.get(APP_URL)  # Reset to login page
try:
    # Enter invalid credentials
    driver.find_element(By.ID, "userName").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.ID, "login").click()

    # Wait for error message to appear
    try:
        error_msg = wait.until(EC.presence_of_element_located((By.ID, "name"))).text
        if "Invalid" in error_msg:
            print("✅ Negative Login Test Passed")
            capture_screenshot(driver, "invalid_login_pass")
        else:
            print(f"❌ Negative Login Test Failed | Message: {error_msg}")
            capture_screenshot(driver, "invalid_login_fail")
    except:
        # Handle case where error message is missing
        print("❌ Negative Login Test Error: No error message found")
        capture_screenshot(driver, "invalid_login_error")
except Exception as e:
    # Handle unexpected exceptions during negative login test
    print(f"❌ Negative Login Test Exception: {e}")
    capture_screenshot(driver, "negative_login_exception")

# ---- CLEANUP ----
# Pause to allow user to inspect browser before closing
input("Tests completed. Press Enter to close browser...")
driver.quit()

