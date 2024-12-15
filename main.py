import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_members(driver, phone_numbers):
    MAX_RETRIES = 1
    for phone_number in phone_numbers:
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                print(f"Attempting to add {phone_number} (try {retry_count + 1}/{MAX_RETRIES})...")

                # Locate and clear the search bar
                search_bar = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                search_bar.click()
                search_bar.send_keys(Keys.CONTROL + "a")  # Select all text
                search_bar.send_keys(Keys.BACKSPACE)  # Clear the search bar
                search_bar.send_keys(phone_number)  # Enter the phone number

                # Wait for search results or timeout
                try:
                    search_result = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="option"]'))
                    )
                    print(f"Search result found for {phone_number}.")
                except Exception:
                    print(f"No search result for {phone_number}. Skipping.")
                    break

                # Check for a checkable box in the search result
                try:
                    checkable_box = WebDriverWait(search_result, 2).until(
                        EC.presence_of_element_located((By.XPATH, './/input[@type="checkbox"]'))
                    )
                    checkable_box.click()
                    print(f"Checkable box selected for {phone_number}.")
                except Exception:
                    print(f"No checkable box found for {phone_number}. Skipping.")
                    break

                # Move to the next contact
                break  # Success, move to next phone number

            except Exception as e:
                retry_count += 1
                if retry_count == MAX_RETRIES:
                    print(f"Failed to add {phone_number} after {MAX_RETRIES} attempts.")

    # Confirm additions
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="checkmark-light"]'))
        )
        confirm_button.click()
        print("All contacts added successfully.")
    except Exception as e:
        print(f"Failed to confirm additions.")

def group_add(group_name):
    phone_numbers = []

    with open('MOVE Servants.csv', 'rt') as f:
        data = csv.DictReader(f)
        for row in data:
            if row['Phone Number']:
                phone_numbers.append(row['Phone Number'])

    print("Falling back to QR code login.")
    driver = webdriver.Edge()
        
        
    driver.get('https://web.whatsapp.com/')
    driver.maximize_window()
    
    #print("Please scan the QR code to log in to WhatsApp Web.")

    try:
        group_element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@title="{group_name}"]'))
        )
        group_element.click()
    except Exception as e:
        print(f"Error finding the group '{group_name}': {e}")
        driver.quit()
        return

    print("Please manually open the group info menu and click 'Add Participants'.")
    input("Press Enter once ready...")

    add_members(driver, phone_numbers)
    driver.quit()

group_name = input("Enter the name of the WhatsApp group you want to add people to: ")
group_add(group_name)