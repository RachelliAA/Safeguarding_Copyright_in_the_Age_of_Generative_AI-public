from bson.objectid import ObjectId
from core.init_DB import get_db
from core.config import settings

class ActionDB:
    def __init__(self):
       self.db = get_db()
       self.collection = self.db[settings.ACTIONS_COLLECTION]
       
    def insert_action(self, action: dict) -> str:
        """Insert an action (as a dictionary) into the database."""
        print("Inserting action:\n", action)
        result = self.collection.insert_one(action)
        print("Action inserted with ID:", result.inserted_id)
        return str(result.inserted_id)

    def get_action(self, id: str) -> dict | None:
        """Retrieve an action document by ID."""
        try:
            return self.collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error retrieving action: {e}")
            return None

    def delete_action(self, id: str) -> bool:
        """Delete an action by ID."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting action: {e}")
            return False
