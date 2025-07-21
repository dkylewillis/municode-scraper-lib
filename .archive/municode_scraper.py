from typing_extensions import Writer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

from pprint import pprint as pp
from urllib.parse import urlparse, parse_qs
from pathlib import Path


class MunicodeScraper:

    def __init__(self, headless: bool = True, timeout: int = 10):
        """
        Initialize the scraper.

        Args:
            headless: Whether to run browser in headless mode
            timeout: Default timeout for element waits in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self._setup_driver()
        self.parsed_headings = []

    def __enter__(self):
        """Context manager entry point."""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit point."""
        self.driver.quit()

    def _setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def _write_sections_to_file(self, sections, filename):
        """
        Writes ordinance sections to a text file in a readable format.
        
        Args:
            sections (list): List of dictionaries with 'title' and 'content' keys.
            filename (str): Path to the output file (e.g., 'ordinance_sections.txt').
        """

        filepath = Path("data", filename)
        print(f"📁 Writing sections to {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            for i, section in enumerate(sections, 1):
                # f.write(f"Section {i}: {section['title']}\n")
                # f.write("-" * 40 + "\n")
                f.write(section['title_txt'])
                f.write(section['content'])

    def _wait_for_element(self, url: str, by: By, value: str, timeout: int = 10, ) -> bool:
        """
        Navigates to the given URL and waits for the element to load.

        Args:
            driver: Selenium WebDriver instance.
            url: URL to navigate to.
            By: The method to locate the element (e.g., By.XPATH, By.ID).
            value: The value to locate the element (e.g., the XPath or ID).
            timeout: Time to wait in seconds (default: 10).

        Returns:
            True if the element is found, False otherwise.
        """
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception as e:
            print(f"⚠️ Element not found at {url}")
            return False

    def _parse(self, href):
        sections = []
        print(f"🔗 Parsing {href}")
        
        ## Check if the url has allready been parsed. compare headings
        ## div class chunk-heading
        try:
            if not self._wait_for_element(href, By.CLASS_NAME, "chunk-heading"):
                print(f"{href} contains no 'chunk-heading' element")
                return sections
            chunk_heading = self.driver.find_element(By.CLASS_NAME, "chunk-heading")
            chunk_heading = chunk_heading.text.splitlines()[0]

            if chunk_heading in self.parsed_headings:
                print(f"🔍 Already parsed: {chunk_heading}")
                return sections
            self.parsed_headings.append(chunk_heading)

        except Exception as e:
            print(f"❌ Error loading {href}: {e}")
            time.sleep(1)

        try:
            self.driver.get(href)
            if self._wait_for_element(href, By.ID, "codesContent"):
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                chunks = soup.find('ul', class_='chunks')

            if chunks:
                li_list = chunks.find_all('li')
                for li in li_list: 
                    title = li.find('div', class_='chunk-title')
                    if not title:
                        continue
                    #title = li.find('h2')
                    content = li.find('div', class_='chunk-content')
                    sections.append({
                        'title_txt': title.get_text(strip=True),
                        'title_html': str(title),
                        'content': str(content)
                    })
        except Exception as e:
            print(f"❌ Error loading {href}")
            time.sleep(1)  # be polite to their server

        return sections

    def _is_root_url(self, url):
        """
        Determines if the given URL is a root URL
        Check if the section contains a table of contents (TOC) element.
        """
        toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/ul"
        if not self._wait_for_element(url, By.XPATH, toc_xpath):
            return True
        else:
            return False

    def scrape_municode_full(self, url: str) -> None:
        """
        Scrapes the full Municode content from the given URL.
        Args:
            url (str): The Municode URL to scrape.
        Returns:
            None            
        """

        full_toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/nav/div[2]/div[2]/mcc-codes-toc/mcc-product-toc/div/ul"
        if not self._wait_for_element(url, By.XPATH, full_toc_xpath):
            print(f"❌ Failed to load TOC page at {url}")
            return 0

        a_tags= self.driver.find_element(By.XPATH, full_toc_xpath).find_elements(By.TAG_NAME, 'a')
        toc_url_list = [a.get_attribute('href') for a in a_tags]
        for url in toc_url_list:
            print(f"🔗 Processing URL: {url}")
            self.scrape_municode_section(url)

    def scrape_municode_section(self, url: str) -> None:
    # Headless browser options

        # Check if the URL contains a node ID
        if "?nodeId=" not in url:
            print("❌ url is not a valid. May need to use scrape_municode_full if not a section url. \n url: " + url)
            return 0

        # Step 1: Check if the URL is a root URL
        if self._is_root_url(url):
            print(f"🔗 Processing root URL: {url}")
            content = self._parse(url)
            if not content:
                return 0
            filename = content[0]['title_txt']
            self._write_sections_to_file(content, filename + ".html")
            return 1

        section_toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/ul"

        if not self._wait_for_element(url, By.XPATH, section_toc_xpath):
            print(f"❌ The url appears not to be a root URL, howerver failed to load a TOC page at {url}")
            return 0
        
        # Attempting to click a Load more button on the TOC page to ensure all links are loaded
        button_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/p/button"
        try:
            button = self.driver.find_element(By.XPATH, button_xpath)
            button.click()
            print(f"🔘 Clicked 'Load More' button on TOC page at {url}")
        except Exception as e:
            pass

        a_tags = self.driver.find_element(By.XPATH, section_toc_xpath).find_elements(By.TAG_NAME, "a")
        toc_url_list = [a.get_attribute('href') for a in a_tags]
        content = []
        filename = a_tags[0].text if a_tags else "Chapter"
        for url in toc_url_list:
            sections = self._parse(url)
            if sections:
                content.extend(sections)
                # Use the first section's title as the filename
        self._write_sections_to_file(content, filename + ".html")


if __name__ == "__main__":
    url1 = "https://library.municode.com/ga/coweta_county/codes/code_of_ordinances?nodeId=PTIICOOR_APXAZODE_ART6AHOOC"
    url2 = "https://library.municode.com/ga/coweta_county/codes/code_of_ordinances"

    with MunicodeScraper() as scraper:
        scraper.scrape_municode_section(url1)

