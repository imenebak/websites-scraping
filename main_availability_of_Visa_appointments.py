import time
import xpaths
import password
import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

driver_path = "VirtualPath\\chromedriver.exe"


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(options=options,executable_path=driver_path)
browser.implicitly_wait(5) # seconds
def capt():

    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
def login(xe,xpw,xsub,uid,upw):
    browser.get('https://online.vfsglobal.dz/Global-Appointment/Account/RegisteredLogin?ReturnUrl=%2fGlobal-Appointment%2fAccount%2fLogOff')
    mail = browser.find_element_by_xpath(xe)
    ao = True
    pw = browser.find_element_by_xpath(xpw)
    mail.send_keys(uid)
    pw.send_keys(upw)
    capt()
    time.sleep(15)
    browser.switch_to.default_content()
    #browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[0])
    try:
        browser.find_element_by_xpath(xsub).submit()
    except:
        login(xpaths.email, xpaths.password, xpaths.submit, password.userid, password.pw)
    check_session_expired()
    appointment(xpaths.appointment,xpaths.selone, xpaths.categorie)


def check_appointment(first_run_flag):
    if "Pas de créneau disponible pour cette catégorie de visa" in browser.page_source:
            #log.info("No appointments are available, trying again in {} minutes.".format(schedule_interval/60))
            if first_run_flag:
                #log.debug("Welcome email notification will be sent to the recipient")
                send_email_2_me("DONT GO","RDV NON DISPO AS ALWAYS")

    elif "Prochain rendez-vous disponible le" in browser.page_source:
            if first_run_flag:
                #log.info("New appointments are available! Please book soon.")
                send_email_2_me("DONT GO","RDV NON DISPO AS ALWAYS")
    elif "Catégorie principale de visa" in browser.page_source:
            #log.info("New appointments are available! Please book soon.")
            send_email_2_me("GO GO GO","RDV DISPONIIIIIIIIIBLE")
    else:
            #log.info("New appointments are available! Please book soon.")
            send_email_2_me("GO GO GO","JE SAIS PAS CE QUI SE PASSE")

def appointment(ax,sx, cx):
    browser.find_element_by_xpath(ax).click()
    time.sleep(random.randint(3,5))
    selelement = Select(browser.find_element_by_xpath(cx))
    try_time = True
    visa_type = "ETUDIANT"
    while True:
        print("JE CHOISIE ", visa_type)
        #selelement.select_by_visible_text('VFS Visa Application Center - Algeria')
        time.sleep(random.randint(3,5))
        selelement.select_by_visible_text('Étudiant')
        time.sleep(random.randint(3,5))
        check_appointment(try_time)
        """if "Pas de créneau disponible pour cette catégorie de visa" in browser.page_source:
            print("hi")"""
        browser.find_element_by_xpath(ax).click()
        selelement = Select(browser.find_element_by_xpath(cx))
        try_time = False

def send_email_2_me(msg, sub):
    print(msg, sub)
    mail = "something@something.somethinsg"
    gmail_code = "code you have to generate frome ur gmail account parameters - if using gmail :v"
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = mail
    msg['Subject'] = str(sub)
    message = str(msg)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(mail, gmail_code)
    mailserver.sendmail(mail, mail, msg.as_string())
    mailserver.quit()

def check_session_expired():
    if 'Session timeout' in browser.page_source:
        browser.quit()
        login(xpaths.email, xpaths.password, xpaths.submit, password.userid, password.pw)
    elif 'Cliquez sur "Je ne suis pas un robot"' in browser.page_source:
        browser.quit()
        login(xpaths.email, xpaths.password, xpaths.submit, password.userid, password.pw)
    pass
login(xpaths.email, xpaths.password, xpaths.submit, password.userid, password.pw)
