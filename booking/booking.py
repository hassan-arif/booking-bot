from types import TracebackType
import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Booking(webdriver.Edge):

  def __init__(self, teardown=False):
    self.teardown = teardown
    super(Booking, self).__init__()
    self.implicitly_wait(5)
    self.maximize_window()
    self.signup_dialog=False

  def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
    if not self.teardown:
      input()
    self.quit()
    return super().__exit__(exc_type, exc, traceback)

  def close_signup_dialog(self):
    if not self.signup_dialog:
      try:
        WebDriverWait(self, 5).until(
          EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
          )
        ).click()
        print(f"Closed sign-up dialog")
        self.signup_dialog = True
      except:
        print(f"Sign-up dialog not found or could not be closed")
    else: print("Sign-up dialog already closed")

  def land_first_page(self):
    self.get(const.BASE_URL)
    
  def change_currency(self, currency=None):
    currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
    currency_element.click()
    
    btns = self.find_elements(By.XPATH, "//button[@class='dba1b3bddf da38b23449 df2e3f2401 e800d43c48 a2ce59f28d']")
    for btn in btns:
      try:
        path = btn.find_element(By.XPATH, f".//div[text()='{currency}']")
        if path:
          btn.click()
          break
      except: pass

  def select_place_to_go(self, place_to_go):
    search_field = self.find_element(By.ID, ":rh:")
    search_field.clear()
    search_field.send_keys(place_to_go)

    time.sleep(1) # let the entered place load

    first_result = self.find_element(By.ID, "autocomplete-result-0")
    first_result.click()

  def select_dates(self, check_in_date, check_out_date):
    check_in_element = self.find_element(
      By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'
    )
    check_in_element.click()

    check_out_element = self.find_element(
      By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'
    )
    check_out_element.click()

  def select_adults(self, count=1):
    selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
    selection_element.click()
    
    decrease_adults_element = self.find_element(
      By.CSS_SELECTOR, '.dba1b3bddf.e99c25fd33.aabf155f9a.f42ee7b31a.a86bcdb87f.e137a4dfeb.af4d87ec2f'
    )
    adults_value_element = self.find_element(By.XPATH, "//input[@id='group_adults']/parent::div/div[@class='f71ad9bb14']/span")

    while True:
      decrease_adults_element.click()
      adults_value = adults_value_element.text # Should give back the adults count

      if int(adults_value) == 1:
          break
    increase_button_element = self.find_element(
      By.XPATH,
      "//input[@id='group_adults']/parent::div/div[@class='f71ad9bb14']/button[@class='dba1b3bddf e99c25fd33 aabf155f9a f42ee7b31a a86bcdb87f e137a4dfeb d1821e6945']"
    )

    for _ in range(count - 1):
        increase_button_element.click()

  def click_search(self):
    search_button = self.find_element(
      By.CSS_SELECTOR,
      '#indexsearch form button[type="submit"]'
    )
    search_button.click()