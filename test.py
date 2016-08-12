from selenium import webdriver
from login import *

path_to_chromedriver = '/Users/Admin/Desktop/chromedriver' 
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

filename_read = "companies_list.txt"

def encode(character, query = None):

    if not query:
        query = raw_input("[Info] Enter search query >>> ")

    query = query.strip().replace(" ", character) 

    return query


def get_company_url(company):

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




def linkedin_login(username, password):

    path_to_chromedriver = '/Users/Admin/Desktop/chromedriver' 
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

    url = "http://linkedin.com"

    browser.get(url)

    username_field = browser.find_element_by_id("login-email")
    password_field = browser.find_element_by_id("login-password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    form = browser.find_element_by_name("submit")
    form.submit()

companies = open(filename_read)
contents = []

for company in companies:
    content = get_company_url(company)
    contents.append(content)

browser.quit()



def linkedin_login(headers = {}):

    HOMEPAGE_URL = "https://www.linkedin.com"
    LOGIN_URL = "https://www.linkedin.com/uas/login-submit"
    login_info = {}

    try:
        response, client = load(HOMEPAGE_URL)
        csrf = list(set(response.xpath('//*[@id="loginCsrfParam-login"]/@value')))[0]

        login_info["session_key"] = username
        login_info["session_password"] = password
        login_info["loginCsrfParam"] = csrf
        client.post(LOGIN_URL, data=login_info)

    except:
        print "[Error] Login error."
        quit()

    return client


def get_company_url(company):

    BASE_URL = "https://www.linkedin.com/vsearch/c?keywords="

    client = linkedin_login()
    query = encode("+", company)

    url = BASE_URL + query 
    response, client = load(url, client)
    data = response.xpath('//a[@class="title main-headline"]/@href')
    print data


