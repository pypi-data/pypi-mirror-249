from time import sleep

def dummy_send(driver, xpath, word, delay):    
    for c in word:
        driver.find_element('xpath',xpath).send_keys(c)
        sleep(delay)