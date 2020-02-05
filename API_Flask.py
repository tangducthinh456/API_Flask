from flask import Flask, request, flash, render_template, url_for, send_from_directory
import pickle
import time
import requests
import os
from selenium import webdriver
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from werkzeug.utils import redirect, secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ubuntu/PycharmProjects/API_Flask/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))

def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    url='https://ads.google.com/aw/keywordplanner/home?ocid=345197485&__u=1786116194&__c=6875589765&authuser=0' if url is None else url
    driver.get(url)
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)

def create_file(UPLOAD_FOLDER, filename):
    res = ['Keyword']
    with open(UPLOAD_FOLDER + '/' + filename, 'r', encoding='utf-16', errors='ignore') as file:
        csv_read = csv.reader(file, delimiter='\t')

        for i, line in enumerate(csv_read):
            if i < 3:
                continue
            res.append(line[0])
    with open(UPLOAD_FOLDER + '/upload.csv', 'w', encoding='utf-16') as file:
        for i in res:
            file.write(i + '\n')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploaded_file():
    if request.method == 'POST':
        text = request.form['text']

        filename = handle_data(text)
        os.remove(UPLOAD_FOLDER + '/upload.csv')

        return download(filename)

            #    os.remove(UPLOAD_FOLDER + '/' + file.filename)
            #    filename_download = filename_download.replace('.crdownload', '')

            #return download(filename_download)
            #os.remove('/home/ubuntu/PycharmProjects/API_Flask/UPLOAD_FOLDER/' + filename_download)

def download(filename):

    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)



def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)

def handle_data(text):

    #import pdb;pdb.set_trace()
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": UPLOAD_FOLDER}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--window-size=1920,1080")
    #options.add_argument('headless')

    location = '/home/ubuntu/PycharmProjects/API_Flask/cookies.pkl'

    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome('/home/ubuntu/PycharmProjects/helllo/driver/chromedriver', options=options)

    #enable_download_in_headless_chrome(driver, UPLOAD_FOLDER)

    #load_cookies(driver, '/home/ubuntu/PycharmProjects/cookies.txt')
    #import pdb; pdb.set_trace()
    driver.get("https://ads.google.com/intl/en_VN/home/")

    get_start = driver.find_element_by_xpath('//div[@class="inner-wrapper"]/a')
    driver.get(get_start.get_attribute('href'))

    username = driver.find_element_by_xpath('//input[@type="email"]')
    username.send_keys("thinhtd@kalapa.vn")

    '''page_source = driver.page_source
    file = open('/home/hiepnt/API_FLASK/context.html', 'w', encoding='utf-8') 
        file.write(page_source);
'''
    #next = driver.find_element_by_id('next')
    next = driver.find_element_by_id('identifierNext')
    #driver.save_screenshot("screeload_cookies('/home/ubuntu/PycharmProjects')nshot.png")

    #sub = driver.find_element_by_id('submit')

    #findId = driver.find_element_by_id('logincaptcha')
    #findId.send_keys('excierbing')
    #sub.click()



    next.click()

    time.sleep(2)


    password = driver.find_element_by_xpath('//input[@type="password"]')
    password.send_keys('Matkhau****')
    #next2 = driver.find_element_by_id('signIn')
    next2 = driver.find_element_by_id('passwordNext')
    next2.click()

    time.sleep(2)
    import pdb;pdb.set_trace();



    #pickle.dump(driver.get_cookies(), open('/home/ubuntu/PycharmProjects' + '/cookies.txt', "w"))

    before = os.listdir(UPLOAD_FOLDER)

    import pdb;pdb.set_trace()
    #save_cookies(driver, '/home/ubuntu/PycharmProjects/cookies.txt')

    driver.get('https://ads.google.com/aw/keywordplanner/home?ocid=345197485&__u=1786116194&__c=6875589765&authuser=0')

    time.sleep(4)
    # import pdb;pdb.set_trace()
    from selenium.webdriver.common.action_chains import ActionChains

    receive_predict = driver.find_element_by_class_name('card-frame')
    ActionChains(driver).move_to_element(receive_predict).click(receive_predict).perform()
    #search_box = driver.find_element_by_link_text('Start with a website')
    search_box = driver.find_elements_by_class_name('tab-button')
    search_box[1].click()
    fill = driver.find_element_by_class_name('input')
    fill.send_keys(text)
    button = driver.find_element_by_class_name('get-results-button')
    button.click()
    button = driver.find_element_by_class_name('download')
    button.click()

    import pdb;pdb.set_trace()
    driver.get('https://ads.google.com/aw/keywordplanner/home?ocid=345197485&__u=1786116194&__c=6875589765&authuser=0')
    receive_predict = driver.find_element_by_class_name('forecasts-card')


    ActionChains(driver).move_to_element(receive_predict).click(receive_predict).perform()

    # import pdb;pdb.set_trace()

    send_file = driver.find_element_by_class_name('upload-button')
    time.sleep(2)
    ActionChains(driver).move_to_element(send_file).click(send_file).perform()

    choose_file = driver.find_element_by_xpath('//material-icon[@aria-label="Edit file"]')
    ActionChains(driver).move_to_element(choose_file).click(choose_file).perform()


    # subprocess.call("C:\\Users\\Dell\\Desktop\\script.exe")
    # import pdb;pdb.set_trace()
    time.sleep(1)
    after = os.listdir(UPLOAD_FOLDER)
    change = set(after) - set(before)
    filename = change.pop()

    create_file(UPLOAD_FOLDER, filename)



    # Fetch file input element
    fileInput = driver.find_element_by_xpath("//input[@type='file']")
    import pdb;pdb.set_trace()
    #  Execute Javascript to reveal the element
    driver.execute_script("arguments[0].style.display = 'block';", fileInput)

    # Send keys to file input
    fileInput.send_keys(UPLOAD_FOLDER + "/upload.csv")

    time.sleep(1)
    submit = driver.find_element_by_class_name('save-button')
    submit.click()
    time.sleep(20)
    download = driver.find_element_by_class_name('download')
    time.sleep(1)
    before = os.listdir(UPLOAD_FOLDER)
    ActionChains(driver).move_to_element(download).click(download).perform()

    download = driver.find_element_by_class_name('menu-item-label')
    ActionChains(driver).move_to_element(download).click(download).perform()
    time.sleep(10)
    after = os.listdir(UPLOAD_FOLDER)
    change = set(after) - set(before)
    filename_handle = change.pop()
    os.remove(UPLOAD_FOLDER + '/' + filename)
    driver.quit()

    return filename_handle


    try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 50)

        # You should see "cheese! - Google Search"
        print(driver.title)

    finally:
        driver.quit()


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()

