import csv
import random
import sqlite3
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from sqlite3 import Error
import requests
import json
import time
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)
re_run = 4
path = "/Company/"
download_dir = path +"file_pdf"
chrome_driver = r'/thuthapdulieudoanhnghiep/chromedriver'
page_link = "https://bocaodientu.dkkd.gov.vn/"

s = Service(chrome_driver)
chromeOptions = Options()
# chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("--allow-running-insecure-content")
chromeOptions.add_argument("--ignore-certificate-errors")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
chromeOptions.add_argument('--no-sandbox')
prefs = {  # "profile.default_content_settings.popups": 0,
    "download.default_directory": download_dir,
    # DOWNLOAD DIRECTORY
    "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.set_capability("acceptInsecureCerts", True)
# driver = webdriver.Chrome(service=s, options=chromeOptions)


url = 'https://bocaodientu.dkkd.gov.vn/'
get_Search = "https://bocaodientu.dkkd.gov.vn/egazette/Public/Srv.aspx/GetSearch"
timeout = 5
headers = {'Content-Type': 'application/json'}
time_wait = 0.2
count_wait = 50

downloaded = False
downloading = False
exist_document = False
exist_company = False
error_connection = False
document = ''
# db = r"/source/company_list_30.db"


def insert_log_to_database(company_id):
    global exist_company, exist_document, downloaded, document, error_connection,path
    try:
        conn = sqlite3.connect(
            path+"company_list_30.db")
        cursor = conn.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = "INSERT INTO log(company_id,exist_company,exist_document,downloaded,error_connection)VALUES (" + company_id + "," + str(
            exist_company) + "," + str(exist_document) + "," + str(downloaded) + "," + str(error_connection) + ")"
        cursor.execute(sqlite_insert_query)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def count_of_file():
    path = download_dir
    os.chdir(path)
    t = os.listdir(os.getcwd())
    print("Count files : " + str(len(t)))


def setup_parameter():
    global download_success, have_file, exist_company
    download_success = False
    have_file = False
    exist_company = False


def check_exists_by_id(id_element, driver):
    try:
        h = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_element)))
    except TimeoutException:
        return False
    return True


def check_exists_by_xpath(driver, xpath_element):
    try:
        h = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_element)))
    except TimeoutException:
        return False
    return True


def check_pdf_file():
    time_out = 10
    if not downloading:
        return False
    while True:
        time.sleep(0.1)
        path = download_dir
        print(path)
        os.chdir(path)
        newest = max(os.listdir(os.getcwd()), key=os.path.getmtime)
        # print(newest[-3:])
        if (newest[-3:] == "pdf") and ('result.' in newest):
            return True
        if time_out < 0:
            break
        time_out = time_out - 0.1
    return False


def func_click_element_by_id(id, driver, action):
    global time_wait, count_wait
    for item in range(count_wait):
        try:
            e = driver.find_element(By.ID, id)
            action.click(e).perform()
            # driver.execute_script("document.getElementById('" + str(id) + "').click();")
            return True
        except:
            time.sleep(time_wait)
    return False


def func_find_element_by_id(id, driver):
    global time_wait, count_wait
    for item in range(count_wait):
        try:
            e = driver.find_element(By.ID, id)
            return True
        except:
            time.sleep(time_wait)
    return False


def func_click_element_by_xpath(xpath, driver, action):
    global time_wait, count_wait
    for item in range(count_wait):
        try:
            e = driver.find_element(By.XPATH, xpath)
            action.click(e).perform()
            # driver.execute_script("document.getElementById('" + str(id) + "').click();")
            return True
        except:
            time.sleep(time_wait)
    return False


def func_find_element_by_xpath(xpath, driver):
    global time_wait, count_wait
    for item in range(count_wait):
        try:
            e = driver.find_element(By.XPATH, xpath)
            return True
        except:
            time.sleep(time_wait)
    return False


