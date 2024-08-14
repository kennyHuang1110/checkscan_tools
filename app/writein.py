import pandas as pd
from dotenv import load_dotenv
import pandas as pd
import os

# 讀取CSV檔案
df1 = pd.read_csv(r'C:\Users\User\Desktop\檢視工具\檢視productlist_OFFICE\office.csv', encoding='utf-8')
df2 = pd.read_csv('檢視sysinfo.csv', encoding='utf-8')
df3 = pd.read_csv(r"C:\Users\User\Desktop\檢視工具\檢視antivirus\antivirus.csv", encoding='utf-8')

# 合併資料
merged_df = pd.merge(df1, df2, on='HostName', how='outer')
merged_df = pd.merge(merged_df, df3, on='HostName', how='outer')

merged_df = merged_df.fillna('None')

# 將結果寫入CSV檔案
merged_df.to_csv('merged_data.csv', index=False, encoding='utf-8-sig')
