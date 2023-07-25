import requests
from bs4 import BeautifulSoup
import concurrent.futures
from requests.exceptions import ConnectTimeout, ReadTimeout, ProxyError
import csv
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

# Check status code

time = []
list_up = []
list_timeout = []
list_down = []
timeout = 60

def read_file(file_name):
    results = []
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.readlines()
    for line in content:
        results.append(line.strip())        
    return results

def check_status_code(list_url):
    for url in list_url:
        try:
            response = requests.get(url=url, timeout=timeout)
            if response.status_code in range(100, 400):
                list_up.append(url)
            elif response.status_code in range(400, 600):
                list_down.append(url)
        except (ConnectTimeout, ReadTimeout):
            list_timeout.append(url)

def show_state():
    for url in list_up:
        print('{} is up'.format(url))
    for url in list_down:
        print('{} is down'.format(url))
    for url in list_timeout:
        print('{} is timeout'.format(url))

# Check content tittle

def read_target_title():
    my_dict = {}
    with open('targets.txt', 'r', encoding='utf-8') as file:
        # Read each line of the file
        contents = file.readlines()
        for i in range(len(contents)):
            if i % 2 == 0:
                key = contents[i].strip()
            elif i%2 != 0:
                my_dict[key] = contents[i].strip()
    return my_dict

def check_content_title(targets):
    for url in targets.keys():
        response = requests.get(url=url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        if title == targets[url]:
            print("{} same title".format(url))
        elif title != targets[url]:
            print("{} change title".format(url))

def open_file_proxy():
    proxylist = []
    portlist = []
    with open('proxylist.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            proxylist.append(row[0])
            portlist.append(row[1])
    return proxylist, portlist

def extract(proxy, port):
    try:
        response = requests.get(url='https://ipinfo.io', timeout=3, proxies={'http':proxy, 'https':proxy})
        print("{} is working".format(proxy))
    except (ProxyError):
        pass

    # print('debug end')

# Change IP


if __name__ == '__main__':
    proxylist, portlist = open_file_proxy()
    with concurrent.futures.ThreadPoolExecutor() as exector:
        exector.map(extract, proxylist, portlist)