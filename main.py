import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

def add_members(driver, phone_numbers):
    for phone_number in phone_numbers:
        try:
            print(f"Adding {phone_number} to the group...")
            # Locate the search bar in the "Add member" interface
            search_bar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Search name or number"]'))
            )
            
            # Clear the search bar (if there's leftover text) and type the phone number
            search_bar.clear()
            search_bar.send_keys(phone_number)
            time.sleep(3)  # Wait for search results to load

            # Check if the contact exists in the search results
            try:
                # Locate the search result for the contact
                contact = driver.find_element(By.XPATH, f'//span[contains(text(), "{phone_number}")]')
                
                # Check if the contact is already added to the group
                already_added = driver.find_elements(By.XPATH, '//span[text()="Already added to group"]')
                if already_added:
                    print(f"Contact {phone_number} is already in the group. Skipping.")
                    continue
                
                # If not already added, click the checkbox to select the contact
                contact.click()
                print(f"Selected contact {phone_number} for addition.")
            except Exception:
                print(f"Contact {phone_number} not found. Skipping.")
                continue

        except Exception as e:
            print(f"Error while adding {phone_number}: {e}")
            continue

    # Click the checkmark to confirm adding members
    try:
        confirm_button = driver.find_element(By.XPATH, '//span[@data-icon="checkmark-light"]')
        confirm_button.click()
        print("Confirmed addition of all selected members.")
    except Exception as e:
        print("Failed to confirm member addition:", e)

def group_add(group_name):
    phone_numbers = []

    # Read phone numbers from the CSV file
    with open('MOVE Servants.csv', 'rt') as f:
        data = csv.DictReader(f)  # Use DictReader to handle column headers
        for row in data:
            if row['Phone Number']:  # Ensure the phone number column exists
                phone_numbers.append(row['Phone Number'])  # Append phone numbers to the list

    # Launch Edge browser and open WhatsApp Web
    
    try: 
        from config import WEBDRIVER_PATH, USER_DATA_DIR, PROFILE
        #Configure Edge WebDriver
        options = webdriver.EdgeOptions()
        options.add_argument(f"user-data-dir={USER_DATA_DIR}")
        options.add_argument(f"profile-directory={PROFILE}")
        
        # Launch Edge browser using WebDriver path and options
        driver = webdriver.Edge(service=Service(WEBDRIVER_PATH), options=options)
        print("Using persistent WebDriver configuration.")
    except Exception as e:
        USER_DATA_DIR = None
        PROFILE = None
        print(f"WebDriver configuration failed: {e}")
        print("Falling back to QR code login.")
        
        # Launch Edge without persistent configuration
        driver = webdriver.Edge()

    driver.maximize_window()
    driver.get('https://web.whatsapp.com/')
    print("Please scan the QR code to log in to WhatsApp Web.")
    #time.sleep(20)  # Wait for the user to log in

    # Search for the group
    try:
        group_element = driver.find_element(By.XPATH, f'//*[@title="{group_name}"]')
        group_element.click()
    except Exception as e:
        print("WhatsApp group doesn't exist. Please check the group name.")
        driver.quit()
        return

    # Open group info menu manually
    print("Please manually open the group info menu.")
    input("Press Enter once you have clicked \"Add Participants\" button ...")

    # Add members to the group
    add_members(driver, phone_numbers)

    # Close the browser
    driver.quit()

# Get group name from the user
group_name = input("Enter the name of the WhatsApp group you want to add people to: ")
group_add(group_name)
