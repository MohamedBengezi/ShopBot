from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException


def run(username, password, cvv):
    driver = webdriver.Chrome('Main\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('https://store.nvidia.com/DRHM/store?Action=Logout&SiteID=nvidia&Locale=en_US&ThemeID=326200&Env=BASE&nextAction=help')
    driver.find_element_by_id('loginEmail').send_keys(str(username))
    pass_text = driver.find_element_by_id('loginPassword')
    pass_text.send_keys(str(password))
    pass_text.submit()
    driver.get("https://www.nvidia.com/en-us/shop/geforce/gpu/?page=1&limit=1&locale=en-us&category=GPU&search=NVIDIA%20GEFORCE%20RTX%203080")
    while True:
        try:
            add_to_cart_button = driver.find_element_by_partial_link_text("CART")  # driver.find_element_by_class_name('cta-button').click()
        except NoSuchElementException:
            driver.execute_script("window.location.reload(true);")
        else:
            add_to_cart_button.click()
            break
    driver.find_element_by_class_name('cart__checkout-button').click()
    continue_xpath = "//input[@type='submit' and @value='continue']"
    driver.find_element_by_xpath(continue_xpath).click()
    driver.find_element_by_id('cardSecurityCode').send_keys(str(cvv))
    driver.find_element_by_xpath(continue_xpath).click()
    try:
        card_button = driver.find_element_by_id('cCard1')
    except NoSuchElementException:
        print('!!!!!! GOOD')
    else:
        card_button.click()
        driver.find_element_by_xpath(continue_xpath).click()
        print('selected card!!!!!!!')
    driver.find_element_by_xpath("//input[@type='submit' and @value='submit']").click()
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
