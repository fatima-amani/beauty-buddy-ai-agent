import requests
from bs4 import BeautifulSoup
import json
import html


def get_recommendation(query):
    query = "%20".join(query.split())  # Format the query for the URL
    url = f"https://www.tirabeauty.com/products/?q={query}"
    print("Fetching URL:", url)

    try:
        response = requests.get(url)
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Adjusting to find the correct product section
            products_container = soup.find('div', class_='product-container')  # Update class name as per actual site
            if not products_container:
                print("Product container not found.")
                return json.dumps([])

            products = products_container.find_all(recursive=False)

            if not products:
                print("No products found.")
                return json.dumps([])

            items = []
            count = 0

            for product in products:  # Loop through all products
                if count == 5:
                    break

                count += 1
                try:
                    # Check if <a> tag exists
                    a_tag = product.find('a')
                    if not a_tag or 'href' not in a_tag.attrs:
                        print("Skipping product: No <a> tag or href attribute found.")
                        continue

                    prod_link = a_tag['href']
                    prod_name = product.find('div', class_='product-name')
                    if not prod_name:
                        print("Skipping product: No product name found.")
                        continue

                    # Decode Unicode escape sequences in the product name
                    prod_name = prod_name.get_text(strip=True)
                    prod_name = prod_name.encode('utf-8').decode('unicode_escape')  # Fix Unicode escape sequences
                    prod_name = html.unescape(prod_name)  # Fix HTML entities

                    # Find the price
                    discounted_price = product.find('p', class_='discounted-price')
                    actual_price = product.find('p', class_='actual-price')

                    # Use discounted price if available, otherwise use actual price
                    if discounted_price:
                        price = discounted_price.get_text(strip=True)
                    elif actual_price:
                        price = actual_price.get_text(strip=True)
                    else:
                        price = "Price not available"

                    # # Decode Unicode escape sequences in the price
                    # price = price.encode('utf-8').decode('unicode_escape')  # Fix Unicode escape sequences
                    # price = html.unescape(price)  # Fix HTML entities

                    items.append({
                        "name": prod_name,
                        "link": f"https://www.tirabeauty.com{prod_link}" if prod_link.startswith("/") else prod_link,
                        "price": price  # Add the price field
                    })
                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue  # Skip if any error occurs

            return json.dumps(items, indent=4, ensure_ascii=False)  # Ensure non-ASCII characters are preserved
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return json.dumps([])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return json.dumps([])


# Example usage
result = get_recommendation("foundation")
print(result)