from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os

class OpenEMRWorkflow:
    def __init__(self):
        # Set up Chrome options
        options = Options()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        # Open Chrome browser
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
        # Initialize the flag as False
        self.provider_selected = False
        self.drug_selected = False
        self.namep1_entered = False
        self.quantity_selected = False

    def open_site(self):
        # Open openEMR demo
        self.driver.get('https://demo.openemr.io/a/openemr/interface/login/login.php?site=default')

    def login(self):
        # Login
        self.wait.until(EC.presence_of_element_located((By.ID, 'authUser'))).send_keys('physician')
        self.wait.until(EC.presence_of_element_located((By.ID, 'clearPass'))).send_keys('physician')
        self.wait.until(EC.presence_of_element_located((By.ID, 'login-button'))).click()

    def click_finder(self):
        # Click on [Finder]
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainMenu"]/div/div[2]/div'))).click()

    def click_patient1(self):
        # Click on the first patient
        iframe = self.wait.until(EC.presence_of_element_located((By.NAME, 'fin')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pid_1"]/td[1]/a'))).click()
        self.driver.switch_to.default_content()

    def click_prescription_page(self):
        # Enter "enter prescription page"
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div/div[4]/iframe')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/section[5]/div/h6/span/a'))).click()
        self.driver.switch_to.default_content()

    def click_add_prescription(self):
        # Click on [Add]
        self.wait.until(EC.element_to_be_clickable((By.ID, 'addButton'))).click()

    def change_starting_date(self):
        # Does not include changing start date
        # To-do
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="start_date"]'))).click()
        self.driver.switch_to.default_content()

    def click_provider(self):
        # Select provider: Billy Smith
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[4]/select')))
        dropdown.click()
        self.driver.switch_to.default_content()
        self.provider_selected = True  # Set the flag to True when this method is called

    def select_billy(self):
        try:
            if not self.provider_selected:  # If the flag is still False when this method is called, raise an error
                raise Exception('Not able to select provider. Missing click_provider.')
            # Select provider: Billy Smith
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
            self.driver.switch_to.frame(iframe)
            dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[4]/select')))
            select = Select(dropdown)
            select.select_by_visible_text('Billy Smith')
            self.driver.switch_to.default_content()
            self.provider_selected = False # Reset back to false
        except Exception as e:
            print(str(e))

    '''def click_search_web(self):
        # Not working right now
        # Todo
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="druglookup"]')))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()  # This should scroll the page until the element is in view
        element.click()
        self.driver.switch_to.default_content()
    '''

    def click_drug(self):
        # Click on drug

        #click_drug, enter_drug_namep1, enter_drug_namep2: No error
        #click_drug, enter_drug_namep1: Applicable, but error
        #click_drug, enter_drug_namep2: Not applicable
        #enter_drug_namep1, enter_drug_namep2: Not applicable
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[5]/span/span[1]/span/span[2]'))).click()
        self.driver.switch_to.default_content()
        self.drug_selected = True

    def enter_drug_namep1(self):
        try:
            if not self.drug_selected:  # If the flag is still False when this method is called, raise an error
                raise Exception('Not able to enter drug name. Missing click_drug.')
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
            self.driver.switch_to.frame(iframe)
            textbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input')))
            textbox.click()
            textbox.send_keys('advi')
            self.driver.switch_to.default_content()
            self.drug_selected = False
            self.namep1_entered = True
        except Exception as e:
            print(str(e))

    def enter_drug_namep2(self):
        try:
            if not self.namep1_entered:
                raise Exception('Not applicable. Missing enter_drug_namep1.')
                if self.drug_selected:  # If the flag is still False when this method is called, raise an error
                    raise Exception('Not able to enter drug name. Missing click_drug.')
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
            self.driver.switch_to.frame(iframe)
            textbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input')))
            textbox.send_keys('l')
            # Close the form
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[2]/ul/li'))).click()
            self.driver.switch_to.default_content()
            self.drug_selected = False
            self.namep1_entered = False
        except Exception as e:
            print(str(e))

    def click_quantity(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        qBox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quantity"]')))
        qBox.click()
        self.driver.switch_to.default_content()
        self.quantity_selected = True

    def enter_quantity(self):
        try:
            if not self.quantity_selected:  # If the flag is still False when this method is called, raise an error
                raise Exception('Error: Not able to enter quantity. Missing click_quantity.')
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
            self.driver.switch_to.frame(iframe)
            qBox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quantity"]')))
            qBox.send_keys('100')
            self.driver.switch_to.default_content()
            self.quantity_selected = False
        except Exception as e:
            print(str(e))

    def enter_medicine_num(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        mBox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="size"]')))
        mBox.send_keys('5')
        self.driver.switch_to.default_content()

    def choose_medicine_unit(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="unit"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[7]/div[3]/select/option[3]'))).click()
        self.driver.switch_to.default_content()

    def enter_direction_num(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        dBox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dosage"]')))
        dBox.send_keys('1')
        self.driver.switch_to.default_content()

    def choose_direction_s1(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[8]/div[4]/select/option[3]'))).click()
        self.driver.switch_to.default_content()

    def choose_direction_s2(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="route"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[8]/div[5]/select/option[3]'))).click()
        self.driver.switch_to.default_content()

    def choose_direction_s3(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="interval"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[8]/div[6]/select/option[6]'))).click()
        self.driver.switch_to.default_content()

    def choose_refill_num1(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[9]/div[2]/select'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[9]/div[2]/select/option[21]'))).click()
        self.driver.switch_to.default_content()

    def add_to_medicine(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div[11]/div[2]/label[2]/input'))).click()
        self.driver.switch_to.default_content()

    # Todo: substitution allowed?

    def save(self):
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalframe"]')))
        self.driver.switch_to.frame(iframe)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save"]'))).click()
        self.driver.switch_to.default_content()

    def run_setup(self):
        # Call this function to setup
        self.open_site()
        self.login()
        self.click_finder()
        self.click_patient1()
        self.click_prescription_page()
        self.click_add_prescription()

    def run_workflow(self, workflow):
        workflow = OpenEMRWorkflow()
        workflow.run_setup()
        # Call deviated workflows
        for action in workflow:
            # Remove any leading/trailing whitespace
            action = action.strip()
            # Check if the method exists
            if hasattr(self, action):
                # If it does, call it
                getattr(self, action)()  # note: add () to call the function
            else:
                print(f"No such method: {action}")

#workflow = OpenEMRWorkflow()
#workflow.run_setup()
# correct workflow:
# 16 actions
# click_provider;select_billy;click_drug;enter_drug_namep1;enter_drug_namep2;click_quantity;enter_quantity;enter_medicine_num;choose_medicine_unit;enter_direction_num;choose_direction_s1;choose_direction_s2;choose_direction_s3;choose_refill_num1;add_to_medicine;save
'''workflow.run_workflow([
    'click_provider',
    'select_billy',
    'click_drug',
    'enter_drug_namep1',
    'enter_drug_namep2',
    'click_quantity',
    'enter_quantity',
    'enter_medicine_num',
    'choose_medicine_unit',
    'enter_direction_num',
    'choose_direction_s1',
    'choose_direction_s2',
    'choose_direction_s3',
    'choose_refill_num1',
    'add_to_medicine',
    'save'
])'''
# Example: Omission1[2]
#workflow.run_workflow(['click_provider', 'click_drug', 'enter_drug_namep1', 'enter_drug_namep2', 'click_quantity', 'enter_quantity', 'enter_medicine_num', 'choose_medicine_unit', 'enter_direction_num', 'choose_direction_s1', 'choose_direction_s2', 'choose_direction_s3', 'choose_refill_num1', 'add_to_medicine', 'save'])