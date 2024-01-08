from m1_project_agne import krepsinis
from io import StringIO
from typing import Any, Callable, Literal
import pandas as pd



CRAWLERS: dict[str, Callable[..., pd.DataFrame]] = {
    "krepsinis": krepsinis.crawl_krepsinis,
}

def crawl(
    source: Literal["krepsinis"],
    return_format: Literal["csv", "df", "records"] = "csv",
    **kwargs,
) -> pd.DataFrame or str or list[dict[str, Any]]:
    """
        Crawls data from a specified source and returns it in the desired format.

        Args:
            source (Literal["krepsinis"]): The source from which to crawl data.
            return_format (Literal["csv", "df", "records"], optional): The desired format for the returned data.
                Options are "csv" for CSV string, "df" for pandas DataFrame, and "records" for a list of dictionaries.
                Default is "csv".
            **kwargs: Additional keyword arguments specific to the chosen source.

        Returns:
            pd.DataFrame or str or list[dict[str, Any]]: The crawled data in the specified format.

        Example:
            crawl("krepsinis", return_format="csv", time_limit=10)
        Example with query:
            crawl("krepsinis", return_format="csv", time_limit=10, search_word = "rytas")
        Raises:
            ValueError: If the specified source is not supported.
        """

    if source not in CRAWLERS:
        raise ValueError(f"Source '{source}' is not supported.")

    data = CRAWLERS[source](**kwargs)

    if return_format == "df":
        return data
    elif return_format == "csv":
        with StringIO() as out:
            data.to_csv(out)
            content = out.getvalue()
        return content
    elif return_format == "records":
        return data.to_dict(orient="records")

if __name__ == "__main__":
    print(crawl("krepsinis", return_format="csv", time_limit=10, search_word = "žalgir"))