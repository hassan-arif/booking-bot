from booking.booking import Booking

with Booking(teardown=False) as bot:
  bot.land_first_page()
  bot.close_signup_dialog()

  bot.change_currency(currency='USD')
  bot.close_signup_dialog()
  
  bot.select_place_to_go('New York')