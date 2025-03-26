class ScraperHttpError(Exception):
    def __init__(self, original_error=None, division_id=None, url=None):
        self.original_error = original_error
        self.division_id = division_id
        self.url = url
        
        # Auto-generate message from available information
        message = f"Scraper HTTP error"
        if division_id is not None:
            message += f" for division {division_id}"
        if url is not None:
            message += f" at URL: {url}"
        if original_error is not None:
            message += f" - {str(original_error)}"
            
        super().__init__(message)