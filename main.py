import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def group_add(group_name):
    phone_numbers = []

    # Read phone numbers from the CSV file
    with open('Samples/people.csv', 'rt') as f:
        data = csv.DictReader(f)  # Use DictReader to handle column headers
        for row in data:
            if row['Phone Number']:  # Ensure the phone number column exists
                phone_numbers.append(row['Phone Number'])  # Append phone numbers to the list

    # Launch browser and open WhatsApp Web
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://web.whatsapp.com/')
    print("Please scan the QR code to log in to WhatsApp Web.")
    time.sleep(20)  # Wait for the user to log in

    # Search for the group
    try:
        group_element = driver.find_element(By.XPATH, f'//*[@title="{group_name}"]')
        group_element.click()
    except Exception as e:
        print("WhatsApp group doesn't exist. Please check the group name.")
        driver.quit()
        return

    # Open group info menu
    try:
        menu_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="_3V5x5"]'))
        )
        menu_button.click()

        add_participants_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="_3p0T6"]'))
        )
        add_participants_button.click()
    except Exception as e:
        print("Unable to access the group menu. Please try again.")
        driver.quit()
        return

    # Add participants by phone number
    for phone_number in phone_numbers:
        try:
            search_field = driver.find_element(By.XPATH, '//*[@title="Search…"]')
            search_field.send_keys(phone_number)  # Input the phone number
            time.sleep(5)  # Wait for the search results

            # Click on the contact if it appears
            contact_element = driver.find_element(By.XPATH, f'//*[@title="{phone_number}"]')
            contact_element.click()
        except Exception as e:
            print(f"Phone number {phone_number} not found or cannot be added.")
            continue

    # Confirm and save the changes
    try:
        confirm_button = driver.find_element(By.XPATH, '//*[@data-icon="checkmark-light"]')
        confirm_button.click()
        print("Participants added successfully.")
    except Exception as e:
        print("Failed to confirm the additions.")

    # Close the browser
    driver.quit()

# Get group name from the user
group_name = input("Enter the name of the WhatsApp group you want to add people to: ")
group_add(group_name)
