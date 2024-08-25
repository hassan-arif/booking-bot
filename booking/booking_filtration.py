# This file will include a class with instance methods that will be responsible to interact with our website after we have some results, to apply filtrations.

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

class BookingFiltration:
  """
  A class to apply filters to search results on Booking.com.
  """

  def __init__(self, driver: WebDriver):
    """
    Initialize the BookingFiltration class with a WebDriver instance.

    :param driver: A WebDriver instance.
    """
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 5)

  def apply_star_rating(self, *star_values):
    """
    Apply star rating filter to search results.

    :param star_values: Variable number of star rating values to filter by.
    """
    star_filtration_box = self.driver.find_element(By.XPATH, '//div[@data-filters-group="class"]')
  
    for star_value in star_values:
      try:
        star_filtration_div = star_filtration_box.find_element(By.XPATH, f'./div[@data-filters-item="class:class={star_value}"]')
      except:
        print(f'not found for {star_value}')
        continue
      else:
        star_filtration_div.click()

  def sort_price_lowest_first(self):
    """
    Sort search results by price, lowest first.
    """
    time.sleep(1)
    dropdown = self.driver.find_element(By.XPATH, '//button[@data-testid="sorters-dropdown-trigger"]')
    dropdown.click()
    time.sleep(2) # wait for dropdown to load options
    self.driver.find_element(By.XPATH, '//button[@data-id="price"]').click()