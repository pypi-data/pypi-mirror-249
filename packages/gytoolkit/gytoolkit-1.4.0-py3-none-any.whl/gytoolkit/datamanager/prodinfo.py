from typing import List, Union,Dict
import glob
import pandas as pd
from gytoolkit import ppwdbapi
from .constants import ProdInfoData
from .dataloader import BaseDataLoader
from .utils import benchmark_to_dict
from functools import lru_cache

DEFAULT_STRATEGY_BENCHMARK_MAP = {
    "主观选股": "沪深300:1",
    "中证500指增": "中证500:1",
    "中证1000指增": "中证1000:1",
    "沪深300指增": "沪深300:1",
    "量化选股": "中证1000:1",
    "其它":"排排网量化中性指数:1"
}

cols = [
    "prodcode",
    "shortname",
    "strategy",
    "benchmark",
    "manager_id",
    "est_date",
]

index_col = "prodcode"


class ProdInfoLoader(BaseDataLoader):
    def __init__(self) -> None:
        super().__init__(ProdInfoData)

    @lru_cache
    def load_local(self) -> Union[List[ProdInfoData], pd.DataFrame]:
        folder_path = self.source["local"]
        file_paths = glob.glob(folder_path + "/*.xlsx")
        local_prodinfo_list = []
        for file in file_paths:
            local_prodinfo_list.append(
                pd.read_excel(file)[["产品代码", "产品简称", "投资策略", "业绩基准", "运作时间","管理人备案编码"]].drop_duplicates(keep="last")
            )

        local_prodinfo = pd.concat(local_prodinfo_list).drop_duplicates(subset="产品代码",keep="last")
        local_prodinfo.业绩基准 = local_prodinfo.业绩基准.apply(benchmark_to_dict)
        local_prodinfo.运作时间 = pd.to_datetime(local_prodinfo.运作时间,format="mixed")
        
        if not local_prodinfo.empty:
            col_map = {
                "产品代码": "prodcode",
                "产品简称": "shortname",
                "投资策略": "strategy",
                "业绩基准": "benchmark",
                "运作时间": "est_date",
                "管理人备案编码":"manager_id",
            }
            local_prodinfo.rename(columns=col_map, inplace=True)

        return self.format_data(local_prodinfo, cols=cols, index_col=index_col)

    def filter(
        self,
        data: pd.DataFrame,
        names: Union[str, List[str]] = None,
        types: Union[str, List[str]] = "私募证券",
        reg_ids: Union[str, List[str]] = None,
        est_start: Union[str, pd.Timestamp] = None,
        est_end: Union[str, pd.Timestamp] = None,
        strategies: Union[str, List[str]] = None,
        second_strategies: Union[str, List[str]] = None,
        third_strategies: Union[str, List[str]] = None,
        company_names: Union[str, List[str]] = None,
        company_reg_ids: Union[str, List[str]] = None,
        status: Union[str, List[str]] = None,
        managers: Union[str, List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        if data.empty:
            return data

        if names:
            if isinstance(names, str):
                names = [names]
            data = data[data["shortname"].isin(names)]

        if reg_ids:
            if isinstance(reg_ids, str):
                reg_ids = [reg_ids]
            data = data[data.index.isin(reg_ids)]
        
        if third_strategies:
            if isinstance(third_strategies, str):
                third_strategies = [third_strategies]
            data = data[data["strategy"].isin(third_strategies)]
        
        return data

    def load_ppw(
        self,
        names: Union[str, List[str]] = None,
        types: Union[str, List[str]] = "私募证券",
        reg_ids: Union[str, List[str]] = None,
        est_start: Union[str, pd.Timestamp] = None,
        est_end: Union[str, pd.Timestamp] = None,
        strategies: Union[str, List[str]] = None,
        second_strategies: Union[str, List[str]] = None,
        third_strategies: Union[str, List[str]] = None,
        company_names: Union[str, List[str]] = None,
        company_reg_ids: Union[str, List[str]] = None,
        status: Union[str, List[str]] = None,
        managers: Union[str, List[str]] = None,
        strategy_benchmark_map: Dict[str,str] = None,
    ) -> pd.DataFrame:
        api: ppwdbapi = self.source["ppw"]
        products_info = api.get_fund(
            names=names,
            types=types,
            reg_ids=reg_ids,
            est_start=est_start,
            est_end=est_end,
            strategies=strategies,
            second_strategies=second_strategies,
            third_strategies=third_strategies,
            company_names=company_names,
            company_reg_ids=company_reg_ids,
            status=status,
            managers=managers,
        )

        if not products_info.empty:
            STRATEGY_BENCHMARK_MAP = DEFAULT_STRATEGY_BENCHMARK_MAP.copy()
            if strategy_benchmark_map:
                STRATEGY_BENCHMARK_MAP.update(strategy_benchmark_map)
            products_info["业绩基准"] = products_info.三级策略.map(STRATEGY_BENCHMARK_MAP).fillna("沪深300:1")
            products_info.业绩基准 = products_info.业绩基准.apply(benchmark_to_dict)

            col_map = {
                "备案编码": "prodcode",
                "产品简称": "shortname",
                "三级策略": "strategy",
                "业绩基准": "benchmark",
                "成立日期": "est_date",
                "管理人备案编码":"manager_id",
            }
            products_info.rename(columns=col_map, inplace=True)
        return self.format_data(products_info, cols=cols, index_col=index_col)

    def load(
        self,
        names: Union[str, List[str]] = None,
        types: Union[str, List[str]] = "私募证券",
        reg_ids: Union[str, List[str]] = None,
        est_start: Union[str, pd.Timestamp] = None,
        est_end: Union[str, pd.Timestamp] = None,
        strategies: Union[str, List[str]] = None,
        second_strategies: Union[str, List[str]] = None,
        third_strategies: Union[str, List[str]] = None,
        company_names: Union[str, List[str]] = None,
        company_reg_ids: Union[str, List[str]] = None,
        status: Union[str, List[str]] = None,
        managers: Union[str, List[str]] = None,
        strategy_benchmark_map: Dict[str,str] = None,
        df=True,
    ) -> Union[List[ProdInfoData], pd.DataFrame]:
        return super().load(
            names=names,
            types=types,
            reg_ids=reg_ids,
            est_start=est_start,
            est_end=est_end,
            strategies=strategies,
            second_strategies=second_strategies,
            third_strategies=third_strategies,
            company_names=company_names,
            company_reg_ids=company_reg_ids,
            status=status,
            managers=managers,
            strategy_benchmark_map = strategy_benchmark_map,
            df=df,
        )
