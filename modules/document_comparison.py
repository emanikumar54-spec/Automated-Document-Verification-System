
from difflib import SequenceMatcher


def normalize(value):
    """Normalize values before comparison."""
    if value is None:
        return None

    return " ".join(str(value).lower().strip().split())


def compare_values(value1, value2):
    """Compare two extracted values."""

    if not value1 or not value2:
        return "Missing"

    if normalize(value1) == normalize(value2):
        return "Match"

    similarity = SequenceMatcher(
        None,
        normalize(value1),
        normalize(value2)
    ).ratio()

    if similarity >= 0.90:
        return "Possible Match"

    return "Mismatch"


def compare_documents(document1, document2):
    """Compare all common fields across two documents."""

    results = {}

    all_fields = set(document1.keys()) | set(document2.keys())

    for field in sorted(all_fields):
        value1 = document1.get(field)
        value2 = document2.get(field)

        results[field] = {
            "document_1": value1,
            "document_2": value2,
            "status": compare_values(value1, value2)
        }

    return results


def generate_summary(results):
    """Generate comparison statistics."""

    summary = {
        "total_fields": len(results),
        "matching": 0,
        "possible_matches": 0,
        "mismatching": 0,
        "missing": 0
    }

    for result in results.values():
        status = result["status"]

        if status == "Match":
            summary["matching"] += 1
        elif status == "Possible Match":
            summary["possible_matches"] += 1
        elif status == "Mismatch":
            summary["mismatching"] += 1
        else:
            summary["missing"] += 1

    return summary
