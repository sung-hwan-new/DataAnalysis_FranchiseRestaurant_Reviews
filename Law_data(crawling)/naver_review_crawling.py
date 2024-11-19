import time
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import csv

def read_data():
    store_info = []
    with open("./data/서울 홍콩반점0410.csv", "r", encoding="utf-8") as fr:
        reader = csv.DictReader(fr)
        for row in reader:
            store_name = row["브랜드"] + " " + row["매장명"]
            store_url = row["URL"]
            store_info.append([store_name, store_url])
    return store_info

def load_all_reviews(playwright_page):
    def has_more_reviews():
        additional_button = playwright_page.query_selector("a[role='button'][data-pui-click-code='keywordmore']")
        if additional_button and additional_button.is_enabled():
            return True
        more_button = playwright_page.query_selector("a.fvwqf")
        if more_button and more_button.is_enabled():
            return True
        return False

    previous_reviews = set()

    while True:
        try:
            html = playwright_page.content()
            soup = BeautifulSoup(html, "lxml")
            current_reviews = {item.get_text(strip=True) for item in soup.find_all("li", class_="pui__X35jYm EjjAW")}
            new_reviews = current_reviews - previous_reviews

            if new_reviews:
                previous_reviews.update(new_reviews)
            else:
                print("더 이상의 리뷰가 없습니다.")
                break

            if has_more_reviews():
                additional_button = playwright_page.query_selector("a[role='button'][data-pui-click-code='keywordmore']")
                if additional_button:
                    additional_button.click(timeout=340000)  # 30초 대기
                else:
                    more_button = playwright_page.query_selector("a.fvwqf")
                    if more_button:
                        more_button.click(timeout=34000)  # 30초 대기
                    else:
                        print("더 이상의 리뷰가 없습니다.")
                        break

                playwright_page.wait_for_load_state("networkidle")
                time.sleep(2)  # 페이지가 안정화되는 시간을 고려하여 대기
            else:
                print("더 이상의 리뷰가 없습니다.")
                break
        except TimeoutError as e:
            print(f"시간 초과 오류 발생: {str(e)}")
            break
        except Exception as e:
            print(f"리뷰 로딩 중 오류 발생: {str(e)}")
            break

def crawl_review_page_html(playwright_page, url):
    html = ""
    try:
        playwright_page.goto(url)
        playwright_page.wait_for_load_state("networkidle")
        load_all_reviews(playwright_page)
        html = playwright_page.content()
    except TimeoutError as e:
        print(f"페이지 로딩 중 시간 초과 오류 발생: {str(e)}")
    except Exception as e:
        print(f"페이지 로딩 중 오류 발생: {str(e)}")
    return html

def parse_review_page(html, store_name):
    soup = BeautifulSoup(html, "lxml")
    review_items = soup.find_all("li", class_="pui__X35jYm EjjAW")
    data = []

    for item in review_items:
        review_text_element = item.find("div", class_="pui__vn15t2")
        if review_text_element:
            for br in review_text_element.find_all("br"):
                br.replace_with(" ")

            review_text = review_text_element.get_text(separator=" ", strip=True)
        else:
            review_text = "No review text"

        additional_info = item.find("div", class_="pui__HLNvmI")
        if additional_info:
            additional_text_elements = additional_info.find_all("span", class_="pui__jhpEyP")
            additional_texts = [element.get_text(strip=True) for element in additional_text_elements]
            additional_text = ", ".join(additional_texts)
        else:
            additional_text = "추가 정보 없음"

        review_date_div = item.find("div", class_="pui__QKE5Pr")
        if review_date_div:
            time_element = review_date_div.find("time", attrs={"aria-hidden": "true"})
            review_date = time_element.get_text(strip=True) if time_element else "No review date"
        else:
            review_date = "No review date div"

        data.append({
            "store_name": store_name,
            "review_text": review_text,
            "additional_info": additional_text,
            "review_date": review_date
        })
    return data

def write_data(data, number):
    file_name = f"./data/review_crawling_{number}.csv"
    with open(file_name, "w", encoding="utf-8", newline="") as fw:
        writer = csv.DictWriter(fw, fieldnames=["store_name", "review_text", "additional_info", "review_date"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    store_info = read_data()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        playwright_page = browser.new_page()

        for i in range(len(store_info)):
            store_name, url = store_info[i]

            print(f"{i + 1}번째 {store_name} 지점의 리뷰 수집 시작.")
            html = crawl_review_page_html(playwright_page, url)
            review_data = parse_review_page(html, store_name)
            print(f"{store_name} 지점의 리뷰 {len(review_data)}개 수집 완료.")
            write_data(review_data, i + 1)

            # 다음 배치 전 페이지와 리소스를 정리
            playwright_page.close()
            playwright_page = browser.new_page()

        browser.close()