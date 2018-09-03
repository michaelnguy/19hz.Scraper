# 19hz.Scraper
A Python-based web scraper that pulls event data from 19hz.info and outputs a beautified JSON file

## Fields
19hz.Scraper returns the following fields:

- age (event age requirement)
- datetime (date/time of the event)
- link (event website link)
- location (location of event)
- name (event name)
- organizer (name of organization for event)
- price (admission cost to event)
- tags (event genre tags)


## Getting Started

The following instructions will help you get the project up and running.

## Installation

1. [Python 2.7](https://www.python.org/downloads/release/python-2710/)
2. [pip](https://www.makeuseof.com/tag/install-pip-for-python/)
3. HTMLParser (if you don't have it)
```
sudo pip install HTMLParser
```
4. Progress Bar
```
sudo pip install progress
```
5. Selenium ([Detailed installation](https://selenium-python.readthedocs.io/installation.html))
```
sudo pip install selenium
```
6. Select your desired browser driver (Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.)
- [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [FireFox](https://github.com/mozilla/geckodriver/releases)
- [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)

## Running the Project
1. On the command prompt, create a folder and cd into it.
```
cd 19hzScraper
```
2. Before you run the project, you have the option to run in headless mode and/or to sort the JSON file.
- Note: As long as you include the sort key and/or the '-hl' option in the arguments (in any ordering), any extraneous subsequent arguments will be ignored and the program should still run.
##### Sort keys
- age
- name
- price
- datetime
- location
#### Head mode, no sorting
```
python 19hzScraper.py 
```
#### Head mode, sorted by name
```
python 19hzScraper.py name
```
#### Headless mode, no sorting
```
python 19hzScraper.py -hl
```
#### Headless mode, sorted by age
```
python 19hzScraper.py -hl age
python 19hzScraper.py age -hl
```
3. Wait for the output file
```
{
    "events": [
        {
            "age": "21+", 
            "datetime": "Sat: Sep 1 (6am-11am)", 
            "link": "https://theendupsf.com/event/inside-out-september-1/", 
            "location": "The Endup (San Francisco)", 
            "name": "Inside Out: Indoor & Outdoor Saturday Morning Party w/ DJ Firestone, Teenus Turner, Cristoffer Z & Love Tap", 
            "organizer": "", 
            "price": "Check website", 
            "tag(s)": [
                "deep house", 
                "tech house"
            ]
        }
...
```
## Parsing the JSON
If I want to print out the event name and age requirement in Python,
```python
import json

with open('data.json') as f:
    data = json.load(f)
    for event in data['events']:
    	print(event['name'] + ' ' +  event['age'])
```

## Authors

* **Michael Nguyen** - *Initial work* - [19hz.Scraper](https://github.com/michaelnguy/19hz.Scraper)

See also the list of [contributors](https://github.com/michaelnguy/19hz.Scraper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/michaelnguy/19hz.Scraper/blob/master/LICENSE) file for details
