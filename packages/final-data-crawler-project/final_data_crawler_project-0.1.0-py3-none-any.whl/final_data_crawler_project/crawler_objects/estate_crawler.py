from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
from pandas import DataFrame
from dataclasses import dataclass
from ..utils.error_handler import text_value_error_handler
from ..utils.converters import convert_to_float

@dataclass
class EstateObject:
    """
    Represents a base class for real estate objects.

    Attributes:
        - address (str): The address of the real estate.
        - url (str): The URL of the real estate listing.
        - price (float): The price of the real estate.
        - area (float): The area of the real estate.
        - real_estate_type (str): The type of the real estate (e.g., Apartment, House, Plot).
    """
    address: str
    url: str
    price: float
    area: float
    real_estate_type: str

@dataclass
class ApartmentObject(EstateObject):
    """
    Represents an Apartment real estate object.

    Attributes:
        - no_of_rooms (int): Number of rooms in the apartment.
        - floor_no (str): The floor number where the apartment is located.
        - created (str): The timestamp when the object was created.
    """
    no_of_rooms: int
    floor_no: str
    created: str = str(datetime.now())

@dataclass
class HouseObject(EstateObject):
    """
    Represents a House real estate object.

    Attributes:
        - plot_area (float): The area of the plot associated with the house.
        - state (str): The current state of the house (e.g., finished, partly finished).
        - created (str): The timestamp when the object was created.
    """
    plot_area: float
    state: str
    created: str = str(datetime.now())

@dataclass
class PlotObject(EstateObject):
    """
    Represents a Plot real estate object.

    Attributes:
        - purpose (str): The purpose of the plot (e.g., residential, commercial).
        - created (str): The timestamp when the object was created.
    """
    purpose: str
    created: str = str(datetime.now())

class EstateCrawler:
    """
    Base class for crawling real estate data from www.aruodas.lt.

    Attributes:
        - BASE_URL (str): The base URL of the website.
        - SEARCH_URL (str): The search URL parameter.
    """
    BASE_URL = "https://www.aruodas.lt/"
    SEARCH_URL = "?search_text="

    def __init__(self, estate_type: str, search_text: Optional[str] = "", time_limit: Optional[int] = None):
        """
        Initializes the EstateCrawler object.

        Parameters:
            - estate_type (str): The type of real estate to search for (e.g., 'APARTMENTS', 'HOUSE', 'PLOT').
            - search_text (str, optional): The region to search for (e.g., 'Vilnius'). Defaults to an empty string.
            - time_limit (int, optional): Time limit for the crawler to get data. Defaults to None.
        """
        checked_text = text_value_error_handler(search_text)
        self.search_text = checked_text
        self.mod_search_text = self.search_text.replace(" ", "%20")
        self.time_limit = int(time_limit) if time_limit is not None else None
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.estate_type = estate_type

    def _handle_cookies(self):
        """
        Handles cookies pop-up if present.
        """
        try:
            cookie_element = self.driver.find_element(by="id", value="onetrust-reject-all-handler")
            cookie_element.click()
        except NoSuchElementException:
            pass

    def _check_time_limit(self, start_time: float):
        """
        Checks if the time limit for crawling has been exceeded.

        Parameters:
            - start_time (float): The start time of the crawling process.

        Returns:
            - bool: True if the time limit has been exceeded, False otherwise.
        """
        return self.time_limit is not None and time.time() - start_time > self.time_limit

    def _extract_estate_data(self, element):
        """
        Extracts common data for all types of real estate.

        Parameters:
            - element: Selenium web element containing real estate data.

        Returns:
            - dict: Common real estate data.
        """
        address_loc = element.find_element(By.CLASS_NAME, "list-adress-v2 ")
        object_link = address_loc.find_element(By.CSS_SELECTOR, "h3 a")
        object_address = object_link.text.replace("\n", " ")
        object_url = object_link.get_attribute("href")
        object_price = convert_to_float(address_loc.find_element(By.CSS_SELECTOR, "div span.list-item-price-v2").text.replace("€", "").replace(" ", ""))
        object_area = convert_to_float(element.find_element(By.CLASS_NAME, "list-AreaOverall-v2 ").text)

        specific_data = self._extract_specific_data(element)

        # Choose the appropriate data class based on the estate_type
        if self.estate_type == 'APARTMENTS':
            return ApartmentObject(
                address=object_address,
                url=object_url,
                price=object_price,
                area=object_area,
                real_estate_type=self.estate_type.lower(),
                **specific_data
            )
        elif self.estate_type == 'HOUSE':
            return HouseObject(
                address=object_address,
                url=object_url,
                price=object_price,
                area=object_area,
                real_estate_type=self.estate_type.lower(),
                **specific_data
            )
        elif self.estate_type == 'PLOT':
            return PlotObject(
                address=object_address,
                url=object_url,
                price=object_price,
                area=object_area,
                real_estate_type=self.estate_type.lower(),
                **specific_data
            )
        else:
            raise ValueError(f"Unsupported estate type: {self.estate_type}")

    def _extract_specific_data(self, element):
        """
        Extracts specific data for each type of real estate.

        To be implemented by subclasses.

        Parameters:
            - element: Selenium web element containing real estate data.

        Returns:
            - dict: Specific real estate data.
        """
        # To be implemented by subclasses
        raise NotImplementedError("Subclasses must implement this method.")

    def _get_next_page_button(self):
        """
        Gets the next page button element.

        Returns:
            - WebElement: The next page button element or None if not found.
        """
        try:
            return self.driver.find_element(By.XPATH, "//div[contains(@class, 'pagination')]/a[text()='»']")
        except NoSuchElementException:
            return None

    def get_search_results(self):
        """
        Scrapes real estate data from the specified search region.

        Returns:
            - pandas.DataFrame: A DataFrame containing all collected real estates. Each row in the DataFrame represents real estate,
                                with columns corresponding to the details of the real estate as provided by www.aruodas.lt.

        Notes:
            - If the request for the first page fails, an empty DataFrame is returned.
            - If the specified time limit is reached before all pages are fetched, the process is terminated, and data
            collected up to that point is returned.
        """
        url = self.BASE_URL + getattr(self, f"{self.estate_type}_URL") + self.SEARCH_URL + self.mod_search_text
        self.driver.get(url)
        self._handle_cookies()

        objects = []
        start_time = time.time()

        while True:
            if self._check_time_limit(start_time):
                print("Time limit exceeded!")
                break
            advert_wrapper = self.driver.find_elements(By.CSS_SELECTOR, ".list-row-v2.object-row")

            if not advert_wrapper:
                return DataFrame()

            for element in advert_wrapper:
                obj_data = self._extract_estate_data(element)
                objects.append(obj_data.__dict__)

            next_page_button = self._get_next_page_button()

            if not next_page_button or "disabled" in next_page_button.get_attribute("class"):
                break
            else:
                next_page_button.click()
                time.sleep(2)

        return DataFrame(objects)

    def close_driver(self):
        """
        Closes the WebDriver.
        """
        self.driver.close()