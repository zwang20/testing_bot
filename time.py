# import modules 
import datetime 
import pytz

# define variables 
import assets.data.timezones_dictionary as timezones_dictionary

# Get time
async def get_time(message, *args):

  # define variables 

  if args:
    timezone_input = args[0]
  
  else:
    timezone_input = 'Australia/Sydney'

  try:
    timezone_input = timezones_dictionary[timezone_input.lower()]
  
  # Nothing to replace
  except KeyError:
    pass
  
  try:
    output_time = datetime.datetime.now(pytz.timezone(timezone_input))

  # Incorrect Timezone 
  except pytz.exceptions.UnknownTimeZoneError:
    return ('Unknown Timezone')
  
  # Output
  return output_time.strftime("%A %Y %B %d %H:%M:%S %Z %z")