from bson import ObjectId
from core.init_DB import get_db  
from core.config import settings 

class PolicyDB:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db[settings.POLICIES_COLLECTION]

    def insert_policy(self, policy: dict) -> str:
        """
        Inserts a policy document into the collection.
        Returns the inserted document's ID as a string.
        """
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", policy)
        result = self.collection.insert_one(policy)
        return str(result.inserted_id)

    def get_policy(self, policy_id: str) -> dict | None:
        """
        Retrieves a policy document by its ID.
        Returns the document or None if not found.
        """
        try:
            policy = self.collection.find_one({"_id": ObjectId(policy_id)})
            if policy:
                policy["_id"] = str(policy["_id"])
            return policy
        except Exception as e:
            print(f"Error retrieving policy: {e}")
            return None


    def delete_policy(self, policy_id: str) -> bool:
        """
        Deletes a policy by its ID.
        Returns True if a document was deleted, False otherwise.
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(policy_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting policy: {e}")
            return False
