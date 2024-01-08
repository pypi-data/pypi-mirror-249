from selenium.webdriver.common.by import By
from .estate_crawler import EstateCrawler
from ..utils.converters import convert_to_int

class ApartmentEstateCrawler(EstateCrawler):
    """
    Crawler for fetching Apartment real estate data from www.aruodas.lt.
    """
    APARTMENTS_URL = "butai/"

    def _extract_specific_data(self, element):
        """
        Extracts specific data for Apartment real estate.

        Parameters:
            - element: Selenium web element containing real estate data.

        Returns:
            - dict: Specific Apartment real estate data.
        """
        object_no_of_rooms = convert_to_int(element.find_element(By.CLASS_NAME, "list-RoomNum-v2 ").text)
        object_floor_no = element.find_element(By.CLASS_NAME, "list-Floors-v2 ").text

        return {
            "no_of_rooms": object_no_of_rooms,
            "floor_no": object_floor_no,
        }
