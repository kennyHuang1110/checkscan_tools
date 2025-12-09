import os
import csv

# 精準比對 - 中國大陸常見應用
china_software_dict = {
    "360tray.exe": "奇虎360",
    "360safe.exe": "奇虎360",
    "QQ.exe": "騰訊",
    "WeChat.exe": "騰訊微信",
    "AliIM.exe": "阿里巴巴",
    "AliWangWang.exe": "阿里巴巴",
    "BaiduNetdisk.exe": "百度網盤",
    "YoudaoDict.exe": "網易有道",
    "SogouCloud.exe": "搜狗",
    "DingTalk.exe": "阿里巴巴釘釘",
    "KuGou.exe": "酷狗音樂",
    "Douyin.exe": "字節跳動抖音",
    "TikTok.exe": "字節跳動",
    "Pinduoduo.exe": "拼多多",
    "WPS.exe": "金山辦公",
    "Feishu.exe": "字節跳動飛書",
    "HuyaClient.exe": "虎牙直播",
    "YY.exe": "歡聚時代YY",
    "Xunlei.exe": "迅雷",
    "Weibo.exe": "新浪微博",
    "Xiaohongshu.exe": "小紅書RED",
    "Alipay.exe": "支付寶",
    "Taobao.exe": "淘寶",
    "JD.exe": "京東",
    "Meituan.exe": "美團",
    "Zhifubao.exe": "支付寶（別名）",
    "Baidu.exe": "百度",
    "iQIYI.exe": "愛奇藝",
    "TencentMeeting.exe": "騰訊會議",
    "TencentVideo.exe": "騰訊視頻",
    "TencentDocs.exe": "騰訊文檔",
    "KugouMusic.exe": "酷狗音樂",
    "KuwoMusic.exe": "酷我音樂",
    "Bilibili.exe": "嗶哩嗶哩",
    "MiHome.exe": "小米米家",
    "Huoshan.exe": "字節跳動火山小視頻",
    "Himalaya.exe": "喜馬拉雅FM",
    "UC.exe": "UC瀏覽器",
    "QQMusic.exe": "QQ音樂",
    "WeSing.exe": "全民K歌",
    "DynaUser.exe": "台灣金蝶"
}

# 精準比對 - 惡意程式清單
malware_software_dict = {
    "Mimikatz.exe": "密碼竊取工具",
    "CobaltStrike.exe": "滲透測試惡意版",
    "Meterpreter.exe": "Metasploit後門",
    "Empire.exe": "PowerShell後門",
    "Quasar.exe": "遠端控制木馬 (RAT)",
    "XMRig.exe": "挖礦木馬",
    "Gh0st.exe": "中國製遠控木馬",
    "PlugX.exe": "APT攻擊木馬",
    "NjRAT.exe": "常見 RAT 木馬",
    "NanoCore.exe": "資料竊取 RAT",
    "AsyncRAT.exe": "加密遠控 RAT",
    "Remcos.exe": "遠控木馬 Remcos",
    "DarkComet.exe": "知名 RAT 工具",
    "NetWire.exe": "跨平台 RAT",
    "FlawedAmmyy.exe": "APT挖礦木馬",
    "PoisonIvy.exe": "資料竊取木馬"
}

# 模糊比對 - 關鍵字比對
fuzzy_keywords = {
    "DeepSeek": "深度尋覓 DeepSeek"
}

def extract_tcpview_info(root_directory, output_csv_path):
    with open(output_csv_path, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['HostName', '可疑程式清單', '來源公司清單', '類別清單'])

    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == "tcpview_csv.log":
                host_name = os.path.basename(dirpath)
                print(f"🔎 正在掃描：{host_name}...")

                file_path = os.path.join(dirpath, filename)
                suspicious_programs = []
                suspicious_sources = []
                suspicious_types = []

                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            exe_name = parts[1]
                            exe_name_lower = exe_name.lower()

                            # 精準比對
                            if exe_name in china_software_dict:
                                if exe_name not in suspicious_programs:
                                    suspicious_programs.append(exe_name)
                                    suspicious_sources.append(china_software_dict[exe_name])
                                    suspicious_types.append("大陸軟體")
                            elif exe_name in malware_software_dict:
                                if exe_name not in suspicious_programs:
                                    suspicious_programs.append(exe_name)
                                    suspicious_sources.append(malware_software_dict[exe_name])
                                    suspicious_types.append("惡意程式")
                            else:
                                # 模糊比對
                                for keyword, company in fuzzy_keywords.items():
                                    if keyword.lower() in exe_name_lower:
                                        if exe_name not in suspicious_programs:
                                            suspicious_programs.append(exe_name)
                                            suspicious_sources.append(company)
                                            suspicious_types.append("大陸軟體（模糊比對）")

                with open(output_csv_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if suspicious_programs:
                        print(f"🚨 {host_name} 發現可疑程式：{';'.join(suspicious_programs)}")
                        writer.writerow([
                            host_name,
                            ';'.join(suspicious_programs),
                            ';'.join(suspicious_sources),
                            ';'.join(suspicious_types)
                        ])
                    else:
                        print(f"✅ {host_name} 沒有發現可疑程式。")
                        writer.writerow([host_name, "無發現", "無發現", "無發現"])

    print("✅ 全部掃描完成！結果已寫入", output_csv_path)

if __name__ == "__main__":
    root_directory = "檢視S"
    output_csv_path = "tcp_suspicious_with_company.csv"
    extract_tcpview_info(root_directory, output_csv_path)
