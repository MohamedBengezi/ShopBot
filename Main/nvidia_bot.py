from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


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
    driver = webdriver.Chrome('Main\chromedriver.exe')
    wait = WebDriverWait(driver, 15, poll_frequency=0.01)
    driver.implicitly_wait(10)
    driver.get('https://store.nvidia.com/DRHM/store?Action=Logout&SiteID=nvidia&Locale=en_US&ThemeID=326200&Env=BASE&nextAction=help')
    driver.find_element_by_id('loginEmail').send_keys(str(username))
    pass_text = driver.find_element_by_id('loginPassword')
    pass_text.send_keys(str(password))
    pass_text.submit()
    driver.get("https://www.nvidia.com/en-us/shop/geforce/gpu/?page=1&limit=1&locale=en-us&category=GPU&search=NVIDIA%20GEFORCE%20RTX%203080")
    driver.implicitly_wait(0)
    while True:
        try:
            add_to_cart_button = driver.find_element_by_partial_link_text("CART")  # driver.find_element_by_class_name('cta-button').click()
        except NoSuchElementException:
            time.sleep(2)
            driver.execute_script("window.location.reload(true);")
            time.sleep(8)
        else:
            add_to_cart_button.click()
            break
    wait.until(ElementHasClass('cart__checkout-button')).click()
    wait.until(ElementHasXpath(continue_xpath)).click()
    wait.until(ElementHasId('cardSecurityCode')).send_keys(str(cvv))
    wait.until(ElementHasXpath(continue_xpath)).click()
    while True:
        try:
            submit_button = driver.find_element_by_xpath(submit_xpath)
        except NoSuchElementException:
            try:
                card_button = driver.find_element_by_id('cCard1')
            except NoSuchElementException:
                continue
            else:
                card_button.click()
                wait.until(ElementHasXpath(continue_xpath)).click()
                print('selected card!!!!!!!')
                break
        else:
            submit_button.click()
            print('!!!!!! GOOD')
            break
    try:
        final_submit = wait.until(ElementHasXpath(submit_xpath))
    except TimeoutException:
        pass
    else:
        final_submit.click()
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
    user_str = input('Whats your NVIDIA username? ') if args.username is None else args.username
    pass_str = getpass.getpass(prompt='Whats your NVIDIA password? ') if args.password is None else args.password
    cvv_str = getpass.getpass(prompt='Whats your Credit card cvv? ') if args.cvv is None else args.cvv
    main_driver = run(username=user_str, password=pass_str, cvv=cvv_str)
    if not args.quit:
        input('Press enter to quit\n')
    main_driver.quit()
