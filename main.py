from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import json

PROMISED_DOWN = 150
PROMISED_UP = 10


class InternetSpeedTwitterBot:
    def __init__(self,data):
        self.email = data['email']
        self.password = data['password']
        self.username = data['username']
        self.driver = webdriver.Chrome(executable_path=data['driver_path'])
        self.down = 0
        self.up = 0
    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        sleep(5)
        accept_cookies = self.driver.find_element(By.ID, value="onetrust-accept-btn-handler").click()
        sleep(3)
        start_speed_test = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]')
        start_speed_test.click()
        sleep(60)

        download = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        download_speed = download.text
        upload = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
        upload_speed = upload.text
        if download_speed == '--' or upload_speed == '--':
            sleep(10)
        
        self.up = upload_speed
        self.down = download_speed

        print(self.down)
        print(self.up)

    def log_in_twitter(self):
        self.driver.get("https://twitter.com/")
        
        sleep(8)
        cookies = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div').click()
        sleep(4)
        sign_in = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a')
        sign_in.click()
        sleep(10)
        
        email_field = self.driver.find_element(By.TAG_NAME, value='input')
        email_field.send_keys(self.email)
        email_field.send_keys(Keys.ENTER)
        sleep(5)
        username_field = self.driver.find_element(By.TAG_NAME, value='input')
        username_field.send_keys(self.username)
        username_field.send_keys(Keys.ENTER)
        sleep(5)
        password_field = self.driver.find_element(By.XPATH, value='//input[@name="password"]')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)

    def tweet_complaint(self):
        message = f"Hey Internet Provider,why is my internet speed {self.down}down/{self.up}up when i pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_field = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
        tweet_field.send_keys(message)

        tweet_button = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        tweet_button.click()
        

if __name__ == "__main__":
    with open("config.json") as config_file:
        data = json.load(config_file)

    bot = InternetSpeedTwitterBot(data)
    bot.get_internet_speed()
    bot.log_in_twitter()
    sleep(10)
    bot.tweet_complaint()
    
