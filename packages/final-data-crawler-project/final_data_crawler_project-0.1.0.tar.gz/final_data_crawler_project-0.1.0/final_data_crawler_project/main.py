from io import StringIO
from typing import Callable, Literal
from pandas import DataFrame

from .crawler_objects import ApartmentEstateCrawler, PlotEstateCrawler, HouseEstateCrawler

CRAWLERS: dict[str, Callable[...,DataFrame]] = {
    "PLOT": PlotEstateCrawler,
    "APARTMENTS": ApartmentEstateCrawler,
    "HOUSE": HouseEstateCrawler
}
def crawl_real_estate(object: Literal["PLOT", "APARTMENTS", "HOUSE"],
                      time_limit: int | None = None,
                      query: str ="",
                      return_format: Literal["csv", "df", "records"] = "df"):
    """
    Crawls real estate data from www.aruodas.lt based on the specified real estate object type.

    Parameters:
        - object (Literal["PLOT", "APARTMENTS", "HOUSE"]): The type of real estate to crawl.
        - time_limit (int | None, optional): Time limit for the crawler to get data. Defaults to None.
        - query (str, optional): The region or search text for the real estate. Defaults to an empty string.
        - return_format (Literal["csv", "df", "records"], optional): The desired format of the output data.
            - "csv": Returns a CSV formatted string.
            - "df": Returns a pandas DataFrame.
            - "records": Returns a list of records (dicts).

    Returns:
        - str, pandas.DataFrame, or list: The crawled real estate data in the specified format.

    Raises:
        - ValueError: If the specified real estate object type is not available in the crawler.
    """
    if object not in CRAWLERS:
        raise ValueError(f"Object '{object}' is not available in the crawler")
    scraper = CRAWLERS[object](object, query, time_limit)
    data = scraper.get_search_results()
    scraper.close_driver()
    if return_format == "csv":
        with StringIO as output:
            data.to_csv(output)
            content = output.getvalue()
        return content
    elif return_format == "records":
        return data.to_dict(orient="records")
    else:
        return data
    