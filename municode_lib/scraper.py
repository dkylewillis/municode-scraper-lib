"""Web scraper for municode content."""

from typing import List, Optional
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from .models import Section, Document
from .exceptions import ScrapingError, InvalidUrlError, ElementNotFoundError


class MunicodeScraper:
    """Web scraper for municode content."""
    
    def __init__(self, headless: bool = True, timeout: int = 10, output_dir: str = "data"):
        """
        Initialize the scraper.

        Args:
            headless: Whether to run browser in headless mode
            timeout: Default timeout for element waits in seconds
            output_dir: Directory for output files
        """
        self.headless = headless
        self.timeout = timeout
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.driver = None
        self.parsed_headings = []
        
    def __enter__(self):
        """Context manager entry point."""
        self._setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit point."""
        if self.driver:
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

    def _wait_for_element(self, url: str, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """
        Navigates to the given URL and waits for the element to load.

        Args:
            url: URL to navigate to.
            by: The method to locate the element (e.g., By.XPATH, By.ID).
            value: The value to locate the element (e.g., the XPath or ID).
            timeout: Time to wait in seconds (default: self.timeout).

        Returns:
            True if the element is found, False otherwise.
        """
        if timeout is None:
            timeout = self.timeout
            
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def _parse_sections(self, url: str) -> List[Section]:
        """Parse sections from a municode page."""
        sections = []
        print(f"🔗 Parsing {url}")
        
        # Check if the url has already been parsed
        try:
            if not self._wait_for_element(url, By.CLASS_NAME, "chunk-heading"):
                print(f"{url} contains no 'chunk-heading' element")
                return sections
                
            chunk_heading = self.driver.find_element(By.CLASS_NAME, "chunk-heading")
            chunk_heading_text = chunk_heading.text.splitlines()[0]

            if chunk_heading_text in self.parsed_headings:
                print(f"🔍 Already parsed: {chunk_heading_text}")
                return sections
            self.parsed_headings.append(chunk_heading_text)

        except Exception as e:
            print(f"❌ Error loading {url}: {e}")
            time.sleep(1)
            return sections

        try:
            if self._wait_for_element(url, By.ID, "codesContent"):
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                chunks = soup.find('ul', class_='chunks')

                if chunks:
                    li_list = chunks.find_all('li')
                    for li in li_list: 
                        title_elem = li.find('div', class_='chunk-title')
                        if not title_elem:
                            continue
                        content_elem = li.find('div', class_='chunk-content')
                        
                        section = Section(
                            title=title_elem.get_text(strip=True),
                            title_html=str(title_elem),
                            content=str(content_elem) if content_elem else "",
                            url=url
                        )
                        sections.append(section)
                        
        except Exception as e:
            print(f"❌ Error parsing {url}: {e}")
            time.sleep(1)

        return sections

    def _is_root_url(self, url: str) -> bool:
        """
        Determines if the given URL is a root URL by checking for TOC element.
        """
        toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/ul"
        return not self._wait_for_element(url, By.XPATH, toc_xpath)

    def _click_load_more_button(self, url: str) -> bool:
        """Attempt to click 'Load More' button if present."""
        button_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/p/button"
        try:
            button = self.driver.find_element(By.XPATH, button_xpath)
            button.click()
            print(f"🔘 Clicked 'Load More' button on TOC page at {url}")
            return True
        except Exception:
            return False

    def scrape_section(self, url: str) -> Optional[Document]:
        """
        Scrape a single section and return Document object.
        
        Args:
            url: The Municode URL to scrape.
            
        Returns:
            Document object containing scraped content, or None if failed.
        """
        if not self.driver:
            self._setup_driver()
            
        # Validate URL
        if "?nodeId=" not in url:
            raise InvalidUrlError(f"URL is not a valid section URL: {url}")

        # Check if the URL is a root URL
        if self._is_root_url(url):
            print(f"🔗 Processing root URL: {url}")
            sections = self._parse_sections(url)
            if not sections:
                return None
            
            title = sections[0].title if sections else "Unknown"
            return Document(title=title, sections=sections, source_url=url)

        # Handle section with TOC
        section_toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/main/div[1]/mcc-codes-content/div/div[2]/div[2]/ul"

        if not self._wait_for_element(url, By.XPATH, section_toc_xpath):
            raise ElementNotFoundError(f"Failed to load TOC page at {url}")
        
        # Try to click load more button
        self._click_load_more_button(url)

        # Get all section URLs from TOC
        a_tags = self.driver.find_element(By.XPATH, section_toc_xpath).find_elements(By.TAG_NAME, "a")
        toc_url_list = [a.get_attribute('href') for a in a_tags]
        
        all_sections = []
        title = a_tags[0].text if a_tags else "Chapter"
        
        for section_url in toc_url_list:
            sections = self._parse_sections(section_url)
            if sections:
                all_sections.extend(sections)
                
        return Document(title=title, sections=all_sections, source_url=url)

    def scrape_full(self, url: str) -> List[Document]:
        """
        Scrape entire municode and return list of Documents.
        
        Args:
            url: The base Municode URL to scrape.
            
        Returns:
            List of Document objects.
        """
        if not self.driver:
            self._setup_driver()
            
        full_toc_xpath = "/html/body/div[3]/div[2]/ui-view/mcc-codes/div[7]/nav/div[2]/div[2]/mcc-codes-toc/mcc-product-toc/div/ul"
        
        if not self._wait_for_element(url, By.XPATH, full_toc_xpath):
            raise ElementNotFoundError(f"Failed to load full TOC page at {url}")

        a_tags = self.driver.find_element(By.XPATH, full_toc_xpath).find_elements(By.TAG_NAME, 'a')
        toc_url_list = [a.get_attribute('href') for a in a_tags]
        
        documents = []
        for section_url in toc_url_list:
            print(f"🔗 Processing URL: {section_url}")
            try:
                doc = self.scrape_section(section_url)
                if doc:
                    documents.append(doc)
            except Exception as e:
                print(f"❌ Failed to scrape {section_url}: {e}")
                continue
                
        return documents
