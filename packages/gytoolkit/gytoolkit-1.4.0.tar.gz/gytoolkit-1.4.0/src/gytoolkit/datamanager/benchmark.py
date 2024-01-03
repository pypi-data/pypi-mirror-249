import pandas as pd

BENCHMARK = {
    "沪深300": ("jq", ("000300.XSHG",)),
    "中证500": ("jq", ("000905.XSHG",)),
    "中证1000": ("jq", ("000852.XSHG",)),
    "商品指数": ("ak", ("nhci",)),
    "中证转债": ("ak", ("000832",)),
    "中证全债": ("ak", ("H11001",)),
    "排排网宏观策略指数": ("ppw", ("宏观策略",)),
    "排排网期权策略指数": ("ppw", ("期权策略",)),
    "排排网套利策略指数": ("ppw", ("量化套利",)),
    "排排网量化中性指数": ("ppw", ("股票市场中性",)),
}


class BenchmarkLoader:
    def __init__(
        self, ppwdbapi=None, jqdatasdk=None, akshare=None, preload=True
    ) -> None:
        if jqdatasdk:
            self.jq = jqdatasdk
        if ppwdbapi:
            self.ppw = ppwdbapi
        if akshare:
            self.ak = akshare

        self.loaded_bm = {}

        if preload:
            self.preload()

    def get_raw_benchmark(self, benchmark_name) -> pd.Series:
        if benchmark_name in self.loaded_bm.keys():
            bm_series = self.loaded_bm[benchmark_name]
        else:
            api, params = BENCHMARK.get(benchmark_name,["",""])
            if hasattr(self, api):
                func = getattr(self, "get_" + api)
                bm_series = func(*params)
            else:
                Warning(f"不支持的业绩基准{benchmark_name}")
                bm_series = pd.Series()
            self.loaded_bm[benchmark_name] = bm_series
        return bm_series

    def preload(self, benchmark=None):
        if benchmark == None:
            benchmark = BENCHMARK.keys()

        for b in benchmark:
            self.get_raw_benchmark(b)

    def get_benchmark(self, benchmarkdict)->pd.Series:
        benchmark_return_list = []
        for benchmark_name, weight in benchmarkdict.items():
            # 获得对应指数序列
            raw_benchmark = self.get_raw_benchmark(benchmark_name)
            if raw_benchmark.empty:
                Warning(f"缺失序列:{benchmark_name}")
                return pd.Series()
            # 获得加权收益率序列
            benchmark_return = raw_benchmark.pct_change()
            benchmark_return = benchmark_return.fillna(0)
            benchmark_return_list.append(weight * benchmark_return)
        # 按权重组合基准收益率序列
        benchmark_return = pd.concat(benchmark_return_list, axis=1).dropna().sum(axis=1)
        # 第一天基期为1
        benchmark_return.iloc[0] = 0
        # 重新构建业绩基准序列
        benchmark = benchmark_return.add(1).cumprod()
        return benchmark

    def get_jq(self, symbol, start_date=None, end_date=None) -> pd.Series:
        if start_date is None:
            start_date = "2010-01-01"
        if end_date is None:
            end_date = pd.Timestamp.today().strftime("%Y-%m-%d")
        return self.jq.get_price(symbol, start_date, end_date, fields="close")[
            "close"
        ].dropna()

    def get_ak(self, symbol, start_date=None, end_date=None):
        if symbol in ("000832", "H11001"):
            if start_date is None:
                start_date = "20100101"
            if end_date is None:
                end_date = pd.Timestamp.today().strftime("%Y%m%d")
            index = self.ak.stock_zh_index_hist_csindex(
                symbol=symbol, start_date=start_date, end_date=end_date
            )
            index = index.set_index(pd.to_datetime(index.日期))["收盘"]
        if symbol in ("nhci"):
            nhci = self.ak.futures_return_index_nh(symbol="NHCI").drop_duplicates()
            index = nhci.set_index(pd.to_datetime(nhci.date))["value"]
        return index

    def get_ppw(self, index_name: str, start_date=None, end_date=None) -> pd.Series:
        if start_date is None:
            start_date = "2010-01-01"
        if end_date is None:
            end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

        PPW_INDEX_ID = {
            "股票市场中性": "IN000002DA",
            "股票多空": "IN000002D9",
            "宏观策略": "IN000002DJ",
            "量化套利": "IN000002E1",
            "期权策略": "IN000002DH",
        }
        index_id = PPW_INDEX_ID.get(index_name)
        if index_id is None:
            raise ValueError(f"{index_name} is not supported.")

        index_data = self.ppw.get_index(
            index_id=index_id, start_date=start_date, end_date=end_date
        )
        return index_data.set_index("截止日期")["指数点位"]
