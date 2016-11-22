#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import logging 

screenshot_path = 'screenshot'

class TimeoutType():
    long = 200
    short = 50

try_count = 6
def find_element(browser, by, objective, timeout):
    global try_count
    starttime = time.time()
    try:
        locator = (by, objective)
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located(locator))
        return browser.find_element(*locator)
    except TimeoutException:
        lasttime = int(time.time() - starttime)
        logMessage = "Get element TIMEOUT, cost:{0} expect:{1} element:{2}".format(lasttime, timeout, objective)
        logger.info(logMessage)
        #exit()
        try_count -= 1
        if try_count <= 0: exit()
        time.sleep(10)
        return find_element(browser, by, objective, timeout)


def find_element_by_id(browser, objective, timeout): return find_element(browser, By.ID, objective, timeout)
def find_element_by_xpath(browser, objective, timeout): return find_element(browser, By.XPATH, objective, timeout)


def screenshot(browser, filename):
    if not os.path.isdir(screenshot_path): os.mkdir(screenshot_path)
    browser.get_screenshot_as_file(os.path.join(screenshot_path, filename))

def changeLanguage(browser, language):
    logger.info('***********************************************************************')
    logMessage = '          Begin to change language to ' + language
    logger.info(logMessage)
    logger.info('***********************************************************************')

    # Change language: Click Humburger button-->Setting-->Language-->Choose DE-->click OK
    try:
        logger.info('Click Humburger button.')
        find_element_by_xpath(browser, "//*[@id='limejs']/div[3]/div[1]/div/div/div/div[3]/div[2]/div[4]", TimeoutType.long).click()

        logger.info('Click Setting button.')
        find_element_by_xpath(browser, "//*[@id='limejs']/div[7]/div/div/div/div[2]/div/div[2]/div[2]/div[1]", 50).click()

        logger.info('Click Language button.')
        find_element_by_xpath(browser, "//*[@id='limejs']/div[7]/div/div/div/div[2]/div/div[3]/div[2]/div[5]", 30).click()

        logger.info('Choose language.')
        if language == 'EN':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[1]", 50).click()
        if language == 'DE':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[2]", 50).click()
        elif language == 'ES':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[3]", 50).click()
        elif language == 'FR':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[4]", 50).click()
        elif language == 'IT':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[5]", 50).click()
        elif language == 'PT':
            find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[4]/div[1]/div[6]", 50).click()

        logger.info('Click OK button.')
        find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[7]", 30).click()

        # Judge whether language changed completely.
        logger.info('Language changing.......')
        time.sleep(3)
        try:
            logger.info('Try whether buyChipsButton disappeared.')
            locator = (By.XPATH, "//*[@id='limejs']/div[3]/div[1]/div/div/div/div[6]/div")
            search_text_field_should_present = EC.visibility_of_any_elements_located(locator)
            WebDriverWait(browser, 200).until(EC.presence_of_element_located(locator))
            logMessage = 'Language' + language + 'changed completely.'
            logger.info(logMessage)
        except TimeoutException:
            logMessage = 'Language' + language + 'changed failed.'
            logger.info(logMessage)

    except TimeoutException:
        logMessage = 'Language' + language + 'changed failed.'
        logger.info(logMessage)

def CheckLanChangingResult(browser, language):
    try:
        logger.info('Click Buy chips button')
        find_element_by_xpath(browser, "//*[@id='limejs']/div[3]/div[1]/div/div/div/div[6]/div", 500).click()

        logger.info('Get the current language in buy chips dialog...')
        textInBuyChips = find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[2]/div[2]", 100).text

        # Compare the text in buy chips dialog and the correct value of corresponding language.
        logger.info('Comparing...')
        if language == 'EN':
            if textInBuyChips == 'Select a Chip Package':
                logMessage = 'Changing language successfully. Current Language is' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)
        if language == 'DE':
            if textInBuyChips == u'Wähle ein Chip-Paket':
                logMessage = 'Changing language successfully. Current Language is' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)
        if language == 'ES':
            if textInBuyChips == 'Elige una oferta de fichas':
                logMessage = 'Changing language successfully. Current Language is ' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)
        if language == 'FR':
            if textInBuyChips == 'Choisissez un ensemble de jetons':
                logMessage = 'Changing language successfully. Current Language is ' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)
        if language == 'IT':
            if textInBuyChips == 'Seleziona un pacchetto di chip':
                logMessage = 'Changing language successfully. Current Language is ' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)
        if language == 'PT':
            if textInBuyChips == 'Selecione um Pacote de fichas':
                logMessage = 'Changing language successfully. Current Language is ' + language + '.'
                logger.info(logMessage)
            else:
                logMessage = 'Changing Language to ' + language + 'failed.'
                logger.info(logMessage)

        # Get the screenshort for checking if needed.
        logger.info("Get screenshort for checking if you need.")
        screenshot(browser, language+'.png')

        # Close buy chips dialog by clicking x button.
        logger.info("Close buy chips dialog.")

        time.sleep(3)
        find_element_by_xpath(browser, "//*[@id='mobileDialogDiv']/div[1]/div/div/div/div[2]/div/div/div[2]/div[3]/div", 50).click()

        logger.info('***********************************************************************')
        logMessage = "       Congratulations!  Changing to " + language + " is OK!"
        logger.info(logMessage)
        logger.info('***********************************************************************')

    except TimeoutException:
        print('Change language to {0} failed.'.format(language))
        browser.close()

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Create handler for writing log to file
log_path = 'logs'
logfile = os.path.join(log_path, 'log.txt')
if not os.path.isdir(log_path): os.mkdir(log_path)
fh = logging.FileHandler(logfile,mode = 'w')
fh.setLevel(logging.INFO)

# Create handler for outputting log  to console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Define the format of the handler
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add logger to handler
logger.addHandler(fh)
logger.addHandler(ch)


# Open the web page
logger.info('Open the DDI')
b = webdriver.Chrome(r"c:/python27/chromedriver.exe")
b.get("https://apps.facebook.com/doubledowncasino/")
b.maximize_window()

#Input user Info and then login
logger.info('Input user Info')
find_element_by_id(b,"email",10).clear()
find_element_by_id(b,"email",10).send_keys("jing.shen@igt.com")
find_element_by_id(b,"pass",10).clear()
find_element_by_id(b,"pass",10).send_keys("!qaz2wsx")
find_element_by_id(b,"loginbutton",10).click()
logger.info('Finished autherization')

#Change frame
frame_canvas = find_element_by_id(b,"iframe_canvas",150)
b.switch_to.frame(frame_canvas)

try:
    changeLanguage(b, 'DE')
    CheckLanChangingResult(b, 'DE')

    changeLanguage(b, 'ES')
    CheckLanChangingResult(b, 'ES')

    changeLanguage(b, 'FR')
    CheckLanChangingResult(b, 'FR')

    changeLanguage(b, 'IT')
    CheckLanChangingResult(b, 'IT')

    changeLanguage(b, 'PT')
    CheckLanChangingResult(b, 'PT')

    changeLanguage(b, 'EN')
    CheckLanChangingResult(b, 'EN')

except TimeoutException:
    logger.info('Change language failed.')
    b.close()

b.close()
