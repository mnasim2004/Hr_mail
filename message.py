from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in PATH

# Log in to LinkedIn
driver.get("https://www.linkedin.com/login")

# Log in
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys("mohammednasim2004@gmail.com")
password.send_keys("Mnasim@23104")
password.send_keys(Keys.RETURN)

# Wait for the home page to load and confirm login
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "global-nav__me")))
    print("Login successful.")
except Exception as e:
    print("Login failed.")
    print(e)
    driver.quit()
    exit()
# List of profile URLs
profile_urls = [
    "https://www.linkedin.com/in/amar-khan-4387a2260/",
    # Add more URLs as needed
]

# Message to send
message = "Hello, this is a custom message."

for url in profile_urls:
    print(f"Navigating to {url}...")
    driver.get(url)
    
    try:
        # Click on the message button
        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "message-anywhere-button"))
        )
        message_button.click()

        # Wait for the message modal to open and the message box to be visible
        message_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "msg-form__contenteditable"))
        )

        # Clear existing text and type new message
        # message_box.clear()
        message_box.send_keys(message)

        # Press Enter to send the message
        message_box.send_keys(Keys.RETURN)

        # Wait a bit to ensure the message is sent
        time.sleep(5)
        print(f"Message sent to {url}")

    except Exception as e:
        print(f"Error sending message to {url}: {e}")

driver.quit()
