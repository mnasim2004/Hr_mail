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
    "https://in.linkedin.com/in/vinita-gupta-394492ab",
    # Add more URLs as needed
]

# Optional connection note
connection_note = "Hello, I'd like to connect with you!"

for url in profile_urls:
    print(f"Navigating to {url}...")
    driver.get(url)
    
    try:
        # Click on the "Connect" button
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pv-s-profile-actions--connect"))
        )
        connect_button.click()

        # Wait for the connection request dialog to open
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "send-invite__actions"))
        )

        # Click on "Add a note" if it's available
        try:
            add_note_button = driver.find_element(By.CLASS_NAME, "send-invite__custom-message")
            add_note_button.click()

            # Wait for the note text area to be visible
            note_text_area = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "send-invite__custom-message-textarea"))
            )
            note_text_area.send_keys(connection_note)
        except Exception:
            pass  # No option to add a note

        # Click "Send now" to send the connection request
        send_button = driver.find_element(By.CLASS_NAME, "send-invite__actions-btn")
        send_button.click()

        # Wait a bit to ensure the connection request is sent
        time.sleep(5)
        print(f"Connection request sent to {url}")

    except Exception as e:
        print(f"Error sending connection request to {url}: {e}")

driver.quit()
