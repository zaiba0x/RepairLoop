
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# 1. Load the API key
load_dotenv()
API_KEY = os.getenv("HINDSIGHT_API_KEY")

# 2. Connect to Hindsight
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=API_KEY
)

BANK_ID = "repair-loop"

print("Welcome to RepairLoop!")

# 3. Ask for repair details
device = input("Enter device name: ")
problem = input("Enter device problem: ")
solution = input("Enter repair solution: ")
result = input("Was it fixed? (yes/no): ")

# 4. Create a repair memory
memory_text = (
    f"Device: {device}. "
    f"Problem: {problem}. "
    f"Solution: {solution}. "
    f"Result: {result}."
)

# 5. Save the repair memory
client.retain(
    bank_id=BANK_ID,
    content=memory_text
)

print("\nRepair case saved successfully!")

# 6. Search for similar repair history
query = f"Repair history for device: {device}. Problem: {problem}. Find past solutions and repair outcomes."

memory_result = client.recall(
    bank_id=BANK_ID,
    query=query
)

# 7. Display the recalled memories
print("\nRepairLoop Recommendations")

if memory_result.results:
    print("Similar past repairs were found!")

    for memory in memory_result.results:
        print("\nPast repair:", memory.text)

    print("\nSuggested next step:")
    print(
        "Review the previous repair solutions "
        "and verify whether they apply to this case."
    )

else:
    print("No similar repair history found.")
    print("Collect more information before suggesting a solution.")
# 8. Close the connection
client.close()