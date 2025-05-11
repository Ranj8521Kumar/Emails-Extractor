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


def extract_emails_from_url(url, max_pages=10):  # Reduced default max_pages for better performance
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Limit max_pages to a reasonable number for free tier
        max_pages = min(max_pages, 20)  # Cap at 20 pages to prevent timeouts

        # Initialize variables
        base_domain = get_domain(url)
        emails = set()
        visited_urls = set()
        urls_to_visit = [url]
        page_count = 0

        # First, extract emails from the main page
        try:
            response = requests.get(url, headers=headers, timeout=5)  # Reduced timeout

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract emails from the main page
                page_emails = extract_emails_from_page(soup)
                emails.update(page_emails)

                # Find links on the main page
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    # Create absolute URL
                    absolute_link = urljoin(url, link)

                    # Only add links on the same domain
                    if get_domain(absolute_link) == base_domain and absolute_link != url:
                        urls_to_visit.append(absolute_link)

                visited_urls.add(url)
                page_count = 1

        except requests.exceptions.RequestException:
            # If main page fails, return empty result
            return {
                'emails': [],
                'pages_crawled': 0,
                'base_url': url,
                'error': 'Failed to access the main page'
            }

        # Crawl additional pages (limited number)
        for i in range(min(len(urls_to_visit), max_pages - 1)):
            if page_count >= max_pages:
                break

            current_url = urls_to_visit[i]

            # Skip if already visited
            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            page_count += 1

            try:
                response = requests.get(current_url, headers=headers, timeout=5)  # Reduced timeout

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract emails from the current page
                page_emails = extract_emails_from_page(soup)
                emails.update(page_emails)

            except requests.exceptions.RequestException:
                # Skip problematic URLs
                continue

        return {
            'emails': list(emails),
            'pages_crawled': page_count,
            'base_url': url
        }

    except Exception as e:
        return {'error': str(e)}