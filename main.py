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

def add_members_re_re(driver, phone_numbers):
    MAX_RETRIES = 3
    for phone_number in phone_numbers:
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                print(f"Attempting to add {phone_number} (try {retry_count+1}/{MAX_RETRIES})...")

                # Locate and clear the search bar
                search_bar = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                search_bar.click()
                search_bar.send_keys(Keys.CONTROL + "a")
                search_bar.send_keys(Keys.BACKSPACE)
                search_bar.send_keys(phone_number)

                # Wait for search results
                search_result = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="option"]'))
                )

                # Check for "Already added" status
                already_added = search_result.find_elements(By.XPATH, './/span[contains(text(), "already added")]')
                if already_added:
                    print(f"Contact {phone_number} is already in the group. Skipping.")
                    break

                # Click the contact to add
                search_result.click()
                print(f"Selected contact {phone_number}.")
                break  # Success, move to next phone number

            except Exception as e:
                retry_count += 1
                if retry_count == MAX_RETRIES:
                    print(f"Failed to add {phone_number} after {MAX_RETRIES} attempts: {e}")

    # Confirm additions
    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="checkmark-light"]'))
        )
        confirm_button.click()
        print("All contacts added successfully.")
    except Exception as e:
        print(f"Failed to confirm additions: {e}")


def add_members(driver, phone_numbers):
    for phone_number in phone_numbers:
        try:
            print(f"Adding {phone_number} to the group...")
            search_bar = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
            search_bar.clear()
            search_bar.send_keys(phone_number)
            time.sleep(10)  # Wait for search results

            try:
                contact = driver.find_element(By.XPATH, f'//span[contains(text(), "{phone_number}")]')
                already_added = driver.find_elements(By.XPATH, '//span[text()="Already added to group"]')
                if already_added:
                    print(f"Contact {phone_number} is already in the group. Skipping.")
                    continue
                contact.click()
                print(f"Selected contact {phone_number}.")
            except Exception:
                print(f"Contact {phone_number} not found. Skipping.")
                continue
        except Exception as e:
            print(f"Error adding {phone_number}: {e}")
            continue

    try:
        confirm_button = driver.find_element(By.XPATH, '//span[@data-icon="checkmark-light"]')
        confirm_button.click()
        print("All members added.")
    except Exception as e:
        print(f"Failed to confirm member addition: {e}")

def add_members_re(driver, phone_numbers):
    for phone_number in phone_numbers:
        try:
            print(f"Adding {phone_number} to the group...")
            search_bar = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            # Clear the search bar
            search_bar.click()  # Focus on the search bar
            search_bar.send_keys(Keys.CONTROL + "a")  # Select all text
            search_bar.send_keys(Keys.BACKSPACE)      # Clear using backspace
            search_bar.send_keys(phone_number)
            
            # Wait for the search results
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="option"]'))
            )
            
            try:
                # Locate and click the contact
                contact = driver.find_element(By.XPATH, f'//div[contains(@class, "matched-text") and contains(text(), "{phone_number}")]')
                already_added = driver.find_elements(By.XPATH, '//span[contains(text(), "already added")]')
                
                if already_added:
                    print(f"Contact {phone_number} is already in the group. Skipping.")
                    continue
                
                contact.click()
                print(f"Selected contact {phone_number}.")
            except Exception:
                print(f"Contact {phone_number} not found. Skipping.")
                continue
        except Exception as e:
            print(f"Error adding {phone_number}: {e}")
            continue

    # Confirm additions
    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="checkmark-light"]'))
        )
        confirm_button.click()
        print("All members added.")
    except Exception as e:
        print(f"Failed to confirm member addition: {e}")

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

    add_members_re_re(driver, phone_numbers)
    driver.quit()

group_name = input("Enter the name of the WhatsApp group you want to add people to: ")
group_add(group_name)
