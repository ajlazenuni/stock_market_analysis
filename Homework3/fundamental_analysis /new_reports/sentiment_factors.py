import os
import xml.etree.ElementTree as ET
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")
bert_sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def extract_company_data_from_reports(folder_path):
    company_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            for company in root.findall('.//Company'):
                name = company.find('Name').text if company.find('Name') is not None else "Unknown"
                value = company.find('Value').text if company.find('Value') is not None else "0"
                company_data[name] = float(value)

    return company_data

def extract_company_name_from_article(article):
    doc = nlp(article)
    companies = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            companies.append(ent.text)
    return companies

def analyze_sentiment_bert(description):
    result = bert_sentiment(description)
    return result[0]['label'], result[0]['score']

def perform_topic_modeling(texts, n_topics=3):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    return lda, vectorizer

def generate_recommendation(sentiment_score, company_value):
    if sentiment_score == 'POSITIVE':
        return "BUY"
    elif sentiment_score == 'NEGATIVE':
        return "SELL"
    else:
        return "HOLD"

def main():
    reports_folder = "downloaded_reports"
    company_data = extract_company_data_from_reports(reports_folder)

    news_file = "news.txt"
    with open(news_file, "r", encoding="utf-8") as file:
        news_articles = file.read().split('\n\n')

    results = []

    for article in news_articles:

        description = article.split("Опис:")[1].strip() if "Опис:" in article else article.strip()
        cleaned_description = clean_text(description)  # Clean the description

        if not cleaned_description:
            print(f"Empty text after cleaning: {description}")
            continue

        companies_mentioned = extract_company_name_from_article(article)
        sentiment_label, sentiment_score = analyze_sentiment_bert(cleaned_description)

        for company_name in companies_mentioned:
            company_value = company_data.get(company_name, 0)
            recommendation = generate_recommendation(sentiment_label, company_value)

            results.append({
                "company": company_name,
                "description": description,
                "sentiment_score": sentiment_score,
                "value": company_value,
                "recommendation": recommendation
            })

    with open("sentiment_analysis_results.txt", "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"Company: {result['company']}\n")
            file.write(f"Description: {result['description']}\n")
            file.write(f"Sentiment Score: {result['sentiment_score']}\n")
            file.write(f"Recommendation: {result['recommendation']}\n")
            file.write("\n-----------------------------\n")

    print("Sentiment analysis and recommendations completed! Results saved to sentiment_analysis_results.txt")

if __name__ == "__main__":
    main()