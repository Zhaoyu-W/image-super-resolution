from datetime import timedelta

LIMIT=10
ADOBE_URL="https://stock.adobe.io/Rest/Media/1/Search/Files?search_parameters[filters][content_type:photo]=1&search_parameters[limit]={}&search_parameters[offset]={}"
PEXELS_URL="https://api.pexels.com/v1/curated?per_page={}&page={}"
PIXABAY_URL="https://pixabay.com/api/?key={}&page={}&per_page={}"
AIRFLOW_DEFAULT_ARGS = {
    "owner": "zw577",
    "email_on_failure": False,
    "email_on_retry": False,
    "provide_context": True,
    "retries": 3,
    "retry_delay": timedelta(minutes=3)
}
