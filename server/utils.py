"""
Email Extraction Utilities

This module contains utility functions for extracting email addresses from websites.
It provides functionality to crawl websites and extract emails from the content.

Author: Your Name
Date: May 2025
"""

import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
import re  # For regular expressions to find email patterns
from urllib.parse import urljoin, urlparse  # For URL handling


def extract_emails_from_page(soup):
    """
    Extract email addresses from a BeautifulSoup object.

    This function extracts emails from both the visible text on the page
    and from mailto links in anchor tags.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing a parsed HTML page.

    Returns:
        set: A set of unique email addresses found on the page.
    """
    emails = set()  # Use a set to avoid duplicate emails

    # Extract emails from visible text using regex
    text = soup.get_text()
    # This regex pattern matches standard email formats
    emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

    # Extract emails from mailto links in anchor tags
    for a_tag in soup.find_all('a', href=True):
        if "mailto:" in a_tag['href']:
            # Extract the email address from the mailto link
            # Split at '?' to remove any parameters
            email = a_tag['href'].split("mailto:")[1].split("?")[0]
            emails.add(email)

    return emails


def get_domain(url):
    """
    Extract the domain name from a URL.

    This function parses a URL and returns just the domain part.
    For example, from 'https://www.example.com/page', it returns 'www.example.com'.

    Args:
        url (str): The URL to parse.

    Returns:
        str: The domain name extracted from the URL.
    """
    parsed_url = urlparse(url)  # Parse the URL into components
    return parsed_url.netloc  # Return just the domain part


def extract_emails_from_url(url, max_pages=10):
    """
    Extract email addresses from a website by crawling its pages.

    This function crawls a website starting from the given URL, extracts
    email addresses from each page, and follows links to other pages on
    the same domain up to the specified maximum number of pages.

    Args:
        url (str): The starting URL to crawl.
        max_pages (int, optional): Maximum number of pages to crawl. Defaults to 10.
            This is capped at 20 pages to prevent timeouts on free hosting tiers.

    Returns:
        dict: A dictionary containing:
            - 'emails': List of unique email addresses found
            - 'pages_crawled': Number of pages successfully crawled
            - 'base_url': The original URL that was crawled
            - 'error': Error message if an error occurred (only present if there was an error)
    """
    try:
        # Set headers to mimic a browser request to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Limit max_pages to a reasonable number for free tier hosting
        max_pages = min(max_pages, 20)  # Cap at 20 pages to prevent timeouts

        # Initialize variables for tracking the crawl
        base_domain = get_domain(url)  # Extract the domain from the URL
        emails = set()  # Store unique emails
        visited_urls = set()  # Track visited URLs to avoid loops
        urls_to_visit = [url]  # Queue of URLs to visit
        page_count = 0  # Counter for pages visited

        # Step 1: First, extract emails from the main page
        try:
            # Request the main page with a short timeout
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract emails from the main page
                page_emails = extract_emails_from_page(soup)
                emails.update(page_emails)

                # Find links on the main page to crawl next
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    # Convert relative URLs to absolute URLs
                    absolute_link = urljoin(url, link)

                    # Only add links on the same domain and not the same as the current URL
                    if get_domain(absolute_link) == base_domain and absolute_link != url:
                        urls_to_visit.append(absolute_link)

                # Mark the main page as visited
                visited_urls.add(url)
                page_count = 1

        except requests.exceptions.RequestException:
            # If the main page fails, return an error
            return {
                'emails': [],
                'pages_crawled': 0,
                'base_url': url,
                'error': 'Failed to access the main page'
            }

        # Step 2: Crawl additional pages (limited number)
        for i in range(min(len(urls_to_visit), max_pages - 1)):
            # Stop if we've reached the maximum number of pages
            if page_count >= max_pages:
                break

            current_url = urls_to_visit[i]

            # Skip if we've already visited this URL
            if current_url in visited_urls:
                continue

            # Mark as visited and increment page counter
            visited_urls.add(current_url)
            page_count += 1

            try:
                # Request the page with a short timeout
                response = requests.get(current_url, headers=headers, timeout=5)

                # Skip pages that don't return a successful status code
                if response.status_code != 200:
                    continue

                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract emails from the current page
                page_emails = extract_emails_from_page(soup)
                emails.update(page_emails)

            except requests.exceptions.RequestException:
                # Skip problematic URLs and continue with the next one
                continue

        # Step 3: Return the results
        return {
            'emails': list(emails),  # Convert set to list for JSON serialization
            'pages_crawled': page_count,
            'base_url': url
        }

    except Exception as e:
        # Catch any unexpected errors and return them
        return {'error': str(e)}