import pytest
from unittest.mock import patch, MagicMock
import requests
from sqlalchemy import select
from falcons_stats.models.base import db
from falcons_stats.scrapers.base_scraper import BaseScraper
from falcons_stats.scrapers.exceptions import ScraperHttpError
from falcons_stats.models import Division

# Create a concrete implementation for testing
class ConcreteScraper(BaseScraper):
    def url(self) -> str:
        return "https://example.com/data"
    
    def parse_html_response(self, raw_data):
        return [{"data": "parsed"}]
    
    def persist_parsed_data(self, parsed_data):
        pass

class TestBaseScraper:
    
    def test_url_is_abstract(self):
        """Test that url is an abstract method"""
        with pytest.raises(TypeError):
            BaseScraper()
    
    def test_init(self):
        """Test that the constructor sets up the expected attributes"""
        scraper = ConcreteScraper()
        
        # Check session and cookies
        assert scraper.session is not None
        assert isinstance(scraper.cookies, dict)
        assert scraper.cookies["e2elc_top10only"] == "false"
        assert scraper.cookies["e2elc_gamesdivisionid"] is None
    
    def test_divisions(self, sample_divisions, app_context):
        pass