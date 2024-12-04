import requests

api_key = "dd517ea9b56e47a196b5c5a742374355"


def get_news(selected_popularity, selected_filter, filter_value):
    """Fetch and return news articles based on the parameters."""
    news_url = f"https://newsapi.org/v2/{selected_popularity}?{selected_filter}={filter_value}&apiKey={api_key}"
    response = requests.get(news_url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return None


def get_dynamic_values(filter_type):
    """Return the dynamic combobox values based on the filter type."""
    if filter_type == "language":
        return ("ar", "de", "en")
    elif filter_type == "country":
        return ("id", "hu", "us", "ua")
    elif filter_type == "category":
        return ("business", "entertainment", "general", "health", "science", "sports", "technology")
    return []
