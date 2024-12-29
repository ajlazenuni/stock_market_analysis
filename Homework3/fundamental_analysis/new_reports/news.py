import requests
from bs4 import BeautifulSoup

def get_news_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = []
    rows = soup.find_all('div', class_='row')

    for row in rows:
        title = row.find('b')
        link = row.find('a')

        if title and 'акции' in title.text.lower():
            news_url = 'https://www.mse.mk' + link['href']
            description = get_description_from_news_page(news_url)

            news_items.append({
                'date': link.text.strip(),
                'title': title.text.strip(),
                'description': description if description else 'Нема опис',
            })

    return news_items


def get_description_from_news_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    panel_body = soup.find('div', class_='panel-body')
    if panel_body:
        description_paragraphs = panel_body.find_all('p')
        description = "\n".join([para.text.strip() for para in description_paragraphs])
        return description
    return None


def get_all_news():
    base_url = 'https://www.mse.mk/mk/news/latest/'

    all_news = []
    for page_num in range(1, 11):
        url = base_url + str(page_num)
        news_from_page = get_news_from_page(url)
        all_news.extend(news_from_page)

    return all_news


def save_news_to_file(news):
    with open('news.txt', 'w', encoding='utf-8') as file:
        for item in news:
            file.write(f"Дата: {item['date']}\n")
            file.write(f"Наслов: {item['title']}\n")
            file.write(f"Опис: {item['description']}\n")
            file.write('-' * 80 + '\n')


def main():
    news = get_all_news()
    if not news:
        print("Нема вести кои содржат зборот 'акции'.")
    else:
        save_news_to_file(news)
        print("Вестите се зачувани во news.txt")


if __name__ == "__main__":
    main()