# This file is going to include method that will parse the specific data that we need from each one of the deal boxes.

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class BookingReport:
    """
    A class to extract data from deal boxes on Booking.com.
    """

    def __init__(self, boxes_section_element: WebElement):
        """
        Initialize the BookingReport class with a WebElement representing the deal boxes section.

        :param boxes_section_element: A WebElement representing the deal boxes section.
        """
        self.deal_boxes = boxes_section_element

    def pull_attributes(self) -> list:
        """
        Extract hotel name, price, and score from each deal box.

        :return: A list of lists, where each sublist contains hotel name, price, and score.
        """
        collection = []

        for deal_box in self.deal_boxes:
            try:
                hotel_name = deal_box.find_element(
                    By.XPATH, './/div[@data-testid="title"]'
                ).get_attribute('innerHTML').strip()

                hotel_price = deal_box.find_element(
                    By.XPATH, './/span[@data-testid="price-and-discounted-price"]'
                ).get_attribute('innerHTML').strip()

                hotel_score = deal_box.find_element(
                    By.XPATH, './/div[@data-testid="review-score"]/div[@class="d0522b0cca fd44f541d8"]'
                ).get_attribute('innerHTML').split('</div>')[-1].strip()

                collection.append([hotel_name, hotel_price, hotel_score])
            except:
                continue

        return collection