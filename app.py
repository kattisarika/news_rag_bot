import requests
from bs4 import BeautifulSoup
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def get_news_articles(source="TOI"):

    if source == "TOI":
        return fetch_from_toi()

    elif source == "BBC":
        return fetch_from_bbc()

    elif source == "NY TIMES":
        return fetch_from_nytimes()

    elif source == "WEATHER":
        return fetch_sample_weather()

    elif source == "GRAPHQL":
        return fetch_from_graphql()

    else:
        return []


# -------------------------
# TIMES OF INDIA
# -------------------------

def fetch_from_toi():

    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="xml")

        items = soup.find_all("item")

        articles = []

        for item in items[:10]:

            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"

            articles.append(
                f"[{title}]({link})"
            )

        return articles

    except Exception as e:
        return [f"Error fetching Times of India: {e}"]


# -------------------------
# BBC
# -------------------------

def fetch_from_bbc():

    url = "https://feeds.bbci.co.uk/news/rss.xml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="xml")

        items = soup.find_all("item")

        articles = []

        for item in items[:10]:

            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"

            articles.append(
                f"[{title}]({link})"
            )

        return articles

    except Exception as e:
        return [f"Error fetching BBC: {e}"]


# -------------------------
# NEW YORK TIMES
# -------------------------

def fetch_from_nytimes():

    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="xml")

        items = soup.find_all("item")

        articles = []

        for item in items[:10]:

            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"

            articles.append(
                f"[{title}]({link})"
            )

        return articles

    except Exception as e:
        return [f"Error fetching NY Times: {e}"]


# -------------------------
# WEATHER
# -------------------------

def fetch_sample_weather():

    try:

        with open(
            "sample_weather.xml",
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        soup = BeautifulSoup(content, "xml")

        items = soup.find_all("item")

        results = []

        for item in items[:10]:

            title = (
                item.title.text
                if item.title
                else "Weather"
            )

            description = (
                item.description.text
                if item.description
                else ""
            )

            results.append(
                f"{title}. {description}"
            )

        return results

    except Exception as e:

        return [
            f"Error reading weather data: {e}"
        ]


# -------------------------
# GRAPHQL
# -------------------------

def fetch_from_graphql():

    try:

        transport = RequestsHTTPTransport(
            url="https://countries.trevorblades.com/",
            verify=True,
            retries=3
        )

        client = Client(
            transport=transport,
            fetch_schema_from_transport=True
        )

        query = gql(
            """
            {
                countries {
                    name
                    capital
                    emoji
                }
            }
            """
        )

        result = client.execute(query)

        articles = []

        for country in result["countries"][:10]:

            name = country["name"]

            capital = country.get(
                "capital"
            ) or "N/A"

            emoji = country.get(
                "emoji"
            ) or ""

            articles.append(
                f"{emoji} **{name}** – Capital: {capital}"
            )

        return articles

    except Exception as e:

        return [
            f"Error fetching GraphQL data: {e}"
        ]
