import time

import pandas as pd
from selenium import webdriver
import liblib
from selenium.webdriver.common.by import By


global_counter = 1
list1 = []

def start_driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1000, 1000)
    driver.implicitly_wait(5)
    return driver


def home_page(driver, link):
    driver.get(link)
    counter = 1
    time.sleep(3)
    while counter < 3:
        data = driver.find_elements(By.CLASS_NAME, "rest-row-image")
        for i in data:
            child = i.find_element(By.XPATH, 'a')
            link = child.get_attribute('href')
            table_info(link)
        next_page = driver.find_element(By.CSS_SELECTOR,
                                        '#results-pagination > li.pagination-li.pagination-arrow.pagination-arrow-next.pagination-border-arrow-next > a > span')
        next_page.click()
        print("CLICKED NEXT ")
        print(counter)
        time.sleep(5)
        counter += 1
    driver.close()
    return


def table_info(link):
    global global_counter
    driver = start_driver()
    driver.get(link)
    driver.execute_script('document.body.style.MozTransform = "scale(1.5)";')
    driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')
    time.sleep(3)
    try:
        view_button = driver.find_element(By.CSS_SELECTOR, '._4dd46ab2 > button:nth-child(1) > span:nth-child(1)')
        view_button.click()
        time.sleep(3)
        data = driver.find_element(By.ID, "overview-section").text
        data_list = data.split("\n")
    except Exception as e:
        data_list = another_view(driver)
    time.sleep(5)
    if not data_list:
        driver.close()
        return
    name = data_list[0]
    rate = data_list[1]
    num_of_reviews = data_list[2]
    starting_price = data_list[3]
    try:
        cuisins = data_list.index('Cuisines')
        cuisins = data_list[cuisins + 1]
    except:
        print("passed cuisin")

    data_dict = {"name": name, "rate": rate, "number of reviews": num_of_reviews, "starting price": starting_price,
                 "cuisins": cuisins}
    try:
        phone_num = data_list.index('Phone number')
        phone_num = data_list[phone_num + 1]
        data_dict["phone number"] = phone_num
    except Exception as e:
        print(e)
    try:
        dress_code = data_list.index('Dress code')
        dress_code = data_list[dress_code + 1]
        data_dict["dress code"] = dress_code
    except Exception as e:
        print(e)
    try:
        neighborhood = data_list.index('Neighborhood')
        neighborhood = data_list[neighborhood + 1]
        data_dict["neighborhood"] = neighborhood
    except Exception as e:
        print(e)
    try:
        parking = data_list.index('Parking details')
        parking = data_list[parking + 1]
        data_dict["parking details"] = parking
    except Exception as e:
        print(e)
    try:
        additional = data_list.index('Additional')
        additional = data_list[additional + 1]
        data_dict["additional"] = additional
    except Exception as e:
        print(e)
    try:
        cross_street = data_list.index('Cross street')
        cross_street = data_list[cross_street + 1]
        data_dict["cross street"] = cross_street
    except Exception as e:
        print(e)
    try:
        x = data_list.index("Phone number")
        y = data_list.index('Hours of operation')
        hours_of_operation = data_list[y + 1:x]
        data_dict["Hours of operation"] = hours_of_operation
    except Exception as e:
        print(e)
    try:
        chef = data_list.index('Executive chef')
        chef = data_list[chef + 1]
        data_dict["chef"] = chef
    except Exception as e:
        print(e)
    try:
        payment_options = data_list.index('Payment options')
        payment_options = data_list[payment_options + 1]
        data_dict["payment options"] = payment_options
    except Exception as e:
        print(e)
    try:
        dining_style = data_list.index('Dining style')
        dining_style = data_list[dining_style + 1]
        data_dict["dining style"] = dining_style
    except Exception as e:
        dining_style = driver.find_element(By.CSS_SELECTOR,
                                                  'div._1a072ecc:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)').text
        data_dict["dining style"] = dining_style
    try:
        location = data_list.index('Location')
        location = data_list[location + 1]
        data_dict["location"] = location
    except Exception as e:
        print(e)

    try:
        public_transit = data_list.index('Public transit')
        public_transit = data_list[public_transit + 1]
        data_dict["public transit"] = public_transit
    except Exception as e:
        print(e)
    try:
        website = data_list.index('Website')
        website = data_list[website + 1]
        data_dict["website"] = website
    except Exception as e:
        print(e)
    inset_to_list(data_dict)
    print(global_counter)
    global_counter += 1
    driver.close()


def another_view(driver):
    print('another view')
    try:
        view_button = driver.driver.find_element(By.CSS_SELECTOR, '._30NsS84PhDTAUQoIhEvgJv')
    except:
        return False
    view_button.click()
    data = driver.driver.find_element(By.CSS_SELECTOR, '.J8XO_TvPz9QpkpXALowZE > div:nth-child(1)').text
    data_list = data.split("\n")
    header = driver.driver.find_element(By.CSS_SELECTOR, '.fPuP2cAGoX-amQiocicDt').text
    header_list = header.split('\n')
    header_list.reverse()
    name = driver.driver.find_element(By.CSS_SELECTOR, '._2k5lAgEURCNcw88d3nAeQO').text

    for i in header_list:
        data_list.insert(0, i)
    data_list.insert(0, name)
    return data_list


def inset_to_list(dict):
    print(dict)
    list1.append(dict)

    # for key,value in dict.items():
    #     print(key+":"+value)
    return


def main():
    for i in liblib.helper_list:
        driver = start_driver()
        home_page(driver, i)

        df = pd.DataFrame(list1)
        df.to_csv("mydf.csv")


if __name__ == '__main__':
    main()
