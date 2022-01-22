import requests as rs
from bs4 import BeautifulSoup
import json


def get_data_from_api(api_param):
    """
    模擬瀏覽器 向 api request, 回傳 回應的requests 的物件
    :param api_param: 內涵 stock_api_ur,post_data,headers


    """

    url = api_param["stock_api_url"]
    post_data = api_param["post_data"]
    headers = api_param["headers"]

    return_data = rs.post(url=url, data=post_data, headers=headers)
    return return_data


def dump_table_data_structure(raw_data):
    """
    將response 提取出股價，分成columns 與data 回傳

    :param raw_data:
    :return: 分成columns 與data 回傳
    """
    bs_parser = BeautifulSoup(raw_data.text, features="html.parser")
    table = bs_parser.find("table")
    thead = table.find('thead')
    th_all = thead.findAll('th')
    tbody = table.find('tbody')
    th_list = []
    for th in th_all:
        th_list.append(th.text)

    data_all = []
    for tr in tbody.findAll('tr'):
        row = []
        for td in tr.findAll('td'):
            row.append(td.text)
        data_all.append(row)

    return {"column": th_list, "data": data_all}


def dump_table_data_json_array(raw_data):
    """
    將接收到的response 提取出需要的部份，再轉成json string 回傳
    :param raw_data: requests.response data
    :return: json array string
    """
    bs_parser = BeautifulSoup(raw_data.text, features="html.parser")
    table = bs_parser.find("table")
    thead = table.find('thead')
    th_all = thead.findAll('th')
    tbody = table.find('tbody')
    return_list = []
    th_list = []
    for th in th_all:
        th_list.append(th.text)

    data_all = []
    for tr in tbody.findAll('tr'):
        row = {}
        for index, td_value in enumerate(tr.findAll('td')):
            key_ = th_list[index]

            row[key_] = td_value.text

        return_list.append(row)

    return return_list


def fetch_stock_price(url, start_date, end_date):
    """
    借由提供的url 及時間，組合出抓取模擬瀏覽器股價的function
    回傳一json formatted string
    :param url: string, 抓取的api url
    :param start_date: 抓取起點
    :param end_date: 抓取日期終點
    :return: json str
    """
    stock_api_param = {
        'stock_api_url': url,
        'headers': {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
        },
        'post_data': {
            'curr_id': 6408,
            'smlID': 1159963,
            'header': 'AAPL历史数据',
            'st_date': start_date,
            'end_date': end_date,
            'interval_sec': 'Daily',
            'sort_col': 'date',
            'sort_ord': 'ASC',
            'action': 'historical_data'
        }

    }
    raw_data = get_data_from_api(stock_api_param)

    data_parsed = dump_table_data_json_array(raw_data)

    return_json = json.dumps(data_parsed, ensure_ascii=False)

    return return_json


if __name__ == "__main__":
    stock_price_start_data = '2021/12/21'
    stock_price_end_date = '2022/01/21'
    stock_price_url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    print(fetch_stock_price(stock_price_url, stock_price_start_data, stock_price_end_date))
