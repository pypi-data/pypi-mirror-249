import os
import ssl

import pandas as pd
from mtmtool.notify import send
from mtmtool.log import stream_logger
from mtmeastmoney.eastmoney import EastMoney
from mtmeastmoney.common import today


os.chdir(os.path.dirname(os.path.abspath(__file__)))
ssl._create_default_https_context = ssl._create_unverified_context()
logger = stream_logger("autobonds")


def trade_bonds(user_info):
    userId = user_info["userId"]
    em = EastMoney(userId, user_info["password"])
    em.login_retry()
    message = em.scripts_auto_trade_bonds(user_info["isAutoSell"] == True)
    message = str(user_info["username"]) + "-" + str(userId) + ":\n" + message.replace("</br>", "\n").strip()
    return message


if __name__ == "__main__":
    df_users_autobonds = pd.read_csv("users_autobonds.csv")
    df_users_eastmoney = pd.read_csv("users_eastmoney.csv")
    df_infos_autotrade = pd.read_csv("infos_autotrade.csv", dtype=str)

    is_new_convertible_bond_available_today = EastMoney().query_is_new_convertible_bond_available_today()

    df_infos_autotrade_today = df_infos_autotrade.query(f"date == '{today()}'")
    for idx, row in df_users_autobonds.iterrows():
        username = row["username"]
        flag_autobuy = row["isAutoBuy"] == True and is_new_convertible_bond_available_today
        flag_autosell = row["isAutoSell"] == True
        df_isSuccess = df_infos_autotrade_today.query(f"username == '{username}'").query("isSuccess == 'True'")
        if (flag_autobuy or flag_autosell) and not len(df_isSuccess):
            try:
                user_info = row.to_dict()
                _user_info = df_users_eastmoney.query(f"username == '{username}'").iloc[0].to_dict()
                user_info.update(_user_info)
                message = trade_bonds(user_info)
                if "登录失败" not in message:
                    _dict = {"username": username, "date": today(), "isSuccess": True}
                    _df = pd.DataFrame.from_dict(_dict, orient="index").T
                    _df.to_csv("infos_autotrade.csv", mode="a", header=None, index=False)
                logger.info(message)
                send(message, user_info["MsgToken"], user_info["MsgPlatform"], host="tg.mutum.top")
                logger.info(username + "->" + "成功!")
            except Exception as e:
                logger.info(username + "->" + str(e))
