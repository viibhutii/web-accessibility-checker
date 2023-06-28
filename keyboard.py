import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

def check_keyboard_accessibility(label, url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Launch the browser using Selenium WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the webpage you are testing
    driver.get(url)

    # Wait for the body element to be present
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Simulate keyboard interaction by pressing the Tab key
    body.send_keys(Keys.TAB)

    # Check if the focus has changed after pressing Tab
    active_element = driver.switch_to.active_element
    if active_element:
        label.config(text="Keyboard accessibility is enabled.", fg='green', font=("Arial", 16))
    else:
        label.config(text="Keyboard accessibility is disabled.", fg='red', font=("Arial", 16))

    # Close the browser
    driver.quit()

# Create the UI window
window = tk.Tk()

# Set the dimensions of the window (width x height)
window.geometry("800x150")
window.title("Keyboard Accessibility Checker")

# Create a label to display the result
result_label = tk.Label(window, text="Enter a URL and click the button to check keyboard accessibility:", font=("Arial", 14))
result_label.pack(pady=10)

# Create an entry field to input the URL
url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=5)

# Create a button to trigger the accessibility check
def perform_accessibility_check():
    url = url_entry.get()
    if is_valid_url(url):
        check_keyboard_accessibility(result_label, url)
    else:
        result_label.config(text="Invalid URL. Please enter a valid URL.", fg='red')

check_button = tk.Button(window, text="Check Accessibility", command=perform_accessibility_check)
check_button.pack(pady=5)

# Run the UI event loop
window.mainloop()






