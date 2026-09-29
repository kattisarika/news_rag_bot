import requests
from bs4 import BeautifulSoup
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# =========================================================
# TIMES OF INDIA TOOL
# =========================================================

def fetch_from_toi():

    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
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


# =========================================================
# BBC TOOL
# =========================================================

def fetch_from_bbc():

    url = "https://feeds.bbci.co.uk/news/rss.xml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
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


# =========================================================
# NEW YORK TIMES TOOL
# =========================================================

def fetch_from_nytimes():

    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
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


# =========================================================
# WEATHER TOOL
# =========================================================

def fetch_sample_weather():

    try:

        with open(
            "sample_weather.xml",
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        soup = BeautifulSoup(content, "xml")
        items = soup.find_all("item")

        weather_results = []

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

            weather_results.append(
                f"{title}: {description}"
            )

        return weather_results

    except Exception as e:

        return [
            f"Error reading weather data: {e}"
        ]


# =========================================================
# GRAPHQL COUNTRY TOOL
# =========================================================

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

        countries = []

        for country in result["countries"][:10]:

            name = country["name"]

            capital = (
                country.get("capital")
                or "N/A"
            )

            emoji = (
                country.get("emoji")
                or ""
            )

            countries.append(
                f"{emoji} **{name}** - Capital: {capital}"
            )

        return countries

    except Exception as e:

        return [
            f"Error fetching GraphQL data: {e}"
        ]
