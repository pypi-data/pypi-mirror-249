# import sharetop as sp

from sharetop import sp_prepare
token = "**"
sp_obj = sp_prepare.BasicTop(token)
r = sp_obj.common_exec_func("stock_to_list_data", {"limit": 10, "is_explain": True})
#
# print(r.to_dict("records"))


# r2 = sp_obj.common_exec_func("stock_to_list_data", {"limit": 10, "is_explain": False})

print(r)