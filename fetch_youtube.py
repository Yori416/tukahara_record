import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 💡 塚原大地的 YouTube 頻道 ID
CHANNEL_ID = "UC9HYkiQZ1_b3J_F8gc12eaA" 
rss_url = f"https://www.youtube.com/@TsukaharaDaichi_Y4T4"

try:
    # 讀取 YouTube RSS Feed
    response = urllib.request.urlopen(rss_url)
    data = response.read()
    root = ET.fromstring(data)
    
    events = []
    # 解析 XML 取得影片資訊（使用完整正確的 Namespace）
    for entry in root.findall('{http://w3.org}entry'):
        title = entry.find('{http://w3.org}title').text
        video_id = entry.find('{http://youtube.com}videoId').text
        published = entry.find('{http://w3.org}published').text
        
        # 轉換成 FullCalendar 需要的格式
        events.append({
            "id": video_id,
            "title": title,
            "start": published,  # YouTube 直播或發布時間
            "url": f"https://youtube.com{video_id}"
        })
        
    # 儲存為 json 檔案讓網頁讀取
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print("成功更新 events.json")

except Exception as e:
    print(f"發生錯誤: {e}")
