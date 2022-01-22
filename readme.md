# 抓取歷史股價

https://cn.investing.com/instruments/HistoricalDataAjax
###fetch_stock_price 
main function 分為2個step : 1. 抓取data 2. 將data 提取出必要資訊回傳  

### get_data_from_api
抓取資料function
###dump_table_data_structure
parser, 回傳一個json 物件，其中包含 columns 與 data
### dump_table_data_json_array
parser, 回傳一json string ，其中為一json array ，每一個item 含股價欄位與值
