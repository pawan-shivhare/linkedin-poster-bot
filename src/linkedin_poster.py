import os
import time
import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_post(topic, tone="Professional", word_limit=200):
    """Generates a LinkedIn post using GPT-3.5 Turbo."""
    prompt = f"""
    Write a LinkedIn post about "{topic}" in a {tone} tone.
    - Keep it engaging and insightful.
    - Use bullet points if necessary.
    - Add a compelling call-to-action at the end.
    - Stay within {word_limit} words.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating AI post: {e}")
        return None



def linkedin_login():
    """Logs into LinkedIn."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    try:
        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(LINKEDIN_EMAIL)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(LINKEDIN_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login
    except Exception as e:
        print("❌ Error during login:", e)
        driver.quit()

def post_on_linkedin(content):
    """Automates posting on LinkedIn."""
    driver.get("https://www.linkedin.com/feed/")
    
    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start a post')]"))
        )
        post_button.click()
    except Exception as e:
        print("❌ Error: Could not find 'Start a Post' button.", e)
        return

    time.sleep(2)

    try:
        post_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
        )
        driver.execute_script("arguments[0].innerHTML = arguments[1]", post_textarea, content)
        time.sleep(1)
    except Exception as e:
        print("❌ Error: Could not find the post text area.", e)
        return

    time.sleep(2)

    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Post']/parent::button"))
        )
        post_button.click()
        print("✅ Post successfully made on LinkedIn!")
    except Exception as e:
        print("❌ Error: Could not find the 'Post' button.", e)

if __name__ == "__main__":
    topic = input("Enter the topic for your LinkedIn post: ")
    generated_post = generate_post(topic)


    if generated_post:
        print("\n📝 AI-Generated LinkedIn Post:\n")
        print(generated_post)
        
        confirm = input("\nDo you want to post this on LinkedIn? (yes/no): ").strip().lower()
        if confirm == "yes":

            # Selenium setup
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--headless=new")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            linkedin_login()
            post_on_linkedin(generated_post)
        else:
            print("❌ Post cancelled.")

    driver.quit()
