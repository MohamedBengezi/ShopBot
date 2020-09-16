from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime


class ElementHasPartial(object):
    def __init__(self, partial_val):
        self.partial_val = partial_val

    def __call__(self, driver):
        try:
            return driver.find_element_by_partial_link_text(self.partial_val)
        except NoSuchElementException:
            return False


class ElementHasXpath(object):
    def __init__(self, xpath_val):
        self.xpath_val = xpath_val

    def __call__(self, driver):
        try:
            return driver.find_element_by_xpath(self.xpath_val)
        except NoSuchElementException:
            return False


class ElementHasClass(object):
    def __init__(self, class_val):
        self.class_val = class_val

    def __call__(self, driver):
        try:
            return driver.find_element_by_class_name(self.class_val)
        except NoSuchElementException:
            return False


class ElementHasId(object):
    def __init__(self, id_val):
        self.id_val = id_val

    def __call__(self, driver):
        try:
            return driver.find_element_by_id(self.id_val)
        except NoSuchElementException:
            return False


def run(username, password, cvv):
    continue_xpath = "//input[@type='submit' and @value='continue']"
    submit_xpath = "//input[@type='submit' and @value='submit']"
    print('Starting Now')
    print(datetime.now())
    driver = webdriver.Chrome('Main\chromedriver.exe')
    wait = WebDriverWait(driver, 15, poll_frequency=0.01)
    wait_add = WebDriverWait(driver, 5, poll_frequency=0.01)
    driver.get('https://store.nvidia.com/DRHM/store?Action=Logout&SiteID=nvidia&Locale=en_US&ThemeID=326200&Env=BASE&nextAction=help')
    wait.until(ElementHasId('loginEmail')).send_keys(str(username))
    pass_text = wait.until(ElementHasId('loginPassword'))
    pass_text.send_keys(str(password))
    pass_text.submit()
    driver.get("https://www.nvidia.com/en-us/shop/geforce/gpu/?page=1&limit=1&locale=en-us&category=GPU&search=NVIDIA%20GEFORCE%20RTX%203080")
    # driver.get("https://www.nvidia.com/en-us/shop/geforce/gpu/?page=1&limit=1&locale=en-us&category=GPU&search=NVIDIA%20GEFORCE%20RTX%202060%20SUPER")
    while True:
        try:
            add_to_cart_button = wait_add.until(ElementHasPartial('CART'))
        except TimeoutException:
            driver.execute_script("window.location.reload(true);")
        else:
            add_to_cart_button.click()
            break
    wait.until(ElementHasClass('cart__checkout-button')).click()
    while True:
        try:
            driver.find_element_by_xpath(continue_xpath).click()
        except NoSuchElementException:
            try:
                driver.find_element_by_id('loginID').send_keys(str(username))
            except NoSuchElementException:
                continue
            else:
                login_pass = driver.find_element_by_id('loginPass')
                login_pass.send_keys(str(password))
                login_pass.submit()
                wait.until(ElementHasXpath(continue_xpath)).click()
                break
        else:
            break
    sec_code = wait.until(ElementHasId('cardSecurityCode'))
    sec_code.send_keys(str(cvv))

    # Below two code blocks are to test if .submit() is faster than finding the CONTINUE button and clicking it

    start = datetime.now()
    sec_code.submit()
    finish = datetime.now()
    diff = finish - start
    print('Time to use sec_code.submit(): ' + str(diff.total_seconds()))

    # start = datetime.now()
    # wait.until(ElementHasXpath(continue_xpath)).click()
    # finish = datetime.now()
    # diff = finish - start
    # print('Time to use wait.until(ElementHasXpath(continue_xpath)).click(): ' + str(diff.total_seconds()))

    while True:
        try:
            driver.find_element_by_xpath(submit_xpath).click()
        except NoSuchElementException:
            try:
                driver.find_element_by_id('cCard1').click()
            except NoSuchElementException:
                continue
            else:
                wait.until(ElementHasXpath(continue_xpath)).click()
                wait.until(ElementHasXpath(submit_xpath)).click()
                break
        else:
            break
    print(datetime.now())
    return driver


if __name__ == '__main__':
    import argparse
    import getpass
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('-c', '--cvv')
    parser.add_argument('-q', '--quit', default=False)
    args = parser.parse_args()
    user_str = input(
        'Whats your NVIDIA username? ') if args.username is None else args.username
    pass_str = getpass.getpass(
        prompt='Whats your NVIDIA password? ') if args.password is None else args.password
    cvv_str = getpass.getpass(
        prompt='Whats your Credit card cvv? ') if args.cvv is None else args.cvv
    main_driver = run(username=user_str, password=pass_str, cvv=cvv_str)
    if not args.quit:
        input('Press enter to quit\n')
    main_driver.quit()
