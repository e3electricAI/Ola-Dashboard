from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re  # For regex to extract the showroom count

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("https://www.bikewale.com/dealer-showrooms/ola/")

wait = WebDriverWait(driver, 10)

# Wait for the main list to load
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'o-eCFISO')))

# Expand all state dropdowns
state_dropdowns = driver.find_elements(By.CLASS_NAME, 'o-dbKqqe')

# Create CSV to save data
with open('ola_dealers_with_showroom_count.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'City', 'Number of Showrooms', 'Dealer URL'])

    for state in state_dropdowns:
        try:
            # Extract state name
            state_name = state.find_element(By.TAG_NAME, 'p').text
            print(f"Expanding: {state_name}")
            
            # Expand the dropdown
            state.click()
            time.sleep(1)  # Allow dropdown to expand

            # Scrape city links under each state
            city_links = state.find_elements(By.CLASS_NAME, 'o-bkmzIL')
            
            for city in city_links:
                city_text = city.text
                city_url = city.get_attribute('href')
                print(f"Found {city_text}: {city_url}")

                # Extract city name and number of showrooms using regex
                match = re.match(r"(.*)\s\((\d+)\)", city_text)
                if match:
                    city_name = match.group(1)
                    showroom_count = match.group(2)
                else:
                    city_name = city_text
                    showroom_count = 'N/A'  # If no match, set showroom count as 'N/A'

                # Write the data to the CSV file
                writer.writerow([state_name, city_name, showroom_count, city_url])

        except Exception as e:
            print(f"Error with {state.text}: {str(e)}")

driver.quit()
