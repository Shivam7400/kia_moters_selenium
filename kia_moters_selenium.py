import csv, logging, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(filename='kia_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--headless")
service = Service(r'chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.kia.com/in/buy/find-a-dealer.html")
try:
    accept_cookies = driver.find_element(By.XPATH, "//button[@class='btn cookies-button']")
    accept_cookies.click()
    logging.info("Accepted cookies.")
except Exception as e:
    logging.error(f"Error accepting cookies: {e}")
with open('kia_moter_dealers.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Dealer_Name', 'Dealer_Type', 'Dealer_Address', 'City', 'State', 'Mobile', 'Email', 'Domain', 'Map_Location'])
    try:
        WebDriverWait(driver, 5)
        click_state_dropdown = driver.find_element(By.XPATH,"//span[@id='select-state-button']")
        click_state_dropdown.click()    
        state_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-state-menu']")))
        state_options = state_dropdown.find_elements(By.XPATH, "./li")[1:]
        click_state_dropdown.click()    
        i = 1
        for state_index in range(len(state_options)):
            try:
                click_state_dropdown = driver.find_element(By.XPATH,"//span[@id='select-state-button']")
                click_state_dropdown.click()    
                state_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-state-menu']")))
                state_options = state_dropdown.find_elements(By.XPATH, "./li")[1:]
                if state_index >= 5:
                    for _ in range(i):
                        driver.execute_script("arguments[0].scrollTop += 200;", state_dropdown)
                        time.sleep(0.5)
                    state_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-state-menu']")))
                    state_options = state_dropdown.find_elements(By.XPATH, "./li")[1:]

                WebDriverWait(driver, 2)
                current_state_value = state_options[state_index].get_attribute("textContent")
                state_options[state_index].click()
                logging.info(f"Selected state: {current_state_value}")
            except (StaleElementReferenceException, ElementClickInterceptedException):
                logging.warning(f"StaleElementReferenceException or ElementClickInterceptedException caught for state_index {state_index}. Retrying...")
                continue
            except Exception as e:
                logging.error(f"An error occurred selecting state {state_index}: {e}")
                continue

            click_city_dropdown = driver.find_element(By.XPATH,"//span[@id='select-city-button']")
            click_city_dropdown.click()    
            actions = ActionChains(driver)
            actions.move_to_element(click_city_dropdown).perform()
            city_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-city-menu']")))
            city_options = city_dropdown.find_elements(By.XPATH, "./li")[1:]
            click_city_dropdown.click()
            j = 1
            for city_index in range(len(city_options)):
                try:
                    click_city_dropdown = driver.find_element(By.XPATH, "//span[@id='select-city-button']")
                    click_city_dropdown.click()
                    actions = ActionChains(driver)
                    actions.move_to_element(click_city_dropdown).perform()
                    city_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-city-menu']")))
                    city_options = city_dropdown.find_elements(By.XPATH, "./li")[1:]

                    if city_index >= 5:
                        for _ in range(j):
                            driver.execute_script("arguments[0].scrollTop += 200;", city_dropdown)
                            time.sleep(0.5)
                        city_dropdown = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='select-city-menu']")))
                        city_options = city_dropdown.find_elements(By.XPATH, "./li")[1:]

                    WebDriverWait(driver, 2)
                    current_city_value = city_options[city_index].get_attribute("textContent")
                    city_options[city_index].click()
                    logging.info(f"Selected city: {current_city_value}")
                except ElementClickInterceptedException:
                        logging.warning(f"City dropdown click intercepted for city_index {city_index}. Retrying...")
                        time.sleep(2)
                        driver.execute_script("arguments[0].click();", click_city_dropdown)
                except StaleElementReferenceException:
                    logging.warning(f"StaleElementReferenceException caught for city_index {city_index}. Retrying...")
                    continue
                except Exception as e:
                    logging.error(f"An error occurred selecting city {city_index}: {e}")
                    continue
                search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                search_button.click()
                dealer_all_cards = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class,'dealer-list mt-sm  mb-sm')]")))
                dealer_cards = dealer_all_cards.find_elements(By.XPATH, "./li")[0:]
                for card in dealer_cards:
                    WebDriverWait(driver, 2)
                    dealer_name = card.find_element(By.XPATH, ".//div[@class='h7 dealer-name']").text
                    dealer_type = card.find_element(By.XPATH, ".//span[contains(@class,'dealer-category')]").text
                    dealer_address = card.find_element(By.XPATH, ".//div[@class='dealer-address']").text
                    dealer_contact = card.find_element(By.XPATH, ".//ul[@class='dealer-contacts']")
                    try:
                        mobile_element = dealer_contact.find_element(By.XPATH, "./li[@class='tel']/a")
                        mobile = mobile_element.text if mobile_element else None
                    except NoSuchElementException:
                        mobile = None
                        logging.info(f"Mobile number not present for {dealer_name} in {current_city_value}")
                    try:
                        email_element = dealer_contact.find_element(By.XPATH, "./li[@class='email']/a")
                        email = email_element.text if email_element else None
                    except NoSuchElementException:
                        email = None
                        logging.info(f"Email not present for {dealer_name} in {current_city_value}")
                    try:
                        domain_element = dealer_contact.find_element(By.XPATH, "./li[@class='domain']/a")
                        domain = domain_element.text if domain_element else None
                    except NoSuchElementException:
                        domain = None
                        logging.info(f"Domain not present for {dealer_name} in {current_city_value}")
                    map_location = dealer_contact.find_element(By.XPATH, "./li[@class='get']/a").get_attribute("href")
                    logging.info(f"Dealer found: {dealer_name}, {dealer_type}, {current_city_value}, {mobile}, {email}, {domain}, {map_location}")
                    writer.writerow([dealer_name, dealer_type, dealer_address, current_city_value, current_state_value, mobile, email, domain, map_location])
                if city_index in [10, 15, 20, 25, 30]:
                    j += 1
                driver.back()
                time.sleep(1)
            if state_index in [9, 15, 21, 25, 30]:
                i += 1
    finally:
        time.sleep(5)
        driver.quit()
        logging.info("Script finished, browser closed.")