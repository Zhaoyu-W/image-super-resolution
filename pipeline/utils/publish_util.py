import requests


def publish_metadata(metadata, topic):
    for meta in metadata:
        if not meta:
            continue

        data = {
            "id": meta["{}_id".format(topic)],
            "title": meta["title"],
            "original_url": meta["original_url"],
            "topic": topic,
        }
        headers = {"Content-Type": "application/json"}

        requests.post(
            "http://publisher:8000/send",
            headers=headers,
            json=data,
        )
