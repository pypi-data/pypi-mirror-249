import os
from itertools import product

import numpy as np
from mtmeastmoney import EastMoney
from mtmtool.io import read_yaml, read_json, write_json
from mtmtool.log import stream_logger


os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = stream_logger()
config = read_yaml("eastmoney_pwd.yml")
em = EastMoney(userId=config["username"], password=config["password"])
em.login_retry()

stock_list = em.query_asset_stocks_list()

obj_balance_stock_codes = ["513100", "159920", "159937"]

# zqdm: 证券代码; zxjg: 最新价格; zqsl: 证券数量; zqcb: 证券成本; zqsz: 证券市值; zqyj: 证券盈亏; zqykbl: 证券盈亏比例, ljyk: 累计盈亏
obj_stocks = [i for i in stock_list if i["Zqdm"] in obj_balance_stock_codes]
stocks_dict = {i["Zqdm"]: i for i in obj_stocks}

# 计算总盈亏
if os.path.exists("money.json"):
    money = read_json("money.json")["money"]
else:
    money = 0


total_profit = sum([float(i["Ljyk"]) for i in obj_stocks])
latest_worth = sum([float(i["Zxsz"]) for i in obj_stocks])
total_worth = latest_worth + money
logger.info(f"总盈亏: {total_profit}")

#
single_obj_worth = total_worth / len(obj_balance_stock_codes)  # 单个标的的目标市值
logger.info(f"单个标的的目标市值: {single_obj_worth}")


range_dict = {}
for stock_code, stock_info in stocks_dict.items():
    # 计算目标数量
    target_amount = single_obj_worth / float(stock_info["Zxjg"])
    # 计算目标数量的上下限
    a = int(target_amount / 100)
    target_amount_range = [(a + i) * 100 for i in range(-15, 15)]
    target_amount_range = [i for i in target_amount_range if i >= 0]
    range_dict[stock_code] = target_amount_range


stock_values = np.array([float(stock_info["Zxjg"]) for stock_code, stock_info in stocks_dict.items()])

min_diff = np.inf
obj_tuple = None
for i in product(*list(range_dict.values())):
    c = np.array(i) * stock_values
    if sum(c) >= total_worth:
        continue
    _diff = sum((c - single_obj_worth) ** 2)
    if _diff < min_diff:
        min_diff = _diff
        obj_tuple = list(i)

for idx, stock_code in enumerate(stocks_dict):
    stocks_dict[stock_code]["target_amount"] = obj_tuple[idx]
    change_amount = obj_tuple[idx] - int(stocks_dict[stock_code]["Zqsl"])
    name = stocks_dict[stock_code]["Zqmc"]
    if change_amount == 0:
        logger.info(f"不调整->{name}({stock_code}): {change_amount}, 目标数量: {obj_tuple[idx]}")
        continue
    if change_amount > 0:
        logger.info(f"买入->{name}({stock_code}): {change_amount}, 目标数量: {obj_tuple[idx]}")
        em.order_(stock_code, abs(change_amount), "0d")
    else:
        logger.info(f"卖出->{name}({stock_code}): {-change_amount}, 目标数量: {obj_tuple[idx]}")
        em.order_(stock_code, abs(change_amount), "0i")


money_used = (np.array(obj_tuple) * stock_values).sum()
logger.info(f"净值: {total_worth}, 已用: {money_used}")
write_json({"money": total_worth - money_used}, "money.json")
