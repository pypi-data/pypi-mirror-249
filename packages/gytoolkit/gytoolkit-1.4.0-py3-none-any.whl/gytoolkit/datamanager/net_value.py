import pandas as pd
from typing import List, Union, Dict
from functools import lru_cache
from .constants import NetValueData
from .dataloader import BaseDataLoader
from gytoolkit import ppwdbapi
from gytoolkit.mailparser import MailClient
from gytoolkit.utils import load_netvalue, save_netvalue
from .utils import get_otc_nv, ppwnvformatter


class NetValueLoader(BaseDataLoader):
    """
    净值数据来源(按优先级):
        1-邮箱解析
        2-ppwdbapi
        3-otc
        4-本地手工净值
    """

    def __init__(self) -> None:
        self.mailapi = {}
        super().__init__(NetValueData)

    def set_mailapi(self, username, password):
        mailclient = MailClient(username=username, password=password)
        self.mailapi[username] = mailclient

    def update_local_mail(self, depth=50):
        if "mail" not in self.source.keys():
            raise ValueError("Please set local mail file first.")

        local_mail_file = self.source["mail"]
        mail_api = self.mailapi
        if len(mail_api) > 0:
            for mailaccount, api in mail_api.items():
                headers = api.get_mail_header(lookin_depth=depth)
                nv_list = api.parse_mails(headers)
                save_netvalue(nv_list, local_mail_file)
        self.set_local_mail(local_mail_file)

    @lru_cache
    def load_mail(self):
        return load_netvalue(self.source["mail"], df=True)

    @lru_cache
    def load_local(self):
        return load_netvalue(self.source["local"], df=True)

    @lru_cache
    def load_otc(self):
        otc_folder = self.source["otc"]
        return get_otc_nv(otc_folder, df=True)

    def filter(
        self, nvdf: pd.DataFrame, reg_ids=None, start_date=None, end_date=None, **kwargs
    ):
        if nvdf.empty:
            return nvdf

        if reg_ids is not None:
            if isinstance(reg_ids, str):
                reg_ids = [reg_ids]
            nvdf = nvdf[nvdf.index.get_level_values("prodcode").isin(reg_ids)]
        if start_date:
            nvdf = nvdf[nvdf.index.get_level_values("date") >= start_date]
        if end_date:
            nvdf = nvdf[nvdf.index.get_level_values("date") <= end_date]

        return nvdf

    def load_ppw(
        self,
        reg_ids=None,
        ppw_ids=None,
        start_date=None,
        end_date=None,
        code_mapper: pd.Series = None,
    ):
        api: ppwdbapi = self.source["ppw"]

        if ppw_ids is None:
            ppw_ids = []
        if isinstance(ppw_ids, str):
            ppw_ids = [ppw_ids]

        if reg_ids is not None:
            if isinstance(reg_ids, str):
                reg_ids = [reg_ids]
            if isinstance(reg_ids, list):
                reg_ids = [reg_id for reg_id in reg_ids if reg_id is not None]
            fund_ids = api.get_fund(reg_ids=reg_ids).index.to_list()
            ppw_ids.extend(fund_ids)

            if code_mapper is not None:
                ppw_ids.extend(code_mapper[code_mapper.isin(reg_ids)].index.tolist())

        ppw_ids = list(set(ppw_ids))
        if len(ppw_ids) == 0 and reg_ids is None:
            ppw_ids = None
        raw_ppwnv = api.get_netvalue(ppw_ids, start_date, end_date)
        ppwnv = ppwnvformatter(raw_ppwnv, code_mapper=code_mapper, df=True)
        return ppwnv

    def load(
        self,
        reg_ids=None,
        ppw_ids=None,
        start_date=None,
        end_date=None,
        code_mapper=None,
        df=True,
    ) -> Union[List[NetValueData], pd.DataFrame]:
        return super().load(
            reg_ids=reg_ids,
            ppw_ids=ppw_ids,
            start_date=start_date,
            end_date=end_date,
            code_mapper=code_mapper,
            df=df,
        )

    # def set_local_mail(self, local_mail_file):
    #     self.local_mail_file = local_mail_file
    #     self.get_local.cache_clear()

    # def set_local_otc(self, otc_folder_path):
    #     self.otc_folder_path = otc_folder_path
    #     self.get_local.cache_clear()

    # def set_addtional_file(self, additional_file):
    #     self.additional_file = additional_file
    #     self.get_local.cache_clear()

    # @lru_cache
    # def get_local(
    #     self, df=True
    # ) -> List[NetValueData]:
    #     # 按优先级顺序读取数据
    #     # 1、OTC数据
    #     if hasattr(self, "otc_folder_path"):
    #         otc_netvalues = get_otc_nv(self.otc_folder_path, df=True)
    #     else:
    #         otc_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
    #     # 2、手工净值
    #     if hasattr(self, "additional_file"):
    #         addtional_netvalues = load_netvalue(self.additional_file, df=True)
    #     else:
    #         addtional_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
    #     # 3、邮箱数据
    #     if hasattr(self, "local_mail_file"):
    #         mail_netvalues = load_netvalue(self.local_mail_file, df=True)
    #     else:
    #         mail_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     local_netvalues = otc_netvalues.combine_first(addtional_netvalues)
    #     local_netvalues = local_netvalues.combine_first(mail_netvalues)

    #     if df:
    #         return local_netvalues
    #     else:
    #         return [NetValueData(**row) for index, row in local_netvalues.reset_index().iterrows()]

    # def load(
    #     self,
    #     prodcode,
    #     df=True,
    # ) -> Union[List[NetValueData], pd.DataFrame]:
    #     local_netvalues = self.get_local()
    #     idx = pd.IndexSlice
    #     try:
    #         local_netvalue = local_netvalues.loc[idx[:, prodcode],]
    #     except:
    #         local_netvalue = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     ppwdbapi = self.api.get("ppwdbapi")
    #     if ppwdbapi:
    #         fund_info = ppwdbapi.get_fund(reg_ids=prodcode)
    #         ppwnv = ppwnvformatter(ppwdbapi.get_netvalue(fund_info.index))
    #     else:
    #         ppwnv = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     net_value = ppwnv.combine_first(local_netvalue)
    #     if df:
    #         return net_value
    #     else:
    #         return [NetValueData(**row) for index, row in net_value.reset_index().iterrows()]
