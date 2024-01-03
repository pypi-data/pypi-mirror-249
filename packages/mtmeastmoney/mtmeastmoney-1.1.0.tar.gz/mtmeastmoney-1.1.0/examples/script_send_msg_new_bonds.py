import os
import ssl

import pandas as pd
from mtmtool.notify import send
from mtmtool.log import stream_logger
from mtmeastmoney.eastmoney import EastMoney


os.chdir(os.path.dirname(os.path.abspath(__file__)))
ssl._create_default_https_context = ssl._create_unverified_context()
logger = stream_logger("newbonds")


if __name__ == "__main__":
    df_users_autobonds = pd.read_csv("users_autobonds.csv")
    is_new_convertible_bond_available_today = EastMoney().query_is_new_convertible_bond_available_today()

    if is_new_convertible_bond_available_today:
        for idx, row in df_users_autobonds.iterrows():
            if row["isNewBondMsgSend"] == False:
                continue
            else:
                message = send("今日新债", row["MsgToken"], row["MsgPlatform"], title="可转债打新")
                logger.info(row["username"] + "->" + message)
    else:
        logger.info("今日无新可转债上市")
