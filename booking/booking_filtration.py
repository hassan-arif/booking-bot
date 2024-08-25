# This file will include a class with instance methods that will be responsible to interact with our website after we have some results, to apply filtrations.

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

class BookingFiltration:
  def __init__(self, driver:WebDriver):
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 5)

  def apply_star_rating(self, *star_values):
    
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
    time.sleep(1)
    dropdown = self.driver.find_element(By.XPATH, '//button[@data-testid="sorters-dropdown-trigger"]')
    dropdown.click()
    time.sleep(2) # wait for dropdown to load options
    self.driver.find_element(By.XPATH, '//button[@data-id="price"]').click()