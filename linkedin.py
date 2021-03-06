##################### HEAD #######################

import os
import json
import random

from selenium import webdriver

from time import sleep
from exceptions import ValueError

from crawly import *
from login import *

#################### CONFIG ######################

filename_read = "companies_list.txt"
filename_write = "companies.csv"
filename_json = "companies.json"

################### FUNCTIONS ####################


def linkedin_login(username, password, browser = None):

    path_to_chromedriver = '/Users/Admin/Desktop/chromedriver' 
    if not browser: browser = webdriver.Chrome(executable_path = path_to_chromedriver)

    url = "http://linkedin.com"

    browser.get(url)

    username_field = browser.find_element_by_id("login-email")
    password_field = browser.find_element_by_id("login-password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    form = browser.find_element_by_name("submit")
    form.submit()

    return browser

def get_company_url(company, browser):

    contents = []

    BASE_URL = "https://www.linkedin.com/vsearch/c?keywords="

    query = encode("+", company)

    url = BASE_URL + query 
    browser.get(url)
    try: 
        browser.find_element_by_xpath('//*[@class="title main-headline"]').click()
        return browser.page_source
    except:
        return None


def parse_linkedin_companies(url):

    for i in xrange(5):

        try:
            response, client = load(url, client)
            data = response.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
            print data

            if data:

                try:
                    json_formatted_data = json.loads(data[0])

                    company_name = json_formatted_data['companyName'] if 'companyName' in json_formatted_data.keys() else None
                    size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else None
                    industry = json_formatted_data['industry'] if 'industry' in json_formatted_data.keys() else None
                    description = json_formatted_data['description'] if 'description' in json_formatted_data.keys() else None
                    follower_count = json_formatted_data['followerCount'] if 'followerCount' in json_formatted_data.keys() else None
                    year_founded = json_formatted_data['yearFounded'] if 'yearFounded' in json_formatted_data.keys() else None
                    website = json_formatted_data['website'] if 'website' in json_formatted_data.keys() else None
                    type = json_formatted_data['companyType'] if 'companyType' in json_formatted_data.keys() else None
                    specialities = json_formatted_data['specialties'] if 'specialties' in json_formatted_data.keys() else None
 
                    if "headquarters" in json_formatted_data.keys():
                        city = json_formatted_data["headquarters"]['city'] if 'city' in json_formatted_data["headquarters"].keys() else None
                        country = json_formatted_data["headquarters"]['country'] if 'country' in json_formatted_data['headquarters'].keys() else None
                        state = json_formatted_data["headquarters"]['state'] if 'state' in json_formatted_data['headquarters'].keys() else None
                        street1 = json_formatted_data["headquarters"]['street1'] if 'street1' in json_formatted_data['headquarters'].keys() else None
                        street2 = json_formatted_data["headquarters"]['street2'] if 'street2' in json_formatted_data['headquarters'].keys() else None
                        zip = json_formatted_data["headquarters"]['zip'] if 'zip' in json_formatted_data['headquarters'].keys() else None
                        street = street1 + ', ' + street2
                    else:
                        city = None
                        country = None
                        state = None
                        street1 = None
                        street2 = None
                        street = None
                        zip = None
 
                    data = {
                                'company_name': company_name,
                                'size': size,
                                'industry': industry,
                                'description': description,
                                'follower_count': follower_count,
                                'founded': year_founded,
                                'website': website,
                                'type': type,
                                'specialities': specialities,
                                'city': city,
                                'country': country,
                                'state': state,
                                'street': street,
                                'zip': zip,
                                'url': url
                            }
                    return data

                except:
                    print "[Error] Cannot parse page: ", url
 
            if len(response.content) < 2000 or "trk=login_reg_redirect" in url:

                if response.status_code == 404:
                    print "[Error] Linkedin page not found."
                else:
                    raise ValueError('[Error] Redirecting to login page or captcha found.')

        except :
            print "[Info] Retrying: ",url
 


##################### MAIN #######################


def main():

    extracted_data = []
    contents = []
    company_list = open(filename_read)

    browser = linkedin_login(username, password)

    for company in company_list:
        content = get_company_url(company, browser)
        contents.append(content)

    for content in contents: print content

    for url in company_urls:
        data = parse_linkedin_companies(url)
        extracted_data.append(data)
        print extracted_data
        sleep(5)
        file_json = open(filename_json, 'w')
        json.dump(extracted_data, file_json, indent=4)
 
 
if __name__ == "__main__":
    main()