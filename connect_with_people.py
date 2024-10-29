import time
import random
import json
import os
import argparse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str,
                    help='The CSV file containing LinkedIn URLs', default='linkedin_urls.csv')
args = parser.parse_args()

try:
    parsed_csv = pd.read_csv(args.file)
except FileNotFoundError:
    print(f"File {args.file} not found, please provide a valid path.")
    exit(1)

try:
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
except FileNotFoundError:
    cookies = []

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

time.sleep(1)

current_url = driver.current_url


if 'feed' not in current_url:
    print("Not in the feed page, logging in")

    driver.get('https://www.linkedin.com/login')

    linkedin_username = os.getenv('LINKEDIN_USERNAME')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    sign_in_button = driver.find_element(
        By.XPATH, '//button[@data-litms-control-urn="login-submit"]')

    username_input.send_keys(linkedin_username)
    time.sleep(1)

    password_input.send_keys(linkedin_password)
    time.sleep(1)

    sign_in_button.click()
    time.sleep(1)

cookies = driver.get_cookies()

with open("cookies.json", "w") as file:
    json.dump(cookies, file)


def get_user_name():
    return driver.find_element(By.XPATH, './/h1[contains(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]').text


def get_connect_button():
    return driver.find_element(
        By.XPATH, f'.//main//*[contains(@class, "artdeco-card")]//button[contains(@aria-label, "Invite {get_user_name()}")]')


def get_follow_button():
    return driver.find_element(
        By.XPATH, f'.//main//*[contains(@class, "artdeco-card")]//button[contains(@aria-label, "Follow {get_user_name()}")]')


def find_send_without_note_button():
    try:
        return driver.find_element(
            By.XPATH, './/button[contains(@aria-label, "Send without a note")][1]')
    except NoSuchElementException:
        return None


def find_action_button():
    try:
        connect_button = get_connect_button()

        return connect_button
    except NoSuchElementException:
        try:
            follow_button = get_follow_button()

            return follow_button
        except NoSuchElementException:
            return None


def is_connection():
    has_connect_button = False
    has_message_button = False

    try:
        get_connect_button()

        print("Connect button found")

        has_connect_button = True
    except NoSuchElementException:
        has_connect_button = False

        print("Connect button NOT found")

    try:
        driver.find_element(
            By.XPATH, './/main//*[contains(@class, "artdeco-card")]//button[contains(@aria-label, "Message")][1]')

        print("Message button found")

        has_message_button = True
    except NoSuchElementException:
        has_message_button = False

        print("Message button NOT found")

    return not has_connect_button and has_message_button


def is_following():
    try:
        driver.find_element(
            By.XPATH, f'.//main//*[contains(@class, "artdeco-card")]//button[contains(@aria-label, "Following {get_user_name()}")]')

        print("Following button found")

        return True
    except NoSuchElementException:
        print("Following button NOT found")

        return False


def is_to_follow():
    try:
        get_follow_button()

        print("Follow button found")

        return True
    except NoSuchElementException:
        print("Follow button NOT found")

        return False


def has_send_note_modal():
    try:
        driver.find_element(By.ID, 'send-invite-modal')

        print("Send note modal found")

        return True
    except NoSuchElementException:

        print("Send note modal NOT found")

        return False


try:

    for index, row in parsed_csv.iterrows():

        url = row['URL']
        driver.get(url)
        time.sleep(5)

        try:
            print("Trying to connect or follow:", url)
            print("")

            if is_connection() and not is_to_follow():
                print("Already connected, moving on to the next url")
                print("")
                continue

            if is_following():
                print("Already following, moving on to the next url")
                print("")
                continue

            button = find_action_button()
            time.sleep(1)

            if button is not None:
                button.click()

                if has_send_note_modal():
                    send_without_note_button = find_send_without_note_button()

                    if send_without_note_button is not None:
                        send_without_note_button.click()
                    else:
                        print(
                            "Could not find the send without note button, moving on to the next url")

                print("Action executed 💪")
                time.sleep(2)
            else:
                print(
                    "Could not find the connect neither the follow button, moving on to the next url")

            time_to_wait = random.uniform(0, 10)
            print(
                f"Waiting for {time_to_wait:.2f} seconds before moving to the next URL")
            time.sleep(time_to_wait)
            print("")

        except Exception as e:
            print(f"Could not connect with {url}: {e}")
            print("")


finally:
    driver.quit()
