"""
Playwright helper for JavaScript-rendered pages.
"""
from typing import Optional
from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup


class PlaywrightHelper:
    """Helper class for using Playwright to fetch JavaScript-rendered pages."""
    
    _browser: Optional[Browser] = None
    _playwright = None
    
    @classmethod
    def get_browser(cls) -> Browser:
        """Get or create a browser instance (singleton)."""
        if cls._browser is None:
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(headless=True)
        return cls._browser
    
    @classmethod
    def close_browser(cls):
        """Close the browser instance."""
        if cls._browser:
            cls._browser.close()
            cls._browser = None
        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None
    
    @classmethod
    def fetch_page(cls, url: str, wait_timeout: int = 30000, wait_selector: Optional[str] = None) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a JavaScript-rendered page using Playwright.
        
        Args:
            url: URL to fetch
            wait_timeout: Maximum time to wait for page load (ms)
            wait_selector: Optional CSS selector to wait for before parsing
            
        Returns:
            BeautifulSoup object or None if fetch fails
        """
        page = None
        try:
            browser = cls.get_browser()
            page = browser.new_page()
            
            # Set longer timeout for slow pages
            page.set_default_timeout(wait_timeout)
            
            # Navigate to page with more lenient wait condition
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=wait_timeout)
            except PlaywrightTimeoutError:
                # Try with load instead
                try:
                    page.goto(url, wait_until="load", timeout=wait_timeout)
                except PlaywrightTimeoutError:
                    print(f"Warning: Page load timeout for {url}, continuing anyway")
            
            # Wait a bit for JavaScript to execute
            page.wait_for_timeout(2000)
            
            # Wait for specific selector if provided
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=10000)
                except PlaywrightTimeoutError:
                    print(f"Warning: Selector '{wait_selector}' not found, continuing anyway")
            
            # Get page content
            content = page.content()
            
            # Handle encoding issues
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8', errors='replace')
                except:
                    content = content.decode('latin-1', errors='replace')
            
            return BeautifulSoup(content, 'lxml')
            
        except Exception as e:
            print(f"Error fetching {url} with Playwright: {e}")
            return None
        finally:
            if page:
                try:
                    page.close()
                except:
                    pass

