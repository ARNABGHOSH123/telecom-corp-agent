import time
import pandas as pd
import pytest
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from utils import intent_classifier
import sys

# Constants
RESULTS_FILE = "test_results.json"

# Test Queries
test_queries = [
    ("Total sales for August 2024", "marketing"),
    ("What does Black Screen - No Guide error mean ?", "technical"),
    ("What are the sales of September 2024 above 6000", "marketing"),
    ("How is the weather today?", "other"),
]

# Store results
query_results = []
latencies = []
true_labels = []
predicted_labels = []


@pytest.mark.parametrize("query, expected_label", test_queries)
def test_agent_response(query, expected_label):
    """Test query classification, accuracy, and NER extraction."""
    start_time = time.time()
    response = intent_classifier.classify_intent(query)
    end_time = time.time()
    latency = end_time - start_time

    predicted_label = response.lower()

    query_results.append(
        {
            "query": query,
            "latency": latency,
            "expected_label": expected_label,
            "predicted_label": predicted_label,
        }
    )

    latencies.append(latency)
    true_labels.append(expected_label)
    predicted_labels.append(predicted_label)

    assert (
        predicted_label == expected_label
    ), f"Incorrect classification for query: {query}"
    assert latency < 7, f"Query took too long: {latency}s"


@pytest.fixture(scope="session", autouse=True)
def save_results():
    """Save test results after all tests complete."""
    yield  # Wait until all tests finish

    if query_results:
        with open(RESULTS_FILE, "w") as f:
            json.dump(query_results, f, indent=4)
        print(f"\nTest results saved to {RESULTS_FILE}")


def visualize_results():
    """Generate graphs for latency, classification, and NER results, then delete the results file."""
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

    # Latency Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df_results["query"], y=df_results["latency"], palette="Blues")
    plt.xlabel("Query")
    plt.ylabel("Latency (s)")
    plt.title("Intent classification Latency Analysis")
    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig(
        "assets/test_analysis/intent_classification_latency_analysis.png",
        bbox_inches="tight",
    )

    # Classification Report
    true_labels = df_results["expected_label"]
    predicted_labels = df_results["predicted_label"]
    report = classification_report(true_labels, predicted_labels, output_dict=True)

    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        confusion_matrix(true_labels, predicted_labels, labels=list(set(true_labels))),
        annot=True,
        fmt="d",
        cmap="Blues",
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Classification Confusion Matrix")
    plt.savefig("assets/test_analysis/intent_classification_matrix.png")

    print(pd.DataFrame(report))

    # Delete the test results file after visualization
    os.remove(RESULTS_FILE)
    print("🗑️ Test results file deleted after visualization.")


if __name__ == "__main__":

    if "--visualize" in sys.argv:
        visualize_results()
    else:
        pytest.main(["-v", "--capture=no"])
