import requests
import pandas as pd

# 네이버 개발자센터에서 발급받은 ID와 Secret
client_id = "oVuchavnGKrySN6cspFN"
client_secret = "mU2534hTwK"

# 지역과 키워드 리스트
areas = ["강릉시", "고성군", "양양군"]
keywords = ["신축", "축제", "호텔", "착공", "오픈", "준공", "행사", "신규", "대회", "콘서트"]

# 검색어 조합 만들기
search_queries = [f"{area} {keyword}" for area in areas for keyword in keywords]

def search_naver_news(query, display=20, start=1, sort='date'):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,  # 최대 100개까지 가능
        "start": start,      # 시작 위치
        "sort": sort         # date: 최신순 / sim: 관련도순
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        return result['items']
    else:
        print("Error:", response.status_code)
        return []

if __name__ == "__main__":
    all_news = []

    for query in search_queries:
        print(f"🔎 검색어: {query}")
        news_items = search_naver_news(query, display=20)  # 한 검색어당 20개 가져오기
        for item in news_items:
            all_news.append({
                "search_query": query,
                "title": item['title'],
                "description": item['description'],
                "link": item['link'],
                "pubDate": item['pubDate']
            })

if all_news:
    df = pd.DataFrame(all_news)
    df.to_csv('filtered_news_full.csv', index=False, encoding='utf-8-sig')
    print("✅ 뉴스 수집 완료! filtered_news_full.csv 파일 생성됨.")
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    from_email = 'sunboya1615@gmail.com'  # 너의 Gmail 주소
    to_email = 'stronglee2@naver.com'         # 받을 사람 이메일
    app_password = 'dlbh yxrc aazn xbrd'  # 방금 만든 앱 비밀번호

# 메일 구성
    msg = MIMEMultipart()
    msg['Subject'] = '자동 뉴스 리포트 (CSV 첨부)'
    msg['From'] = from_email
    msg['To'] = to_email

# 본문 텍스트
    body = MIMEText('자동 수집된 뉴스 리포트를 첨부합니다.', 'plain')
    msg.attach(body)

# CSV 첨부
    filename = 'filtered_news_full.csv'
    with open(filename, 'rb') as f:
        part = MIMEApplication(f.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

# Gmail SMTP 전송
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_email, app_password)
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()
else:
    print("❌ 조건에 맞는 뉴스가 없습니다.")
