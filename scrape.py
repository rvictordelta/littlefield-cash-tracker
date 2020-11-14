from datetime import datetime
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scrape(Group):
    ## login
    url = "http://op.responsive.net/lt/chicago/entry.html"
    driver = webdriver.Chrome()
    driver.get(url)

    elem = driver.find_element_by_name("id")
    elem.clear()
    elem.send_keys(Group.id)

    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(Group.pw)

    elem.send_keys(Keys.RETURN)

    while True:
        # loop starts here
        # navigate to the page
        prefix = "http://op.responsive.net/Littlefield/"
        url = prefix + 'LTStatus'
        driver.get(url)

        # get the text
        time.sleep(5)
        tag = driver.find_element_by_tag_name('center')
        text = tag.text

        # parse the text
        text_list = text.split(" ")
        disp_gday = int(text_list[1])
        balance = int(text_list[-1].replace(',', ''))
        td = datetime.now() - datetime(2020, 11, 9, 12)
        hours_elapsed = td.days * 24.0 + td.seconds / 3600.0
        gday_elapsed = round(hours_elapsed * 1.25 + 50, 2)
        out = [disp_gday, gday_elapsed, balance]

        # debug
        # print(disp_gday, balance, gday_elapsed)

        file_name = 'cash_data.csv'
        # read last
        with open(file_name, 'r', newline='') as read_obj:
            i = -1
            last = []
            while len(last) == 0 and i > -5:
                last = list(csv.reader(read_obj))[i]
                i = i - 1
            print(last, 'vs', out)

        # write latest
        # checks that this is a new time
        if len(out) > 0 and float(out[1]) > float(last[1]):
            with open(file_name, 'a+') as fp:
                wr = csv.writer(fp, lineterminator='\n')
                wr.writerow(out)

            # checks that this is a sufficient change
            chg_bool = int(out[2]) > int(last[2])  # handles no change and inv purchase
            chg_value = int(out[2]) - int(last[2])
            if chg_value < 500 and chg_bool and int(out[0]) == int(last[0]):
                # change it to 2
                time.sleep(1)
                print("****CHANGING IT TO CONTRACT 2!!!!******")
                url = prefix + 'OrdersForm'
                driver.get(url)
                driver.find_element_by_xpath("//input[@value='2'][@name='contractOpt']").click()
                driver.find_element_by_xpath("//input[@value='ok']").click()
                time.sleep(2)
                try:
                    elem = driver.find_element_by_name("pwd")
                    elem.clear()
                    elem.send_keys(Group.pw)
                    driver.find_element_by_xpath("//input[@value='confirm']").click()
                except:
                    print("Failed to switch to 2")

                # wait
                time.sleep(360)

                # change it to 3
                print("****CHANGING IT BACK TO CONTRACT 3!!!!******")
                url = prefix + 'OrdersForm'
                driver.get(url)
                driver.find_element_by_xpath("//input[@value='3'][@name='contractOpt']").click()
                driver.find_element_by_xpath("//input[@value='ok']").click()
                time.sleep(2)
                try:
                    elem = driver.find_element_by_name("pwd")
                    elem.clear()
                    elem.send_keys(Group.pw)
                    driver.find_element_by_xpath("//input[@value='confirm']").click()
                except:
                    print("********")
                    print("******** FAILED TO SWITCH BACK TO 3!!!!")
                    print("********")
            # print(last)
        time.sleep(5)




class Group:
    def __init__(self, name, id, pw, emails):
        self.name = name
        self.id = id
        self.pw = pw
        self.emails = emails


groups = []
with open("groups.csv") as csvfile:  # not tracked
    rows = csv.reader(csvfile)
    for row in rows:
        groups.append(Group(row[0], row[1], row[2], [x for x in row[3:]]))

group = groups[0]
scrape(group)
