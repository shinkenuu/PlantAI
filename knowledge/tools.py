from langchain_core.tools import tool
from typing import Annotated

# Example symptom-cause mapping for demonstration
SYMPTOM_CAUSE_DB = {
    ("Spathiphyllum wallisii", "blackened flowers"): [
        "Overwatering can cause blackened flowers.",
        "Fungal infections are a common cause of blackened flowers in peace lilies.",
        "Cold drafts or sudden temperature drops may blacken flowers.",
        "Natural aging: Peace lily flowers turn black as they age.",
    ],
    # Add more (scientific_name, symptom) pairs as needed
}


@tool
def get_symptom_causes(
    scientific_name: Annotated[str, "Scientific name of the plant"],
    symptom: Annotated[
        str, "Observed symptom (e.g., 'yellowing leaves', 'blackened flowers')"
    ],
) -> str:
    """Returns possible causes for a given symptom in a specific plant, based on care guides and known issues."""
    key = (scientific_name, symptom)
    causes = SYMPTOM_CAUSE_DB.get(key)
    if not causes:
        return f"No known causes found for '{symptom}' in {scientific_name}."
    return "Possible causes for '{}':\n- {}".format(symptom, "\n- ".join(causes))
