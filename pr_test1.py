import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import seaborn as sns

proxies = [
    {'http': 'http://123.456.789.000:8080', 'https': 'http://123.456.789.000:8080'},
    {'http': 'http://987.654.321.000:8080', 'https': 'http://987.654.321.000:8080'},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

base_url = "https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/"

product_data = []

def scrape_data():
    global product_data
    page = 1

    while len(product_data) < 200:
        url = f"{base_url}?page={page}"
        proxy = random.choice(proxies)
        response = requests.get(url, headers=headers, proxies=proxy)

        if response.status_code != 200:
            print(f"Error: {response.status_code}. Retrying...")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', {'class': 'productContainer'})

        if not products:
            break

        for product in products:
            try:
                name = product.find('div', {'class': 'name'}).text.strip()
                price = float(product.find('div', {'class': 'price'}).text.replace('AED', '').strip())
                brand = product.get('data-brand', 'Unknown')
                seller = product.get('data-seller', 'Unknown')
                product_data.append({
                    'Name': name,
                    'Price': price,
                    'Brand': brand,
                    'Seller': seller
                })

                if len(product_data) >= 200:
                    break
            except Exception as e:
                print(f"Error parsing product: {e}")

        page += 1
        time.sleep(random.uniform(1, 3))

def save_to_csv():
    df = pd.DataFrame(product_data)
    df.to_csv('noon_products.csv', index=False)
    print("Data saved to noon_products.csv")

def analyze_data():
    df = pd.DataFrame(product_data)
    most_expensive = df.loc[df['Price'].idxmax()]
    print(f"Most Expensive Product: {most_expensive['Name']} - AED {most_expensive['Price']}")
    cheapest = df.loc[df['Price'].idxmin()]
    print(f"Cheapest Product: {cheapest['Name']} - AED {cheapest['Price']}")
    brand_counts = df['Brand'].value_counts()
    print("\nNumber of Products by Brand:")
    print(brand_counts)
    seller_counts = df['Seller'].value_counts()
    print("\nNumber of Products by Seller:")
    print(seller_counts)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=brand_counts.index[:10], y=brand_counts.values[:10])
    plt.title("Top 10 Brands by Product Count")
    plt.xticks(rotation=45)
    plt.ylabel("Number of Products")
    plt.show()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=seller_counts.index[:10], y=seller_counts.values[:10])
    plt.title("Top 10 Sellers by Product Count")
    plt.xticks(rotation=45)
    plt.ylabel("Number of Products")
    plt.show()

if __name__ == "__main__":
    scrape_data()
    save_to_csv()
    analyze_data()
