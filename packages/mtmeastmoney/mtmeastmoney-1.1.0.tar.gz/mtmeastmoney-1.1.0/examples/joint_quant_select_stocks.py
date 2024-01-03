import requests
from requests.cookies import RequestsCookieJar
from mtmtool.io import read_yaml
import pandas as pd
from mtmeastmoney.jointquant import JointQuant
from mtmeastmoney.eastmoney import EastMoney
import os, glob
import datetime
from mtmtool.notify import telegram
import ssl

ssl._create_default_https_context = ssl._create_unverified_context()

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def totime(x):
    return datetime.datetime.strptime(x, "%Y-%m-%d")


if __name__ == "__main__":
    # 这个脚本在早晨8点运行，获取昨天的数据
    stock_history_file = "stocks.csv"
    today = pd.Timestamp.today("Asia/Shanghai").strftime("%Y-%m-%d")
    yesterday = (pd.Timestamp.today("Asia/Shanghai") - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    day_before_yesterday = (pd.Timestamp.today("Asia/Shanghai") - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    # 获取昨天的涨跌停数据
    if os.path.exists(stock_history_file) and EastMoney.is_oneday_trade_day(yesterday):
        df = pd.read_csv(stock_history_file, dtype=str)
        df_tail = df.tail(10).head(10)
        for idx, row in df_tail.iterrows():
            print(idx, row["股票代码"])
            data = EastMoney.query_stock_current_info(row["股票代码"])
            if data["涨停"] == data["最新价"]:
                df.loc[idx, "收盘涨停"] = "1"
                telegram(
                    text=f"{row['股票代码']} {row['股票名称']} 涨停",
                    token="5603924161:AAEWalTZhV4re9zZ-ozKiBtMdWYJv9taL7s|2048941980",
                    host="tg.mutum.top",
                )
        df.to_csv(stock_history_file, index=False)

    recent_trade_day_yyesterday = EastMoney.recent_trade_day(day_before_yesterday)
    # 判断昨天是否是交易日，且昨天是否是当月第一次运行(前天的最近交易日在上个月)
    flag = (
        EastMoney.is_oneday_trade_day(yesterday)
        and totime(recent_trade_day_yyesterday).month != totime(yesterday).month
    )
    if flag:
        # 获取聚宽选股策略选择的股票
        headers_file = "./cookie_jointquant.yml"
        jq = JointQuant(headers_file)
        is_login = jq.login_web(18801101503, "DBLdbl1998")
        print("登录是否成功:", is_login)
        file = "cookie_dama_select.yml"
        algorithmId, backtestId, backtestId_, tradeDays = jq.run_strategy(file, yesterday, yesterday)
        needSeconds = jq.until_strategy_finish(file, backtestId)
        print("策略编译运行时间:", needSeconds)
        stocks_log_list = jq.track_strategy_log(file, backtestId)
        flag_trade_day = "所选日期区间没有交易日" not in stocks_log_list[-1]
        if flag_trade_day:
            stocks_list = [i.split(" - INFO  - ") for i in stocks_log_list]
            df = pd.DataFrame(stocks_list, columns=["运行时间", "股票代码-聚宽"])
            df["股票代码"] = df["股票代码-聚宽"].apply(lambda x: x.split(".")[0])
            df["收盘涨停"] = 0
            df.index.name = "买入排序"
            df.reset_index(inplace=True)
            header = False if os.path.exists(stock_history_file) else True
            mode = "w" if header else "a"
            df.to_csv(stock_history_file, mode=mode, index=False, header=header)
            texts = []
            for idx, row in df.head(10).iterrows():
                text = f"{row['股票代码']} 持仓"
                texts.append(text)
            text = "\n".join(texts)
            telegram(text=text, token="5603924161:AAEWalTZhV4re9zZ-ozKiBtMdWYJv9taL7s|2048941980", host="tg.mutum.top")
