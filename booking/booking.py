import time
from types import TracebackType
import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
  """
  A class to interact with Booking.com website.
  """

  def __init__(self, teardown=False):
    """
    Initialize the Booking class with a WebDriver instance.

    :param teardown: Whether to quit the WebDriver instance when exiting the context manager.
    """
    super(Booking, self).__init__()
    self.implicitly_wait(5)
    self.maximize_window()
    self.teardown = teardown
    self.wait = WebDriverWait(self, 5)

  def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
    """
    Exit the context manager.

    :param exc_type: The type of exception that occurred.
    :param exc: The exception that occurred.
    :param traceback: The traceback of the exception.
    """
    if not self.teardown:
      input()
    self.quit()
    return super().__exit__(exc_type, exc, traceback)

  def close_signup_dialog(self):
    """
    Close the sign-up dialog if it appears.
    """
    times = 2
    while times > 0:
      try:
        self.wait.until(
          EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#b2indexPage > div.a1b9d2f057.c20dffcd7d > div > div')
          )
        )
        close = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
        close.click()
        # print(f"Closed sign-up dialog")
        return
      except:
        # print(f"Sign-up dialog not found or could not be closed")
        self.refresh()
      times -= 1

  def land_first_page(self):
    """
    Navigate to the first page of Booking.com.
    """
    self.get(const.BASE_URL)
    
  def change_currency(self, currency=None):
    """
    Change the currency of the search results.

    :param currency: The currency to change to.
    """
    currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
    currency_element.click()

    time.sleep(1)
    
    btns = self.find_elements(By.XPATH, "//button[@class='dba1b3bddf da38b23449 df2e3f2401 e800d43c48 a2ce59f28d']")
    for btn in btns:
      try:
        path = btn.find_element(By.XPATH, f".//div[text()='{currency}']")
        if path:
          btn.click()
          break
      except: pass

  def select_place_to_go(self, place_to_go):
    """
    Select the place to go for the search.

    :param place_to_go: The place to go.
    """
    search_field = self.find_element(By.ID, ":rh:")
    search_field.clear()
    search_field.send_keys(place_to_go)

    time.sleep(1) # let the entered place load

    first_result = self.find_element(By.ID, "autocomplete-result-0")
    first_result.click()

  def select_dates(self, check_in_date, check_out_date):
    """
    Select the check-in and check-out dates for the search.

    :param check_in_date: The check-in date.
    :param check_out_date: The check-out date.
    """
    check_in_element = self.find_element(
      By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'
    )
    check_in_element.click()

    check_out_element = self.find_element(
      By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'
    )
    check_out_element.click()

  def select_adults(self, count=1):
    """
    Select the number of adults for the search.

    :param count: The number of adults.
    """
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
    """
    Click the search button.
    """
    search_button = self.find_element(
      By.CSS_SELECTOR,
      '#indexsearch form button[type="submit"]'
    )
    search_button.click()
    self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

  def apply_filtrations(self):
    """
    Apply filtrations to the search results.
    """
    filtration = BookingFiltration(driver=self)

    filtration.sort_price_lowest_first()
    filtration.apply_star_rating(4, 5)

  def report_results(self):
    """
    Generate a report of the search results.
    """
    hotel_boxes = self.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
    report = BookingReport(hotel_boxes)

    table = PrettyTable(
      field_names=["Name", "Price", "Score"]
    )
    table.add_rows(report.pull_attributes())
    print(table)