from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load credentials from .env file
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Set up WebDriver correctly
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser maximized

# Use Service() with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def linkedin_login():
    """Logs into LinkedIn."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    # Enter email
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(LINKEDIN_EMAIL)

    # Enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(LINKEDIN_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

def post_on_linkedin(content):
    """Automates posting on LinkedIn."""
    driver.get("https://www.linkedin.com/feed/")

    # Wait for the 'Start a post' button and click it
    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start a post')]"))
        )
        post_button.click()
    except Exception as e:
        print("❌ Error: Could not find the 'Start a Post' button.", e)
        return

    time.sleep(2)

    # Locate the text input area
    try:
        post_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor.ql-blank"))
        )
        driver.execute_script("arguments[0].innerHTML = arguments[1]", post_textarea, content)
        time.sleep(1)
    except Exception as e:
        print("❌ Error: Could not find the post text area.", e)
        return

    time.sleep(2)

    # Locate and click the 'Post' button inside the pop-up
    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Post']/parent::button"))
        )
        post_button.click()
        print("✅ Post successfully made on LinkedIn!")
    except Exception as e:
        print("❌ Error: Could not find the 'Post' button.", e)



if __name__ == "__main__":
    linkedin_login()
    post_content = "🚀 Excited to launch my LinkedIn automation project! #Automation #LinkedIn"
    post_on_linkedin(post_content)
    time.sleep(5)
    driver.quit()
