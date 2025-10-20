# from datetime import datetime
# from database.policyDB import PolicyDB  # Adjust path as needed

# def run_tests():
#     db = PolicyDB()

#     # Sample policy to test with
#     policy = {
#         "name": "Test Policy",
#         "domain": "Image",
#         "description": "Test description",
#         "scope": "Test scope",
#         "constraints": [
#             "Do not test in production"
#         ],
#         "prohibited_actions": [
#             "Inserting fake data into production"
#         ],
#         "parameters": {
#             "hairstyle": None,
#             "outfit": None,
#             "accessories": None
#         },
#         "enforcement": {
#             "methods": [
#                 {
#                     "name": "CLIPSimilarityTool",
#                     "threshold": 0.0
#                 }
#             ]
#         },
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow(),
#         "status": "draft",
#         "version": 1
#     }

#     print("Inserting policy...")
#     policy_id = db.insert_policy(policy)
#     print(f"Inserted with ID: {policy_id}")

#     print("\nRetrieving policy...")
#     retrieved = db.get_policy(policy_id)
#     if retrieved:
#         print("Retrieved successfully:")
#         print(retrieved)
#     else:
#         print("Failed to retrieve.")

#     print("\nDeleting policy...")
#     deleted = db.delete_policy(policy_id)
#     print("Deleted:" if deleted else "Delete failed")

#     print("\nVerifying deletion...")
#     should_be_none = db.get_policy(policy_id)
#     if should_be_none is None:
#         print("Policy successfully deleted.")
#     else:
#         print("Policy still exists!")

# if __name__ == "__main__":
#     run_tests()
from pydantic import BaseModel
from pprint import pprint

class Policy(BaseModel):
    name: str
    domain: str
    description: str
    scope: str
    constraints: list[str]
    prohibited_actions: list[str]
    parameters: dict
    enforcement: dict
    status: str
    version: int

# Create a policy object
policy = Policy(
    name="Test Policy",
    domain="Image",
    description="Test description",
    scope="Test scope",
    constraints=["Do not test in production"],
    prohibited_actions=["Inserting fake data into production"],
    parameters={"hairstyle": None, "outfit": None, "accessories": None},
    enforcement={"methods": [{"name": "CLIPSimilarityTool", "threshold": 0.0}]},
    status="draft",
    version=1
)

# Pretty-print the policy data
print(policy)
pprint(policy.model_dump())