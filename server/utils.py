import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse


def extract_emails_from_page(soup):
    """Extract emails from a BeautifulSoup object."""
    emails = set()

    # Extract from visible text
    text = soup.get_text()
    emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

    # Extract from mailto links
    for a_tag in soup.find_all('a', href=True):
        if "mailto:" in a_tag['href']:
            email = a_tag['href'].split("mailto:")[1].split("?")[0]
            emails.add(email)

    return emails


def get_domain(url):
    """Extract the domain from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc


def extract_emails_from_url(url, max_pages=50):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Initialize variables
        base_domain = get_domain(url)
        emails = set()
        visited_urls = set()
        urls_to_visit = [url]
        page_count = 0

        # Crawl the website
        while urls_to_visit and page_count < max_pages:
            current_url = urls_to_visit.pop(0)

            # Skip if already visited
            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            page_count += 1

            try:
                response = requests.get(current_url, headers=headers, timeout=10)

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract emails from the current page
                page_emails = extract_emails_from_page(soup)
                emails.update(page_emails)

                # Find links to other pages on the same domain
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    # Create absolute URL
                    absolute_link = urljoin(current_url, link)

                    # Only follow links on the same domain
                    if get_domain(absolute_link) == base_domain and absolute_link not in visited_urls:
                        urls_to_visit.append(absolute_link)

            except requests.exceptions.RequestException:
                # Skip problematic URLs
                continue

        return {
            'emails': list(emails),
            'pages_crawled': page_count,
            'base_url': url
        }

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}