
import time
import pandas as pd
import pytest
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from config import settings as config_settings
from services.multi_agent_service import handle_query

# Constants
RESULTS_FILE = "test_results_query.json"

# Load dataset
df = pd.read_csv(config_settings.TELECOM_DATA_SOURCE_PATH)

# Test Queries
test_queries = [
    ("Total sales for August and September 2024", "418,411"),
    ("Tell me the total sales more than 7000 units in August 2024", "137,239"),
    ("What is the error code when remote reaches its pairing limit ?", "457"),
    ("What is the error code for partial signal loss ?", "002"),
    ("How is the weather today?", "Sorry, I couldn't classify your request."),
    ("Hi", "Sorry, I couldn't classify your request."),
]

test_intents_map = {
    "Total sales for August and September 2024": "marketing",
    "Tell me the total sales more than 7000 units in August 2024": "marketing",
    "What is the error code when remote reaches its pairing limit ?": "technical",
    "What is the error code for partial signal loss ?": "technical",
    "How is the weather today?": "other",
    "Hi": "other"
}

# Store results
query_results = []

@pytest.mark.parametrize("query, expected_label", test_queries)
def test_agent_response(query, expected_label):
    """Test query classification, accuracy, and NER extraction."""
    start_time = time.time()
    response = handle_query(query)
    end_time = time.time()
    latency = end_time - start_time

    query_results.append({
        "intent": test_intents_map[query], 
        "latency": latency, 
    })

    assert expected_label in response, f"Incorrect classification for query: {query}"
    assert latency <= 10, f"Query took too long: {latency}s"

@pytest.fixture(scope="session", autouse=True)
def save_results():
    """Save test results after all tests complete."""
    yield  # Wait until all tests finish

    if query_results:
        with open(RESULTS_FILE, "w") as f:
            json.dump(query_results, f, indent=4)
        print(f"\nTest results saved to {RESULTS_FILE}")

def visualize_results():
    try:
        with open(RESULTS_FILE, "r") as f:
            query_results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No data available! Run tests first.")
        return

    if not query_results:
        print("No data available! Run tests first.")
        return

    df_results = pd.DataFrame(query_results)
    print("\nData Collected:\n", df_results)
    df_summary = df_results.groupby(by="intent").agg({'latency': 'mean'}).reset_index()
    print("\nData summary:\n",df_summary)

    # Latency Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df_summary["intent"], y=df_summary["latency"], palette="Blues")
    plt.xlabel("Query")
    plt.ylabel("Latency (s)")
    plt.title("Query Latency Analysis by Intent")
    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig("assets/test_analysis/query_latency_analysis.png", bbox_inches="tight")

    os.remove(RESULTS_FILE)
    print("Test results file deleted after visualization.")

if __name__ == "__main__":
    import sys

    if "--visualize" in sys.argv:
        visualize_results()
    else:
        pytest.main(["-v", "--capture=no"])
