import requests
from bs4 import BeautifulSoup

def scrape_savings_bond_rates():
    url = "https://www.treasurydirect.gov/indiv/products/prod_ibonds_glance.htm"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table containing the savings bond rates
            table = soup.find("table", class_="t-chart")

            # Extract the data from the table
            bond_rates = {}
            for row in table.find_all("tr")[1:]:
                columns = row.find_all("td")
                bond_type = columns[0].get_text().strip()
                current_rate = columns[1].get_text().strip()
                bond_rates[bond_type] = current_rate

            return bond_rates

        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            return None

    except Exception as e:
        print("An error occurred:", e)
        return None

def main():
    # Scrape savings bond rates
    bond_rates = scrape_savings_bond_rates()

    # Print the results
    if bond_rates:
        print("Savings Bond Interest Rates:")
        for bond_type, rate in bond_rates.items():
            print(f"{bond_type}: {rate}")
    else:
        print("Failed to retrieve savings bond rates.")

if __name__ == "__main__":
    main()
