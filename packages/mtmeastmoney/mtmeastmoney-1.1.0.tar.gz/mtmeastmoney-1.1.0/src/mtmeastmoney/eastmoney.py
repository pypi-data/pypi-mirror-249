import re
import json
import time
import random
from datetime import datetime, date

import requests

from .ocr import ocr_code


def post_order(session, url, data: dict):
    payloadHeader = {'Content-Type': 'application/json'}
    rsp = session.post(url, data=json.dumps(data), headers=payloadHeader)
    return rsp.json().get("Message", rsp.json())


class EastMoney:
    def __init__(self, userId=None, password=None, randomNumber=None, duration=15) -> None:
        self.host = "https://jywg.18.cn"
        self.session = requests.Session()
        self.userId = userId
        self.password = password
        self.login_duration = duration
        self.random_number = random.random() if randomNumber is None else randomNumber
        self.vertify_code_url = self.host + f"/Login/YZM?randNum={self.random_number}"
        self.validate_key = ""
        pass

    def get_validate_key(self):
        url = self.url_add_host("/Trade/XzsgBatPurchase")
        rsp = self.session.get(url)
        validatekey_list = re.findall("<input id=\"em_validatekey\"[^>]*value=\"([^\"]*)\"", rsp.text)
        if not len(validatekey_list):
            raise Exception("获取验证秘钥：登录失败")
        return validatekey_list[0]

    def login_once(self):
        data = {
            "userId": str(self.userId),
            "password": str(self.password),
            "randNumber": str(self.random_number),
            "identifyCode": ocr_code(self.vertify_code_url),
            "duration": str(self.login_duration),
            "authCode": "",
            "type": "Z"
        }
        url = self.host + "/Login/Authentication?validatekey="
        rsp = self.session.post(url, data)
        return "Uuid" in str(self.session.cookies)

    def login_retry(self, max_times=3, wait_second=5):
        for _ in range(max_times):
            if self.login_once():
                break
            else:
                time.sleep(wait_second)
        else:
            raise Exception("登录失败")
        self.validate_key = self.get_validate_key()

    def url_add_host(self, url):
        return (self.host + url) if "https" not in url else url

    def url_add_validate_key(self, url):
        url = self.url_add_host(url)
        url = (url + "?") if "?" not in url else url
        return url + f"validatekey={self.validate_key}"

    def query(self, url, data=None):
        if data is None:
            rsp = self.session.post(url)
        else:
            rsp = self.session.post(url, data=data)
        try:
            bonds_data = rsp.json()["Data"]
        except:
            raise Exception("获取信息：登录失败")
        return bonds_data

    @staticmethod
    def is_oneday_trade_day(date, stock_code="000001"):
        recent_trade_day = EastMoney.recent_trade_day(date, stock_code)
        return recent_trade_day == date

    @staticmethod
    def recent_trade_day(date, stock_code="000001"):
        klines_dict = EastMoney.query_stock_klines(stock_code, limit=1, end_date=date, is_data_frame=False)
        recent_trade_day = [i.split(",") for i in klines_dict["klines"]][-1][0]
        return recent_trade_day

    @staticmethod
    def query_stock_klines(stock_code, limit=1, end_date="2050-01-01", is_data_frame=False):
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        market = "1" if (stock_code.startswith("6") or stock_code.startswith("5")) else "0"
        payload = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "0",
            "lmt": limit,
            "secid": f"{market}.{stock_code}",
            "end": end_date.replace("-", ""),
        }
        resp = requests.get(url, params=payload).json()
        data = resp["data"]
        if not is_data_frame:
            return data.copy()
        else:
            import pandas as pd
            df = pd.DataFrame([i.split(",") for i in data["klines"]])
            df.columns = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
            df["股票代码"] = data["code"]
            df["股票名称"] = data["name"]
            df["市场代码"] = data["market"]
            return df
    @staticmethod
    def query_stock_current_info(stock_code):
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        market = "1" if (stock_code.startswith("6") or stock_code.startswith("5")) else "0"
        payload = {
            "fields": "f43,f44,f45,f46,f47,f48,f49,f161,f51,f52,f57,f58,f59",
            "secid": f"{market}.{stock_code}",
        }
        key_dict = {
            "f43": "最新价",
            "f44": "最高",
            "f45": "最低",
            "f46": "今开",
            "f47": "总手",
            "f48": "金额",
            "f49": "外盘",
            "f161": "内盘",
            "f51": "涨停",
            "f52": "跌停",
            "f57": "股票代码",
            "f58": "股票名称",
            "f59": "价格精度",
        }
        resp = requests.get(url, params=payload).json()
        data = resp["data"]
        data = {key_dict[key]: data[key] for key in data.keys()}
        return data.copy()

    def query_stock_trade_info(self, stock_code):
        url = self.url_add_validate_key("/Trade/GetAllNeedTradeInfo")
        return self.query(url, data={"stockCode": stock_code})["ZqInfo"]

    def query_trade_history(self, start_date, end_date, count=10000):
        url = self.url_add_validate_key("/Search/GetHisDealData")
        return self.query(url, data={"st": start_date, "et": end_date, "qqhs": count, "dws": ""})

    def query_market_convertible_bonds_list(self):
        url = self.url_add_validate_key("/Trade/GetConvertibleBondListV2")
        return self.query(url)

    def query_asset_stocks_list(self):
        url = self.url_add_validate_key("/Search/GetStockList")
        return self.query(url)

    def query_is_new_convertible_bond_available_today(self):
        today_str = date.today().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=10&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=PUBLIC_START_DATE"

        resp = self.session.get(url)
        result = re.search(today_str, resp.text)
        if result is not None:
            return True
        else:
            return False

    def order_(self, stock_code:str, amount:int, trade_type:str, price:float=None) -> dict: 
        """下单固定的数量

        Parameters
        ----------
        stock_code : str
            股票代码
        amount : int
            股票交易数量
        trade_type : str
            股票交易类型\  

        price : float, optional
            股票价格，限价需要, by default None

        交易类型可选: \ 
        0i 最优五档剩余撤销，卖出; \ 
        0d 最优五档剩余撤销，买入; \ 
        S 限价委托卖出; \ 
        B 限价委托买入; \ 

        Returns
        -------
        dict
            委托发送信息
        """

        url = self.url_add_validate_key("/Trade/SubmitTradeV2")
        if price is None:
            _infos = self.query_stock_current_info(stock_code)
            price_current = _infos["最新价"]/10**(_infos["价格精度"])
            price_limit_up = _infos["涨停"]/10**(_infos["价格精度"])
            price_limit_down = _infos["跌停"]/10**(_infos["价格精度"])
            format = "{:." + str(_infos["价格精度"]) + "f}"
            if trade_type == "0d":
                price = price_limit_up
            elif trade_type == "0i":
                price = price_limit_down
            else:
                raise Exception("下单失败：价格未指定")
        data = {
            "stockCode": stock_code,
            "price": format.format(price),
            "amount": int(amount),
            "tradeType": trade_type,
        }
        message = post_order(self.session, url, data)
        return message

    def scripts_buy_today_convertible_bonds(self):
        json_data = self.query_market_convertible_bonds_list()
        json_data = [bond for bond in json_data if bond["PURCHASEDATE"] == datetime.now().strftime("%Y%m%d")]
        if not len(json_data):
            return "今日无可买可转债"
        data = [{
            "StockCode": bond["SUBCODE"],
            "StockName": bond["SUBNAME"],
            "Price": bond['PARVALUE'],
            "Amount": int(bond['LIMITBUYVOL']),
            "TradeType": "B",
            "Market": bond['Market']
        } for bond in json_data]
        url = self.url_add_validate_key("/Trade/SubmitBatTradeV2")
        message = post_order(self.session, url, data)
        return message

    def scripts_sell_old_convertible_bonds(self):
        json_data = self.query_asset_stocks_list()
        json_data = [i for i in json_data if int(i["Kysl"]) > 0]
        if not len(json_data):
            return ""
        data = [{
            "stockCode": i["Zqdm"],
            "price": 80,
            "amount": int(i['Kysl']),
            "tradeType": "S",
            "zqmc": i["Zqmc"],
            "gddm": i["Gddm"],
            "market": i["Market"]
        } for i in json_data if "债" in i["Zqmc"] or "转2" in i["Zqmc"]]
        url = self.url_add_validate_key("/Trade/SubmitTradeV2")
        message_list = [
            f"卖单提交:" + str(i["zqmc"]) + str(i["amount"]) + str(post_order(self.session, url, i)) for i in data
            if i["amount"] > 0
        ]
        return "\n".join(message_list)

    def scripts_auto_trade_bonds(self, isSell=False):
        try:
            message = self.scripts_buy_today_convertible_bonds()
        except Exception as e:
            message = str(e)
        if isSell:
            message += "\n"
            try:
                message += self.scripts_sell_old_convertible_bonds()
            except Exception as e:
                message += str(e)
        if message.endswith("\n"):
            message = message[:-1]
        return message
