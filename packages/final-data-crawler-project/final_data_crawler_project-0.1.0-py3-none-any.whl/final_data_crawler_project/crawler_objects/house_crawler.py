from selenium.webdriver.common.by import By
from .estate_crawler import EstateCrawler
from ..utils.converters import convert_to_float

class HouseEstateCrawler(EstateCrawler):
    """
    Crawler for fetching House real estate data from www.aruodas.lt.
    """
    HOUSE_URL = "namai/"

    def _extract_specific_data(self, element):
        """
        Extracts specific data for House real estate.

        Parameters:
            - element: Selenium web element containing real estate data.

        Returns:
            - dict: Specific House real estate data.
        """
        object_plot_area = convert_to_float(element.find_element(By.CLASS_NAME, "list-AreaLot-v2 ").text)
        object_state = element.find_element(By.CLASS_NAME, "list-HouseStates-v2 ").text

        return {
            "plot_area": object_plot_area,
            "state": object_state,
        }
