from bson.objectid import ObjectId
from core.init_DB import get_db
from core.config import settings

class AssessmentDB:
    def __init__(self):
       self.db = get_db()
       self.collection = self.db[settings.ASSESSMENTS_COLLECTION]
       
    def insert_assessment(self, assessement: dict) -> str:
        """Insert an assessment policy (as a dictionary) into the database."""
        print("Inserting assessment:\n", assessement)
        result = self.collection.insert_one(assessement)
        return str(result.inserted_id)

    def get_assessment(self, id: str) -> dict | None:
        """Retrieve an assessment document by ID."""
        try:
            return self.collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error retrieving assessment: {e}")
            return None

    def delete_assessment(self, id: str) -> bool:
        """Delete an assessment by ID."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting assessment: {e}")
            return False
