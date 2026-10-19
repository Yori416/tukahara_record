import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 💡 這裡目前放的是 Nijisanji 官方頻道的 ID 作為測試，你可以隨時改成你想追蹤的 VTuber 頻道 ID
CHANNEL_ID = "UC_x5XG1OV2P6uYZ5HEx9fyw" 
rss_url = f"https://youtube.com{CHANNEL_ID}"

try:
    # 讀取 YouTube RSS Feed
    response = urllib.request.urlopen(rss_url)
    data = response.read()
    root = ET.fromstring(data)
    
    events = []
    # 解析 XML 取得影片資訊
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
