from random import randint
import undetected_chromedriver as uc
from undetected_chromedriver.options import ChromeOptions
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# driver = uc.Chrome()

def set_value_with_event(element, value, driver):
    # Click to focus
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()
    
    # Clear the existing value
    driver.execute_script("arguments[0].value = '';", element)
    
    # Use JavaScript to simulate human typing
    driver.execute_script("""
    var setValue = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    var element = arguments[0];
    var value = arguments[1];
    
    setValue.call(element, value);
    
    var event = new Event('input', { bubbles: true });
    element.dispatchEvent(event);
    """, element, value)

def main():
    Selection = int(input('(1) Send Connection Requests \n(2) Withdraw all pending connections\nWhich would you like to do: '))
    # LoginUser = input('\nEnter your LinkedIn email: ')
    # LoginPass = input('\nEnter your LinkedIn Password: ')

    LoginUser = "umanggupta1103@gmail.com"
    LoginPass = "8sPK7Zx5M*Hdt8D"


    print('\nSigning in... (Takes about 10 seconds)')


    # Feel free to comment out the three lines below and uncomment the fourth one if you would like to watch the process!
    myoptions = ChromeOptions()
    myoptions.add_argument("--headless")
    driver = uc.Chrome(options=myoptions)
    # driver = uc.Chrome()
    
    # Opening LinkedIn Signinpage
    urltoSignInPage = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(urltoSignInPage)
    time.sleep(2)

    # Logging in
    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    password = driver.find_element(By.XPATH,"//input[@name='session_password']")

    username.send_keys(LoginUser)
    password.send_keys(LoginPass)
    time.sleep(2)
    submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # Login Process Complete.
    os.system('cls||clear')
    print('\nSuccessfully signed in!')

    if (Selection == 1):
        chose_Connect(driver)
    elif (Selection == 2):
        chose_withdraw(driver)

def chose_Connect(driver):

    JobLink = input('\nEnter your job link: ')

    # Company = input('\nEnter company name: ')

    query = input('\nEnter query : ')

    ConnectionMessage = f"Hi,I am Umang, I found an opening at which fits my interests and skillsets. Would love if you can refer me!\nJD: {JobLink}\nMy portfolio: https://umangpt.com/"
    # ConnectionMessage = f"Hi,I am Umang, I have applied at Google through a referral for a SWE position , would love to connect and share my portfolio! \nJD: {JobLink}\nMy portfolio: https://umangpt.com/"

    print('\n Your message is: \n', ConnectionMessage)

    if(len(ConnectionMessage)>299):
        print('too long: ', len(ConnectionMessage))
        return


    # Keywords = []

    # KeywordNum = int(input('How many keywords would you like to use: '))

    # for x in range(KeywordNum):
    #     Keywords.append(input(f'Enter Keyword {x+1}: '))
        

    maxConnect = int(input('\nHow many connection requests would you like to send? (Stay below 50 to be safe): '))
    os.system('cls||clear')
    # Keywords = [w.replace(" ", "%20") for w in Keywords]
    # Keywords = str.join("%20", Keywords)

    
    i = 0
    # if program is crashing, increment K variable below by 5
    k = 1

    print("\nBeginning connection request process...\nThere is a delay between requests intentionally to bypass bot detections")
    while i < maxConnect:
        try:
            # Construct the URL for the search results page
            # urllink = f"https://www.linkedin.com/search/results/people/?&keywords={Keywords}&network=%5B%22S%22%2C%22O%22%5D&origin=SWITCH_SEARCH_VERTICAL&page={k}&sid=aiC&spellCorrectionEnabled=true"
            # urllink = f"https://www.linkedin.com/search/results/people/?currentCompany=%5B%22162479%22%5D&origin=FACETED_SEARCH&page={k}"
            # Load the search results page and wait for it to load
            # urllink = query
            urllink = query+f'&page={k}'
            driver.get(urllink)
            time.sleep(randint(4, 6))

            # Find all the Connect buttons on the page
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

            # Loop through all the Connect buttons and send connection requests
            for btn in connect_buttons:
                driver.execute_script("arguments[0].click();", btn)
                try: 
                    name = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/p/span/strong").text
                    print(f"Sending connection request to {name}")
                    time.sleep(randint(4, 5))
                    add_note = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
                    driver.execute_script("arguments[0].click();", add_note)

                    print(f"Adding a note to {name}")
                    time.sleep(randint(4, 5))

                    text_field = driver.find_element(By.XPATH, '//textarea[@id="custom-message"]')
                    print(f"Finding text field for {name}")
                    time.sleep(randint(2, 3))

                    set_value_with_event(text_field, ConnectionMessage, driver)
                    print(f"Setting text field for {name}")
                    time.sleep(randint(4, 4))
                    send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                    driver.execute_script("arguments[0].click();", send)
                    print(f"sending request {name}")

                    # close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    # driver.execute_script("arguments[0].click();", close)
                    time.sleep(2)
                except Exception as e:
                    print(f"Inner error occurred: {str(e)}")

            # If there are no more Connect buttons on the page, go to the next page
            if len(connect_buttons) == 0:
                k += 1
            else:
                # Update the counter for the number of connections made and go to the next page
                i += len(connect_buttons)
                k += 1

            # Print the total number of connection requests sent so far
            print(f"Connection Invitations sent = {i}, page = {k}")
            time.sleep(randint(4, 6))

            # Exit the loop if the maximum number of connections has been reached
            if i >= maxConnect:
                break

    # Handle any exceptions that may arise during the process
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def chose_withdraw(driver):
    i = 0
    urllink = "https://www.linkedin.com/notifications/?origin=SWITCH_SEARCH_VERTICAL&sid=aiC&filter=invitations_sent_people"
    driver.get(urllink)
    print('Withdrawing all current connection requests!\nPlease be aware that there is an intentional delay to avoid being banned as a bot.')
    while i < 400:
        time.sleep(2)
        all_buttons = driver.find_elements(By.XPATH,"//button/span/span[1]")    
        
        withdraw_buttons = [btn for btn in all_buttons if btn.text == "Withdraw"]

        for btn in withdraw_buttons:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(randint(6,20))
            send = driver.find_element(By.XPATH,"//button[@aria-label='Withdraw']")
            driver.execute_script("arguments[0].click();", send)
            time.sleep(randint(6,20))
        time.sleep(4)
        i+=len(withdraw_buttons)
        print("Connection Invitations withdrawn = ", i )
        more = driver.find_element(By.XPATH,"//button[@class='artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--3 artdeco-button--fluid artdeco-button--tertiary ember-view redesigned-experience__show-more-btn pv3']")
        driver.execute_script("arguments[0].click();", more)
            
    driver.quit()
    exit(0)

if __name__ == "__main__":
    main()