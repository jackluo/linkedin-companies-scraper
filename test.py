from selenium import webdriver

path_to_chromedriver = '/Users/Admin/Desktop/chromedriver' 
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

browser.get(url)

