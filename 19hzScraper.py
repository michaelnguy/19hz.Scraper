# Author : Michael Nguyen
# 19hz.info Event Scraper

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import json
import HTMLParser
from progress.bar import IncrementalBar

# Run Chrome Webdriver, logs into 19hz.info, and ensures we're on the right page
driver = webdriver.Chrome()
driver.get("https://19hz.info/eventlisting_BayArea.php")
assert "Event Listing" in driver.title

# Waits for the page to load before we begin scraping data
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//tbody[1]')))
except TimeoutException:
    pass  # Handle the exception here

# Locates the table of data, checks for how many rows and columns
table = driver.find_element_by_xpath('//tbody[1]').get_attribute('innerHTML')
rows = len(driver.find_elements_by_xpath("//table[1]/tbody/tr"))
columns = len(driver.find_elements_by_xpath("//table[1]/thead/tr/th"))

# Initialize a progress bar to visualize progress on the webscrape
progress_col = columns - 1;
bar = IncrementalBar('Gathering', max = rows * progress_col)

# This HTMLParser is required to unescape HTML syntax into human language
html = HTMLParser.HTMLParser()

# Main function to scrape data
def gather():
	# Data Structure for the scrapped data
	data = {}
	data['events'] = []

	# Data is organized into a table which we'll need to iterate through using a double for loop
	for x in range(1, rows + 1):
		temp = {} # List container for each row
		for y in range(1, columns):
			# This is where the cell detected and scrapped
			datum = driver.find_element_by_xpath("//table[1]/tbody/tr[" + str(x) + "]/td[" + str(y) + "]")
			if y == 1: # Date and Time Column
				# Removing any breakline, and stringfying the data
				date = datum.get_attribute('innerHTML')
				date = date.replace("<br>", " ")
				date = str(date)
				temp['datetime'] = date
			elif y == 2: # Event Name, Location, and Link Column
				# Getting location data
				full = datum.get_attribute('innerHTML')
				full = str(full).split('@')
				location = full[1].strip()
				# Getting event name data
				link = datum.find_element_by_tag_name('a')
				name = link.get_attribute('innerHTML')
				name = str(name).strip()
				name = html.unescape(name)
				# Getting event link data
				link = link.get_attribute('href')
				link = str(link)
				# Adding processed data to container
				temp['name'] = name
				temp['location'] = location
				temp['link'] = link
			elif y == 3: # Genre Tags Column
				# Splitting data into tokens
				tags = datum.get_attribute('innerHTML')
				tags = str(tags)
				tags = tags.split(",")
				# After splitting, we'll remove any whitespace with strip()
				for z in range(len(tags)):
					tags[z] = tags[z].strip()
					tags[z] = html.unescape(tags[z])
				temp['tag(s)'] = tags
			elif y == 4: # Price and Age Column
				# Getting price and age data
				full = datum.get_attribute('innerHTML')
				full = str(full)
				if not full: # Checks if cell is empty
					temp['price'] = "Check website"
					temp['age'] = "Check website"
				elif len(full.split("|")) == 2: # Checks if price and age is included
					full = full.split("|")
					full[0] = full[0].strip()
					full[1] = full[1].strip()
					temp['price'] = full[0]
					temp['age'] = full[1]
				else: # Check if price or age is present, but not both.
					if "$" in full: # If price and not age
						temp['price'] = full
						temp['age'] = "Check website"
					else: # If not price and age
						temp['price'] = "Check website"
						temp['age'] = full
			elif y == 5: # Organizer Name Column
				# Getting the organization for the event
				organizer = datum.get_attribute('innerHTML')
				organizer = str(organizer)
				# Unscaping html syntax
				organizer = html.unescape(organizer)
				if not datum: # Checks if cell is empty
					temp['organizer'] = None
				else:
					temp['organizer'] = organizer
			bar.next() # Shows data scraping progress through the table
		data['events'].append(temp)
	# After we're done iterating the table, we'll dump the data into a json file for external application usage
	with open('data.json', 'w') as outfile:
		json.dump(data, outfile, indent = 4, sort_keys=True)
	bar.finish() # Loading Bar finishes

# Run the main function
gather()

# Close the browser when we're done
driver.close()
