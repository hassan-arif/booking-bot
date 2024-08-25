from booking.booking import Booking

with Booking(teardown=False) as bot:
  bot.land_first_page()
  bot.close_signup_dialog()
  bot.change_currency(currency='USD')

  bot.select_place_to_go(input("Where do you want to go? "))
  
  # YYYY-MM-DD
  bot.select_dates(check_in_date=input("What is the check in date? "),
                   check_out_date=input("What is the check out date? "))
  
  bot.int(input("How many people ?"))(int(input("How many people? ")))
  
  bot.click_search()
  bot.apply_filtrations()
  bot.report_results()