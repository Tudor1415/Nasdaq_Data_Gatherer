import os
import json
import requests
error = {
    "Error Message": "Limit Reach . Please upgrade your plan or visit our documentation for more details at https://financialmodelingprep.com/developer/docs/pricing "
}
errors = []
for sym in os.listdir("../DATA/data_per_symbol/"):
    dict = json.loads(open(f"../DATA/data_per_symbol/{sym}/cash_flow_quarterly.json").read())
    if dict == error:
        errors.append(sym)

for i in errors:
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{i}?period=quarter&apikey=4da1ae466d65e86f140b6238a24acb74")
    data = json.loads(response.text)
    open(f"../DATA/data_per_symbol/{i}/cash_flow_quarterly.json", "w+").write(json.dumps(data))
    print(f"Done {i}")

