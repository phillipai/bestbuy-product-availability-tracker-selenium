from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests


# Telegram alert
def telegram_bot_send_text(bot_message):
    bot_token = "INSERT BOT_TOKEN"
    bot_chatID = "INSERT CHATID"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID \
                + '&parse_mode=Markdown&text=' + bot_message

    bot_response = requests.get(send_text)
    return bot_response.json()


browser = webdriver.Chrome("INSERT CHROME DRIVER PATH")
browser.get("https://www.bestbuy.ca/en-ca/product/xbox-series-x-1tb-console/14964951")


# Input postal code to search nearby stores
input_location = browser.find_element(By.XPATH, value='//*[@id="postalCode"]')
input_location.send_keys("INSERT POSTAL CODE")
search_location = browser.find_element(By.XPATH,
                                       value='//*[@id="root"]/div/div[3]/div[2]/div[1]/div[2]/div[5]/div[3]/div/div[2]/div[2]/button[1]')
search_location.click()

# Continuous tracking
in_stock = False
while not in_stock:
    check_stock = browser.find_element(By.XPATH,
                                       value='//*[@id="root"]/div/div[3]/div[2]/div[1]/div[2]/div[5]/div[3]/div/div[2]/div[1]/p[1]').text
    if check_stock == 'Sold out in nearby stores':
        browser.implicitly_wait(10)
        browser.refresh()
    else:
        # Send alert
        product_name = browser.find_element(By.XPATH, value='//*[@id="root"]/div/div[3]/h1').text
        telegram_bot_send_text(f'🚨 {product_name} is available to purchase:\n{browser.current_url}')
        time.sleep(60)
        browser.refresh()
