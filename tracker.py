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
# Product page
browser.get("https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/15463567")

# Continuous tracking
in_stock = False
while not in_stock:
    current_stock = browser.find_element(By.XPATH,
                                         value='//*[@id="root"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[3]/div/div[1]/div[1]/p/span').text
    if current_stock == 'Sold out online':
        browser.implicitly_wait(10)
        browser.refresh()
    elif current_stock == 'Available to ship':
        # Send alert
        product_name = browser.find_element(By.XPATH, value='//*[@id="root"]/div/div[3]/h1').text
        telegram_bot_send_text(f'🚨 {product_name} is available to ship:\n{browser.current_url}')
        time.sleep(60)
