import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = "repair-loop"

client = None

if API_KEY:
    client = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=API_KEY
    )


def save_memory(device, problem, solution, outcome):
    if not client:
        return False

    content = (
        f"REPAIR CASE. Device: {device}. "
        f"Problem: {problem}. "
        f"Solution: {solution}. "
        f"Outcome: {outcome}."
    )

    try:
        client.retain(
            bank_id=BANK_ID,
            content=content
        )
        return True

    except Exception as e:
        print("Memory save error:", e)
        return False


def search_memory(query):
    if not client:
        return []

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        return [memory.text for memory in result.results]

    except Exception as e:
        print("Memory search error:", e)
        return []