def latest_download_file():
    path = download_dir
    os.chdir(path)
    newest = max(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = download_dir + "/" + newest
    print(newest)
    return newest


def search_match_id(company_id, driver, action, re_run):
    global exist_company, error_connection
    error_connection = False
    if re_run < 0:
        error = driver.find_element("error_to_search_match_id")
        action.click(error).perform()
        error_connection = True
    try:
        h = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_hdParameter")))
    except TimeoutException:
        print("Can't get hash code ")
        return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
    payload = json.dumps({
        "searchField": str(company_id),
        "h": h.get_attribute("value")
    })
    response = requests.post(get_Search, headers=headers, data=payload, verify=False)
    time_out = 10
    while response.status_code != 200:
        print("Status code different 200!")
        time_out = time_out - 1
        time.sleep(0.5)
        if time_out == 0:
            print("Post request time out")
            driver.get(url)
            return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
    try:
        res = response.json()
        temp = len(res['d'])
    except TypeError:
        print("Response fail")
        time.sleep(0.2)
        return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
    if temp == 0:
        print('None company')
        return False
    else:
        print("Exist company")
        exist_company = True
        try:
            # search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_FldSearch")))
            if not func_find_element_by_id("ctl00_FldSearch", driver=driver):
                print("Search field not exist")
                return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
            print("Search field exist")
            search_field = driver.find_element(By.ID, "ctl00_FldSearch")
            search_field.clear()
            search_field.send_keys(company_id)
            if not func_click_element_by_xpath(
                    "//span[contains(text(),'Mã số doanh nghiệp: " + str(company_id) + ";')]", driver=driver,
                    action=action):
                print("Red span not exits")
                time.sleep(3)
                return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
        except:
            print("Timed out waiting for page to load")
            time.sleep(3)
            return search_match_id(company_id=company_id, driver=driver, action=action, re_run=re_run - 1)
        return True


def process_to_download(company_id, driver, action):
    global re_run, downloaded, error_connection
    error_connection = False
    downloaded = False
    print("Re run : " + str(re_run))
    if re_run < 0:
        error_connection = True
        return
    if not search_match_id(company_id, driver=driver, action=action, re_run=10):
        print("Can't search company")
        return
    else:
        try:
            if go_to_cart(driver, action):
                if check_pdf_file():
                    try:
                        lastest_download = latest_download_file()
                        new_file = os.path.join(download_dir, str(company_id) + ".pdf")
                        os.rename(lastest_download, new_file)
                        downloaded = True
                        print("Download success")
                    except:
                        print("Can not rename file")
                        downloaded = False
                else:
                    print("Can't download")
                    downloaded = False
                return
            else:
                re_run = re_run - 1
                process_to_download(company_id, driver, action)
                return
        except:
            print("Error when go to cart")
            return


def go_to_cart(driver, action):
    global exist_document, downloading
    exist_document = False
    downloading = False
    if not func_click_element_by_id("ctl00_C_btnBuyProducts", driver=driver, action=action):
        try:
            driver.find_element(By.ID, "ctl00_C_LnkTab1")
            print("Don't have Danh muc san pham")
            return True
        except:
            print("Reload website")
            return False
    print("Have clicked Dat hang san pham")
    if not func_click_element_by_id("ctl00_C_RptAvailableProd_ctl04_LnkSubCatEGAZETTE", driver=driver, action=action):
        try:
            driver.find_element(By.XPATH, "//legend[text()='Các sản phẩm hiện có']")
            print("Can't click button Cong thong tin dang ky doanh nghiep")
            return True
        except:
            print("Reloading page")
            return False
    print("Have clicked Cong thong tin dang ky doanh nghiep")

    if not func_find_element_by_id("ctl00_C_RptAvailableProd_ctl04_LnkProduct", driver=driver):

        print("Fail")
        print("Trying to re search ID")
        return False
    else:
        links_bo_cao_dang_ky_thay_doi = driver.find_elements(By.XPATH,
                                                             "//a[contains(text(),'Bố cáo đăng ký thay đổi')]")  # Bo cao thong bao thay doi
        link = ''
        temp = datetime.strptime('01/01/01', "%d/%m/%y")
        if links_bo_cao_dang_ky_thay_doi:
            for item in links_bo_cao_dang_ky_thay_doi:
                if temp < datetime.strptime(item.text[:6] + item.text[8:10], "%d/%m/%y"):
                    temp = datetime.strptime(item.text[:6] + item.text[8:10], "%d/%m/%y")
                    link = item.text
        elif func_find_element_by_xpath("//a[contains(text(),'Bố cáo đăng ký mới')]", driver=driver):
            link_bo_cao_dang_ki_moi = driver.find_element(By.XPATH,
                                                          "//a[contains(text(),'Bố cáo đăng ký mới')]")
            link = link_bo_cao_dang_ki_moi.text
        else:
            print("Can not go to cart")
            return True
        print("Document : " + link)
        exist_document = True
        element_newest_link = driver.find_element(By.XPATH,
                                                  "//a[text()='" + link + "']")
        # ctl00_C_RptAvailableProd_ctl06_LnkProdAdd
        id_element_add_to_cart = element_newest_link.get_attribute('id')
        submit_element = id_element_add_to_cart[:38] + 'Add'
        action.click(element_newest_link).perform()
        if not func_click_element_by_id(submit_element, driver=driver, action=action):
            print("Fail")
            print("Trying to re search ID")
            return False
    if not func_find_element_by_id("ctl00_LnkShoppingCart", driver=driver):
        print("Check ctl00_LnkShoppingCart fail")
        print("Trying to re search ID")
        return False
    driver.execute_script("document.getElementById('ctl00_LnkShoppingCart').click();")
    if not func_click_element_by_id("ctl00_C_btnProceed", driver=driver, action=action):
        print("Check ctl00_C_btnProceed fail")
        print("Trying to re search ID")
        return False
    try:
        e = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_C_UC_BUYER_DETAILSEditCtl_FIRST_NAMEFld")))
        e.clear()
        e.send_keys("123")
        e = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_C_UC_BUYER_DETAILSEditCtl_ADDRESS_TEXTFld")))
        e.clear()
        e.send_keys("123")
        e = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_C_UC_BUYER_DETAILSEditCtl_EMAILFld")))
        e.clear()
        e.send_keys("123@gmail.com")
    except TimeoutException:
        print("Check add info fail")
        print("Trying to re search ID")
        return False
    if not func_click_element_by_id("ctl00_C_btnProceed", driver=driver, action=action):
        print("Check ctl00_C_btnProceed fail")
        print("Trying to re search ID")
        return False
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    driver.execute_script("document.getElementById('ctl00_C_agreeTermsChk').click();")
    driver.execute_script("document.getElementById('ctl00_C_btnSendPayment').click();")
    if not func_click_element_by_id("ctl00_C_CtlList2_ctl02_AttachmentGroup_ctl00_LnkGetFileActive", driver=driver,
                                    action=action):
        print("Fail to click ctl00_C_CtlList2_ctl02_AttachmentGroup_ctl00_LnkGetFileActive")
        return False
    print("Downloading")
    downloading = True
    return True


first_company = 3100
last_company = first_company + 100


def read_company_id(filename, first_company, last_company):
    company_list = []
    with open(filename, encoding="utf8") as f:  # "company_list_30_1.csv"
        reader = csv.reader(f)
        temp = 0
        for row in reader:
            if temp < first_company:
                temp = temp + 1
                continue
            if temp == last_company:
                break
            company_list.append(row[1])
            temp = temp + 1
    f.close()
    print(company_list)
    return company_list


company_list = []
with open( path+"company_list_30_1.csv", encoding="utf8") as f:  # "company_list_30_1.csv"
    reader = csv.reader(f)
    temp = 0
    for row in reader:
        if temp < first_company:
            temp = temp + 1
            continue
        if temp == last_company:
            break
        company_list.append(row[1])
        temp = temp + 1
f.close()

print(company_list)
print("Start count company list : " + str(len(company_list)))


def run_application():
    global company_list, re_run
    try:
        driver = webdriver.Chrome(options=chromeOptions)
        action = webdriver.ActionChains(driver)
        driver.get(url)
        # for item in company_list:
        while len(company_list) != 0:
            item = company_list[0]
            re_run = 4
            print(" ")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            count_of_file()
            print("ID company: " + str(item))
            process_to_download(str(item), driver, action)
            insert_log_to_database(item)
            company_list.remove(item)
            print("After remove : " + str(len(company_list)))
    except:
        driver.close()
        print("Driver has closed")
        time.sleep(5)
        run_application()


if __name__ == '__main__':
    run_application()
