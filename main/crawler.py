from selenium import webdriver


option = webdriver.ChromeOptions()

browser = webdriver.Chrome(executable_path='C:\\ProgramData\\Anaconda3\\selenium\\chromedriver.exe', chrome_options=option)
browser.get("https://getaroom.io/67f6ac")
# input = browser.find_elements_by_css_selector("//*[@id='displayName']")
# input.clear()
# input.send_keys('ali')
text_area = browser.find_element_by_id("displayName")
print(text_area)
text_area.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
text_area.send_keys("test")
