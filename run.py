"""
A script to interact with Booking.com and generate a report of search results.

This script uses the Booking class to navigate Booking.com, select search options, 
and generate a report of the search results.
"""

from booking.booking import Booking

def main():
  """
  The main function to execute the script.
  """
  with Booking(teardown=False) as bot:
    """
    Create a Booking instance and navigate to the first page of Booking.com.
    """
    bot.land_first_page()
    bot.close_signup_dialog()
    bot.change_currency(currency='USD')

    """
    Get user input for the search options.
    """
    place_to_go = input("Where do you want to go? ")
    check_in_date = input("What is the check in date? ")
    check_out_date = input("What is the check out date? ")
    adults_count = int(input("How many people? "))

    """
    Select the search options.
    """
    bot.select_place_to_go(place_to_go)
    bot.select_dates(check_in_date=check_in_date, check_out_date=check_out_date)
    bot.select_adults(count=adults_count)
    
    """
    Click the search button and apply filtrations to the search results.
    """
    bot.click_search()
    bot.apply_filtrations()
    bot.report_results()

if __name__ == "__main__":
  """
  Execute the main function.
  """
  main()