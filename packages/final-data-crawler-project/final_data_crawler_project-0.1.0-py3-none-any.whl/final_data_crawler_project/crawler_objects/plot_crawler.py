from selenium.webdriver.common.by import By
from .estate_crawler import EstateCrawler

class PlotEstateCrawler(EstateCrawler):
    """
    Crawler for fetching Plot real estate data from www.aruodas.lt.
    """
    PLOT_URL = "sklypai/"

    def _extract_specific_data(self, element):
        """
        Extracts specific data for Plot real estate.

        Parameters:
            - element: Selenium web element containing real estate data.

        Returns:
            - dict: Specific Plot real estate data.
        """
        object_purpose = element.find_element(By.CLASS_NAME, "list-Intendances-v2 ").text

        return {
            "purpose": object_purpose,
        }
