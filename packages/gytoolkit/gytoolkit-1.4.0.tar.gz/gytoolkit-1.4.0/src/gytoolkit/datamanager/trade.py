from typing import Union, List, Literal
import pandas as pd
from glob import glob
from .dataloader import BaseDataLoader
from .constants import TradeData
from functools import lru_cache

cols = [
    "client_id",
    "prodcode",
    "date",
    "type",
    "amount",
    "shares",
    "divmod",
]

index_col = ["client_id", "prodcode", "date", "type"]


class TradeLoader(BaseDataLoader):
    def __init__(self) -> None:
        super().__init__(TradeData)

    @lru_cache
    def load_otc(self):
        folder_path = self.source["otc"]
        file_paths = glob(folder_path + "/*.xlsx")
        otc_trade_list = []
        for file in file_paths:
            otc_trade_list.append(
                pd.read_excel(file, header=8)[:-1][
                    ["客户代码", "交易日期", "交易类别", "产品代码", "确认数量", "确认金额","分红方式"]
                ].drop_duplicates(keep="last")
            )

        otc_trade = pd.concat(otc_trade_list).drop_duplicates(keep="last")

        if not otc_trade.empty:
            col_map = {
                "客户代码": "client_id",
                "产品代码": "prodcode",
                "交易日期": "date",
                "交易类别": "type",
                "确认数量": "shares",
                "确认金额": "amount",
                "分红方式": "divmod",
            }
            otc_trade.rename(columns=col_map, inplace=True)

            otc_trade["date"] = pd.to_datetime(otc_trade["date"], format="mixed")

        return self.format_data(otc_trade, cols=cols, index_col=index_col)

    @lru_cache
    def load_local(self):
        file_paths = self.source["local"]
        local_trade_data = pd.read_excel(file_paths).drop_duplicates(keep="last")

        if not local_trade_data.empty:
            col_map = {
                "客户代码": "client_id",
                "产品代码": "prodcode",
                "交易日期": "date",
                "交易类别": "type",
                "确认数量": "shares",
                "确认金额": "amount",
                "分红方式": "divmod",
            }
            local_trade_data.rename(columns=col_map, inplace=True)

            local_trade_data["date"] = pd.to_datetime(
                local_trade_data["date"], format="mixed"
            )

        return self.format_data(local_trade_data, cols=cols, index_col=index_col)

    def filter(
        self,
        data: pd.DataFrame,
        client_id: Union[str, List[str]] = None,
        prodcode: Union[str, List[str]] = None,
        date: Union[str, pd.Timestamp] = None,
        type: Literal["110-认购", "111-申购", "112-赎回","129-分红设置"] = None,
        **kwargs
    ) -> pd.DataFrame:
        if data.empty:
            return data

        if client_id is not None:
            if isinstance(client_id, str) or isinstance(client_id, int):
                client_id = [client_id]
            data = data[data.index.get_level_values("client_id").isin(client_id)]

        if prodcode is not None:
            if isinstance(prodcode, str):
                prodcode = [prodcode]
            data = data[data.index.get_level_values("prodcode").isin(prodcode)]

        if date is not None:
            if isinstance(date, str):
                date = pd.Timestamp(date)
            data = data[data.index.get_level_values("date") == date]

        if type is not None:
            if isinstance(type, str):
                type = [type]
            data = data[data.index.get_level_values("type").isin(type)]

        return data

    def load(
        self,
        client_id: Union[str, List[str]] = None,
        prodcode: Union[str, List[str]] = None,
        date: Union[str, pd.Timestamp] = None,
        type: Literal["110-认购", "111-申购", "112-赎回","129-分红设置"] = None,
        df=True,
    ) -> Union[List[TradeData], pd.DataFrame]:
        return super().load(
            client_id=client_id, prodcode=prodcode, date=date, type=type, df=df
        )
