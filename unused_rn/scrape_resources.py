import time
from selenium import webdriver

from resources import data_urls

# Set the Firefox browser to headless, try later
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')

# Launch firefox
driver = webdriver.Firefox()

# In the firefox browser, go to the desired asset URL
driver.get(data_urls.btc_url)

# On that page, find all the technical indicator rows in a table
# Iterate over every technical indicator, and return the RSI (Or whatever other technical indicator you want to return)
try:
    while True:
        rows = driver.find_elements("css selector", "tr.datatable_row__Hk3IV")
        for row in rows:
            # Check for RSI
            if "RSI(14)" in row.text:
                print(row.text)
        time.sleep(60)
except KeyboardInterrupt:
    print("Exiting technical indicator loop scan")
finally:
    driver.quit()

"""
the above all works, but i want to make it headless, add proxy randomization to change the IP address each request, and 
if the connection is given a captcha, somehow recognize that and try a different proxy or refresh the page.
"""