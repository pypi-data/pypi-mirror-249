# import sharetop as sp

from sharetop import sp_prepare
from sharetop import fund

token = "**"

# fund_list = fund.get_fund_open_rank(token, symbol="股票型")
# sp_obj = sp_prepare.BasicTop(token)
# r = sp_obj.common_exec_func("stock_to_list_data", {"limit": 10, "is_explain": True})
#
# print(r.to_dict("records"))

# r2 = sp_obj.common_exec_func("stock_to_list_data", {"limit": 10, "is_explain": False})

fund_base_list = fund.get_fund_codes(token, ft='zs')

print(fund_base_list)