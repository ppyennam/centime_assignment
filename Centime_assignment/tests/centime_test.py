import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import pytest

class TestAssignment:
    @pytest.fixture()
    def setup(self):
        self.service = Service(r"C:/Users/JOSHMITHA/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        # creating driver object
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        # Navigating to required webpage
        self.driver.get("https://practice.automationtesting.in/")
        self.driver.maximize_window()
        # waiting implicitly to load webpage properly
        self.driver.implicitly_wait(5)

        # reading external txt file and assigning parameters required using text file data
        with open('C:/Users/JOSHMITHA/Documents/Centime_assignment/tests/input.txt', 'r') as credentials_file:
            credentials_info = credentials_file.read().splitlines()
        for element in credentials_info:
            if 'new_registration' in element:
                self.new_registration = element.split(':')[1]
            if 'email' in element:
                self.email = element.split(':')[1]
            if 'username' in element:
                self.username = element.split(':')[1]
            if 'password' in element:
                self.password = element.split(':')[1]
            if 'new_password' in element:
                self.new_password = element.split(':')[1]
            if 'add_product_type' in element:
                self.add_product_type = element.split(':')[1]
            if 'add_product_by_search' in element:
                self.add_product_by_search = element.split(':')[1].split(',')
            if 'del_products' in element:
                self.del_product = element.split(':')[1]
            if 'del_product_by_number' in element:
                self.del_product_by_number = element.split(':')[1].split(',')
            if 'first_name' in element:
                self.first_name = element.split(':')[1]
            if 'last_name' in element:
                self.last_name = element.split(':')[1]
            if 'phone_number' in element:
                self.phone_number = element.split(':')[1]
            if 'street_address' in element:
                self.street_address = element.split(':')[1]
            if 'apartment' in element:
                self.apartment = element.split(':')[1]
            if 'city' in element:
                self.city = element.split(':')[1]
            if 'postal_code' in element:
                self.postal_code = element.split(':')[1]
            if 'validate_address' in element:
                self.validate_address = element.split(':')[1]

        #using yield to execute after every testcase
        yield
        #logging out after every testcase
        try:
            self.driver.find_element(By.XPATH, "//a[contains(text(), 'My Account')]").click()
            self.driver.find_element(By.XPATH, "//a[text()='Logout']").click()
        except:
            pass
        # closing webdriver
        self.driver.close()

    def test_registration(self,setup):
        if self.new_registration:
            #Navigating to login page
            self.driver.find_element(By.XPATH, "//a[contains(text(), 'My Account')]").click()
            # finding username element and giving username to username element
            email_ele = self.driver.find_element(By.XPATH, '//input[@id="reg_email"]')
            email_ele.send_keys(self.email)

            # finding password element and giving password to password element
            password_ele = self.driver.find_element(By.XPATH, '//input[@id="reg_password"]')
            password_ele.send_keys(self.password)

            try:
                # collecting text to assert error if password is weak
                weak_pwd_element = self.driver.find_element(By.XPATH, '//small[@class="woocommerce-password-hint"]').text
            except:
                weak_pwd_element = ''
            if weak_pwd_element:
                raise AssertionError(weak_pwd_element)

            # clicking on register button
            self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

            # assert error if account already exists
            try:
                register_error_element = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Error:')]/ancestor::li").text
            except:
                register_error_element = ''
            if register_error_element:
                raise AssertionError(register_error_element)

            if self.driver.find_element(By.XPATH, '//div[@class="woocommerce-MyAccount-content"]'):
                print("registration successful")
    def test_login(self,setup):
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'My Account')]").click()
        if self.password:
            # finding username element and giving username to username element
            username_ele = self.driver.find_element(By.XPATH,'//input[@id="username"]')
            username_ele.send_keys(self.email)

            # finding password element and giving password to password element
            password_ele = self.driver.find_element(By.XPATH,'//input[@id="password"]')
            password_ele.send_keys(self.password)

            self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

            # assert error if password or username incorrect
            try:
                login_error_element = self.driver.find_element(By.XPATH, "// strong[contains(text(), 'Error:')]/ancestor::li").text
            except:
                login_error_element = ''
            if login_error_element:
                raise AssertionError(login_error_element)

            if self.driver.find_element(By.XPATH, '//div[@class="woocommerce-MyAccount-content"]'):
                print('Login Successful')

        else:
            # resetting password if password field is not provides
            self.driver.find_element(By.XPATH, "//a[contains(text(),'Lost your password?')]").click()
            pwd_reset_ele = self.driver.find_element(By.XPATH, '//input[@name="user_login"]')
            pwd_reset_ele.send_keys(self.email)
            self.driver.find_element(By.XPATH, '//input[@value="Reset Password"]').click()
            if self.driver.find_element(By.XPATH, '//div[@class="woocommerce"]'):
                printing_text = self.driver.find_element(By.XPATH, '//div[@class="woocommerce"]/p').text
                # asserting error as password is not present in given data
                raise AssertionError(printing_text)

    def test_adding_products_to_cart_by_product_type(self, setup):
        # logging in to account
        self.test_login(setup)
        self.driver.find_element(By.XPATH, "// a[contains(text(), 'Shop')]").click()
        # collecting web elements of product types
        product_type_list = self.driver.find_elements(By.XPATH, '//*[@id="woocommerce_product_categories-2"]/ul/li/a')
        for product in product_type_list:
            try:
                if self.add_product_type == product.text:
                    product.click()
                    # Adding products of same type to cart
                    web_elements = self.driver.find_elements(By.XPATH, '//*[@id="content"]/ul/li/a[@rel="nofollow"]')
                    for ele in web_elements:
                        ele.click()
                    # displaying products of same type which we added to cart
                    for ele in web_elements:
                        text1 = ele.find_element(By.XPATH, 'ancestor::li/a/img').get_attribute('title')
                        print('%s was added to cart' % text1)

            except StaleElementReferenceException:
                continue

    def test_adding_products_to_cart_by_search_product_and_quantity(self, setup):
        # logging in to account
        self.test_login(setup)
        self.driver.find_element(By.XPATH, "// a[contains(text(), 'Shop')]").click()
        item_quantity = int(self.add_product_by_search[1])
        while item_quantity > 0:
            # Trying to find web element of product we wish and asserting error if not able to find it
            try:
                ele = self.driver.find_element(By.XPATH, "//h3[text()='%s']/ancestor::li/a[@rel='nofollow']" % self.add_product_by_search[0])
            except:
                raise AssertionError('Product is not available in store')
            if ele:
                self.driver.find_element(By.XPATH, "//h3[text()='%s']/ancestor::li/a[@rel='nofollow']" % self.add_product_by_search[0]).click()
            item_quantity = item_quantity-1
        print('product %s is added %s times to the cart' % (self.add_product_by_search[0], self.add_product_by_search[1]))

    def test_decreasing_product_quantity_from_cart(self, setup):

        count = 0
        # logging in to account
        self.test_login(setup)
        self.driver.find_element(By.XPATH, '//*[@id="wpmenucartli"]/a').click()
        # collecting all web elements of cart products
        selected_product_list = self.driver.find_elements(By.XPATH, '//td[@class="product-name"]/a')
        for pro in selected_product_list:
            if pro.text == self.del_product_by_number[0]:
                product_size_to_remove = int(self.del_product_by_number[1])
                input_ele = self.driver.find_element(By.XPATH, '//a[text()="%s"]/ancestor::tr[@class="cart_item"]//div[@class="quantity"]/input[@type="number"]' % self.del_product_by_number[0])
                product_size_in_cart = int(input_ele.get_attribute('value'))
                # Calculating product size after removing required number of products
                expected_product_size = product_size_in_cart-product_size_to_remove
                if expected_product_size > 0:
                    # Removing old quantity of product
                    input_ele.clear()
                    # updating new quantity of product in cart
                    input_ele.send_keys(expected_product_size)
                    self.driver.find_element(By.XPATH, '//input[@value = "Update Basket"]').click()
                    print('now product %s size is %s'%(self.del_product_by_number[0],expected_product_size))
                    count = count + 1
                else:
                    raise AssertionError('product size in the card is less than product size to remove')
        # Asserting error if product is not present in cart
        if count == 0:
            raise AssertionError('product %s was not present in cart' % self.del_product_by_number[0])

    def test_removing_products_from_cart(self, setup):

        count1 = 0
        # logging in to account
        self.test_login(setup)
        self.driver.find_element(By.XPATH, '//*[@id="wpmenucartli"]/a').click()
        # collecting all web elements of cart products
        selected_product_list = self.driver.find_elements(By.XPATH, '//td[@class="product-name"]/a')
        for pro in selected_product_list:
            if pro.text == self.del_product:
                # finding web element to remove product from cart
                pro.find_element(By.XPATH, "//a[text()='%s']/ancestor::tr[@class='cart_item']/td[@class='product-remove']/a" % pro.text).click()
                print('product %s was removed from cart'% pro.text)
                count1 = count1+1
        # Asserting error if product is not present in cart
        if count1 == 0:
            raise AssertionError('product %s was not present in cart' % self.del_product)

    def test_updating_address_to_profile(self, setup):
        # logging in to account
        self.test_login(setup)
        #navigating to address section and editing address
        self.driver.find_element(By.XPATH, "//a[text()='Addresses']").click()
        self.driver.find_element(By.XPATH, "//a[@class='edit']").click()

        # Sending All address values collected from Data file to input fields
        first_name_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_first_name"]')
        first_name_ele.clear()
        first_name_ele.send_keys(self.first_name)
        last_name_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_last_name"]')
        last_name_ele.clear()
        last_name_ele.send_keys(self.last_name)
        billing_phone_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_phone"]')
        billing_phone_ele.clear()
        billing_phone_ele.send_keys(self.phone_number)
        billing_address_1_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_address_1"]')
        billing_address_1_ele.clear()
        billing_address_1_ele.send_keys(self.street_address)
        billing_address_2_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_address_2"]')
        billing_address_2_ele.clear()
        billing_address_2_ele.send_keys(self.apartment)
        city_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_city"]')
        city_ele.clear()
        city_ele.send_keys(self.city)
        postcode_ele = self.driver.find_element(By.XPATH, '//input[@name="billing_postcode"]')
        postcode_ele.clear()
        postcode_ele.send_keys(self.postal_code)

        # Saving Address
        self.driver.find_element(By.XPATH, '// input[ @name="save_address"]').click()
        time.sleep(2)
        try:
            # Asserting Error if Any one of mandatory parameters is not present in data
            error_ele = self.driver.find_element(By.XPATH, '//ul[@class="woocommerce-error"]')
            if error_ele:
                # pytest.fail(error_ele.text)
                raise AssertionError(error_ele.text)
        except:
            print('Address Updated Successfully')

    def test_validating_address_from_profile(self, setup):
        # logging in to account
        self.test_login(setup)
        # Getting saved data to verify
        self.driver.find_element(By.XPATH, "//a[text()='Addresses']").click()
        address_saved = self.driver.find_element(By.XPATH, "//h3[text()='%s']/ancestor::header/following-sibling::address" % self.validate_address).text
        print(address_saved)



