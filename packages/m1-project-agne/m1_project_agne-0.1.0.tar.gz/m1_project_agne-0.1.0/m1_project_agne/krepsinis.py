from lxml.etree import HTML
from requests import get
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

base_url = "https://www.krepsinis.net"
response = get(base_url)
tree = HTML(response.text)


def search_in_articles(data, target_word):
    """
    Searches for articles containing a specified word in their titles.

    Args:
        data (List[Dict[str, Union[str, List[str]]]]): A list of dictionaries representing articles.
            Each dictionary should have "title" as a string.
        target_word (str): The word to search for in article titles.

    Returns:
        List[Dict[str, Union[str, List[str]]]]: A list of dictionaries representing articles that contain the specified word.
            Each dictionary has "title" as a string, "url" as a string, and "image" as a string representing the URL
            of the corresponding image.
    """
    matching_articles = []

    for article in data:
        title = article.get("title", "").lower()
        if target_word.lower() in title:
            matching_articles.append(article)

    return matching_articles

def crawl_krepsinis(base_url = "https://www.krepsinis.net", time_limit: int = 60, search_word: str or None = None):
    """
    Crawls the 'https://www.krepsinis.net/' webpage, extracting articles with scrolling.

    Args:
        base_url (str, optional): The base URL used to construct complete URLs. Default is "https://www.krepsinis.net".
        time_limit (int, optional): The maximum time in seconds allowed for the function to run. Default is 60 seconds.
        search_word (str or None, optional): A word to search for in article titles. If provided, only articles containing
            the specified word will be included in the result. Default is None.

    Returns:
        pd.DataFrame: A DataFrame where each row represents an article.
            The DataFrame has "title" as a string, "url" as a string, and "image" as a string representing the URL
            of the corresponding image.

    Raises:
        ValueError: If there is an issue during extraction.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        start_time = time.time()

        driver.get(base_url)
        def scroll_down(driver):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        while time.time() - start_time < time_limit:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            scroll_down(driver)

        page_source = driver.page_source
        tree = HTML(page_source)

        articles = tree.xpath("//a[@class='a-text']")
        article_data = []
        n = 0

        for article in articles:
            title_list = article.xpath("text()")
            title = ' '.join(title.strip() for title in title_list) if title_list else None

            url = base_url + str(article.xpath("@href")[0]).replace("['", "").replace("']", "") if article.xpath("@href") else None

            # Extract the corresponding image for each article
            image = article.xpath("//a[@class='image']/img/@src")
            image_url = str(image[n]).replace("['", "").replace("']", "") if image else None
            n += 1


            if title and url:
                article_data.append({"title": title, "url": url, "image": image_url})
            else:
                raise ValueError("Error extracting title or URL for an article.")

        if search_word is not None:
            return pd.DataFrame(search_in_articles(article_data, search_word))
        else:
            return pd.DataFrame(article_data)

    except Exception as e:
        raise ValueError(f"Error during extraction: {e}")

    finally:
        driver.quit()



