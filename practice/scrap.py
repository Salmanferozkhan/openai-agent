import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
from PyPDF2 import PdfMerger
import re
from typing import Set, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentationDownloader:
    def __init__(self, base_url: str, output_dir: str = "downloaded_docs"):
        """
        Initialize the documentation downloader.
        
        Args:
            base_url: The base URL of the documentation site
            output_dir: Directory to save the PDFs
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls: Set[str] = set()
        self.pdf_files: List[str] = []
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def is_valid_doc_url(self, url: str) -> bool:
        """Check if the URL belongs to the documentation domain."""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        
        # Check if it's the same domain and within the docs path
        return (parsed_url.netloc == parsed_base.netloc and 
                parsed_url.path.startswith(parsed_base.path))
    
    def get_all_doc_links(self, url: str) -> Set[str]:
        """Recursively find all documentation links starting from the given URL."""
        if url in self.visited_urls:
            return set()
            
        self.visited_urls.add(url)
        links = set()
        
        try:
            logger.info(f"Crawling: {url}")
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                
                # Filter out non-documentation links
                if (self.is_valid_doc_url(absolute_url) and 
                    not absolute_url.endswith(('.pdf', '.zip', '.tar.gz')) and
                    '#' not in absolute_url):  # Avoid fragment URLs
                    links.add(absolute_url)
            
            # Recursively crawl found links
            for link in list(links):
                if link not in self.visited_urls:
                    time.sleep(0.5)  # Be polite to the server
                    links.update(self.get_all_doc_links(link))
                    
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            
        return links
    
    def url_to_filename(self, url: str) -> str:
        """Convert URL to a valid filename."""
        # Remove protocol and domain
        parsed = urlparse(url)
        path = parsed.path
        
        # Clean up the path
        if path.endswith('/'):
            path = path[:-1]
        if not path or path == '/':
            path = 'index'
            
        # Replace slashes with underscores and remove special characters
        filename = re.sub(r'[^\w\-_]', '_', path.strip('/'))
        return f"{filename}.pdf"
    
    def convert_url_to_pdf(self, url: str) -> str:
        """Convert a single URL to PDF."""
        filename = self.url_to_filename(url)
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            logger.info(f"Converting {url} to PDF...")
            
            # Configure pdfkit options for better rendering
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
                'no-background': False,
                'javascript-delay': 2000,  # Wait for JS to load
            }
            
            # Convert URL to PDF
            pdfkit.from_url(url, filepath, options=options)
            logger.info(f"Saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error converting {url} to PDF: {e}")
            return None
    
    def merge_pdfs(self, output_filename: str = "complete_documentation.pdf"):
        """Merge all individual PDFs into a single file."""
        if not self.pdf_files:
            logger.warning("No PDFs to merge")
            return
            
        merger = PdfMerger()
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            for pdf_file in sorted(self.pdf_files):
                if os.path.exists(pdf_file):
                    logger.info(f"Adding {pdf_file} to merged PDF")
                    merger.append(pdf_file)
            
            merger.write(output_path)
            merger.close()
            logger.info(f"Merged PDF saved as: {output_path}")
            
            # Optionally, delete individual PDFs after merging
            # for pdf_file in self.pdf_files:
            #     os.remove(pdf_file)
            
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
    
    def download_documentation(self, merge: bool = True):
        """Main method to download entire documentation."""
        logger.info(f"Starting documentation download from: {self.base_url}")
        
        # Step 1: Crawl and find all documentation URLs
        all_urls = self.get_all_doc_links(self.base_url)
        all_urls.add(self.base_url)  # Include the base URL
        
        logger.info(f"Found {len(all_urls)} documentation pages")
        
        # Step 2: Convert each URL to PDF
        for i, url in enumerate(sorted(all_urls), 1):
            logger.info(f"Processing {i}/{len(all_urls)}: {url}")
            pdf_path = self.convert_url_to_pdf(url)
            if pdf_path:
                self.pdf_files.append(pdf_path)
            time.sleep(1)  # Rate limiting
        
        # Step 3: Merge PDFs if requested
        if merge and len(self.pdf_files) > 1:
            self.merge_pdfs()
        
        logger.info("Documentation download completed!")


def download_shopify_graphql_docs():
    """Specific function to download Shopify GraphQL documentation."""
    url = "https://shopify.dev/docs/api/admin-graphql/latest"
    downloader = DocumentationDownloader(url, output_dir="shopify_graphql_docs")
    downloader.download_documentation(merge=True)


# Alternative implementation using Playwright (better for JavaScript-heavy sites)
class PlaywrightDocumentationDownloader:
    """Alternative implementation using Playwright for better JavaScript support."""

    def __init__(self, base_url: str, output_dir: str = "downloaded_docs"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls: Set[str] = set()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_valid_doc_url(self, url: str) -> bool:
        """Check if the URL belongs to the documentation domain."""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)

        # Check if it's the same domain and within the docs path
        return (parsed_url.netloc == parsed_base.netloc and
                parsed_url.path.startswith(parsed_base.path))

    def url_to_filename(self, url: str) -> str:
        """Convert URL to a valid filename."""
        # Remove protocol and domain
        parsed = urlparse(url)
        path = parsed.path

        # Clean up the path
        if path.endswith('/'):
            path = path[:-1]
        if not path or path == '/':
            path = 'index'

        # Replace slashes with underscores and remove special characters
        filename = re.sub(r'[^\w\-_]', '_', path.strip('/'))
        return f"{filename}.pdf"
    
    async def download_with_playwright(self):
        """Download documentation using Playwright (requires playwright package)."""
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Navigate to the base URL
            await page.goto(self.base_url, wait_until='networkidle')
            
            # Get all links
            links = await page.evaluate('''
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links.map(link => link.href);
                }
            ''')
            
            # Filter and process links
            doc_links = [link for link in links if self.is_valid_doc_url(link)]
            
            for link in doc_links:
                if link not in self.visited_urls:
                    self.visited_urls.add(link)
                    await page.goto(link, wait_until='networkidle')
                    
                    # Generate PDF
                    filename = self.url_to_filename(link)
                    filepath = os.path.join(self.output_dir, filename)
                    await page.pdf(path=filepath, format='A4')
                    logger.info(f"Saved: {filepath}")
            
            await browser.close()


# Usage example
if __name__ == "__main__":
    # Method 2: Using Playwright (better for JavaScript-heavy sites)
    # Install: pip install playwright && playwright install chromium
    import asyncio
    downloader = PlaywrightDocumentationDownloader("https://shopify.dev/docs/api/admin-graphql/latest", "shopify_graphql_docs")
    asyncio.run(downloader.download_with_playwright())