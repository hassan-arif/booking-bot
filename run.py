from booking.booking import Booking

with Booking(teardown=False) as bot:
  bot.land_first_page()
  bot.close_signup_dialog()

  bot.change_currency(currency='USD')
  bot.close_signup_dialog()
  
  bot.select_place_to_go('New York')
  bot.select_dates(check_in_date='2024-08-24',
                  check_out_date='2024-08-30')
  bot.select_adults(1)

  bot.click_search()

  # bot.apply_filtrations()