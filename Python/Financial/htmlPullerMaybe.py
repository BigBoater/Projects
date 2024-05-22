import grequests

def scrape_and_print_lines_with_percentage(urls):
    global html_lines
    try:
        # Stage GET requests
        requests = [grequests.get(url) for url in urls]
        # Send GET requests
        responses = grequests.map(requests)

        # Check if the request was successful (status code 200)
        for response in responses:
            if response.status_code == 200:
                # Split the HTML content into lines
                html_lines = response.text.splitlines()

                # Find lines containing "%</div>"
                lines_with_percentage = [line.strip() for line in html_lines if "%</div>" in line]

                # Print the filtered lines
                print("Lines containing '%</div>':")
                for line in lines_with_percentage:
                    print(line[-11:-6])
                    print(html_lines)
            else:
                print("Failed to retrieve HTML. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", e)

def main():
    # URL of the website you want to scrape
    urls = [
        "https://www.treasurydirect.gov/savings-bonds/ee-bonds/",
        "https://www.treasurydirect.gov/savings-bonds/i-bonds/"
    ]

    # Scrape and print lines containing "%</div>"
    scrape_and_print_lines_with_percentage(urls)

if __name__ == "__main__":
    main()
