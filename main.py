import sys
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

timeout = 10


def get_first_search_result_url(browser, url, search_word):
    input_search_locator = 'q'
    results_locator = 'g'
    results_url_locator = 'cite'

    browser.get(url)
    search_input = browser.find_element_by_name(input_search_locator)
    search_input.send_keys(search_word)
    search_input.send_keys(Keys.ENTER)

    WebDriverWait(browser, timeout).until(
        EC.visibility_of_any_elements_located((By.CLASS_NAME, results_locator))
    )
    first_search_result = browser.find_elements_by_class_name(results_locator)[0]
    return first_search_result.find_element_by_tag_name(results_url_locator)


def get_first_search_image_result(browser):
    images_search_type_locator = 'Картинки'
    image_result_locator = 'isv-r'

    browser.find_element_by_link_text(images_search_type_locator).click()
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_any_elements_located(
            (By.CLASS_NAME, image_result_locator))
    )

    return browser.find_elements_by_class_name(image_result_locator)[0]


def test(browser, url, search_word):
    expected_url_part = 'selenide.org'
    expected_text = 'selenide'

    first_search_result_url = get_first_search_result_url(browser, url, search_word)

    assert expected_url_part in first_search_result_url.text

    first_image_result = get_first_search_image_result(browser)

    assert expected_text in first_image_result.text


if __name__ == '__main__':
    executable_path = sys.argv[1]
    search_word = sys.argv[2]
    browser = Firefox(executable_path=executable_path)
    test(browser, 'https://www.google.com', search_word)
