from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box

        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the list page
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                '#id_text:invalid'
            )
        )

        # She starts typing some text for the new item and the error disappears

        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                '#id_text:valid'
            )
        )

        # and she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                '#id_text:invalid'
            )
        )

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                '#id_text:valid'
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list5
        BUY_WELLIES = 'Buy wellies'
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(BUY_WELLIES)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )
        self.wait_for_row_in_list_table(f'1: {BUY_WELLIES}')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys(BUY_WELLIES)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_in_element().text,
                DUPLICATE_ITEM_ERROR
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        TEST = 'Banter too thick'
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(TEST)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(f"1: {TEST}")
        self.get_item_input_box().send_keys(TEST)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertTrue(self.get_error_in_element().is_displayed())
            )

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see the error message disappears
        self.wait_for(
            lambda: self.assertFalse(
                self.get_error_in_element().is_displayed()
            )
        )

    def get_error_in_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')
