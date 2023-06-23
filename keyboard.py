from tkinter import Tk, Label, Button
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def check_keyboard_accessibility(label):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Launch the browser using Selenium WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # ScreenSteps URL
    url = "https://snhu.screenstepslive.com/a/1137941-you-attend-blocked"

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
window = Tk()

# Set the dimensions of the window (width x height)
window.geometry("400x150")
window.title("Keyboard Accessibility Checker")

# Create a button to trigger the accessibility check
check_button = Button(window, text="Check Accessibility", command=lambda: check_keyboard_accessibility(result_label))
check_button.pack(pady=10)

# Create a label to display the result
result_label = Label(window, text="Click the button to check keyboard accessibility.", font=("Arial", 12))
result_label.pack(pady=10)


# Run the UI event loop
window.mainloop()







