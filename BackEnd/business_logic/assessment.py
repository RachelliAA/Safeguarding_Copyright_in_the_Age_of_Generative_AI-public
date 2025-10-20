#from pymongo import MongoClient
#from bson import ObjectId #, Binary
from datetime import datetime
from pydantic import ValidationError
#from PIL import Image
import tempfile
import os
import time
import base64
import pandas as pd
from datetime import datetime, timezone

from database.assessment_DB import AssessmentDB
#from core.init_DB import init_db_client, get_db
#from core.config import settings

from .assessment_agent import AssessmentAgent
from tools.clip_similarity import ClipSimilarityTool
from tools.image_to_json import ImageToJsonTool
from tools.image_to_text import ImageToTextTool
from database.policy_DB import PolicyDB
from .assessment_validation import AssessmentSchema


class Assessment:
    def __init__(self, image_data: bytes, image_url: str, policy_id: str):
        #self.client = init_db_client()
        #self.collection = get_db()[settings.ASSESSMENTS_COLLECTION]
        self.db = AssessmentDB()  # Initialize the database instance

        self.image_data = image_data
        self.image_url = image_url
        self.policy_id = policy_id

        self.results = None
        self.policy_breach = None
        self.used_tools = None
        self.assessment_id = None
        self.time_stamp = None
        self.violations = None

    async def create_assessment(self, prompt, image_data, local_image_path):
        """
        creats the assesment and saves it to the dataset
        """
        results = await self.assess()
        self.save_assessment_to_dataset(prompt, image_data, local_image_path)
        return results


    async def assess(self) -> dict:
        """
        Main assessment pipeline.
        This method retrieves the policy text, saves the image to a temporary file,
        initializes the assessment agent with tools, and performs the assessment.
        It returns a dictionary with the assessment results.
        """
        
        policy_text = self.get_policy_to_assess(self.policy_id)
        if not policy_text:
            raise ValueError(f"Policy not found for ID: {self.policy_id}")

        temp_image_path = self._save_temp_image()

        try:
            tools = {
                "compare_images": ClipSimilarityTool().search_similar_images,
                "image_to_json": ImageToJsonTool().analyze_caricature,
                "image_to_text": ImageToTextTool().describe_image
            }

            agent = AssessmentAgent(tools) #creats the agent with the tools
            self.results = agent.analyze_image(temp_image_path, policy_text) #calls the agent to analyze the image
            print(f"[Assessment] Results: {self.results}")
            self.policy_breach = self.results.get("breach", False)
            print(f"[Assessment] Breach detected: {self.policy_breach}")
            self.violations = self.results.get("violations", None)
            print(f"[Assessment] Violations: {self.violations}")
            assessment_data = self._build_assessment_data()
            self.time_stamp = assessment_data["created_at"]

            validated = self.validate_assessment(assessment_data)
            if not validated:
                raise ValueError("Assessment validation failed.")

            #result = self.collection.insert_one(validated.model_dump(by_alias=True))
            #db = AssessmentDB()
            inserted_id = self.insert_assessment(assessment_data)#turn the object to a dictionary and insert it into the database
            self.assessment_id = str(inserted_id)
            print(f"[Assessment] Inserted with ID: {self.assessment_id}")
        except Exception as e:
            print(e)
        finally:
            self._cleanup_temp_file(temp_image_path)
        
        return {
            "assessment_id": self.assessment_id,
            "image_data": base64.b64encode(self.image_data).decode("utf-8"),  # encode bytes to base64 string
            "breach": self.policy_breach,  #bool
            "violations": self.violations, #string
            "created_at": self.time_stamp, #.isoformat(),
            "status": "completed"
        }

    def _save_temp_image(self) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(self.image_data)
            print(f"[TempFile] Saved image to {tmp_file.name}")
            return tmp_file.name

    def _cleanup_temp_file(self, path: str):
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"[TempFile] Deleted temporary image {path}")
            except PermissionError:
                print("[TempFile] Permission error; retrying...")
                time.sleep(1)
                os.remove(path)

    def _build_assessment_data(self) -> dict:
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')#gets the current time in UTC
        return {
            "title": "Image Assessment Result",
            "description": f"Assessment for image {self.image_url} against policy {self.policy_id}",
            "image_data": self.image_data,
            "policy_id": self.policy_id,
            "violation": self.violations,
            "results": self.results,
            "created_at": current_time,
            "updated_at": current_time,
            "policy_breach": self.policy_breach,
            "status": "completed"
        }

    def get_policy_to_assess(self, policy_id: str) -> str:
        return PolicyDB().get_policy(policy_id)

    def validate_assessment(self, assessment: dict) -> AssessmentSchema:
        try:
            validated = AssessmentSchema(**assessment)
            print("[Validation] Assessment schema validation successful.")
            return validated
        except ValidationError as e:
            print("[Validation] Assessment validation failed:")
            print(e.json())
            return None

    def insert_assessment(self, assessment_data) -> str:
        validated = self.validate_assessment(assessment_data)
        if not validated:
            raise ValueError("Assessment validation failed.")
        
        #db = AssessmentDB()
        inserted_id = self.db.insert_assessment(validated.model_dump()) #turn the object to a dictionary and insert it into the database
        self.assessment_id = str(inserted_id)

        #result = self.collection.insert_one(validated.model_dump())
        print(f"[Assessment] Manually inserted with ID: {self.assessment_id}")
        return str(self.assessment_id)

    def get_assessment(self, id: str) ->str | None:
        try:
            #obj_id = ObjectId(id)
            return self.db.get_assessment(id) #  collection.find_one({"_id": obj_id})
        except Exception as e:
            print(f"[DB] Error fetching assessment: {e}")
            return None

    def delete_assessment(self, id: str) -> bool:
        try:
            results = self.db.delete_assessment(id) #self.collection.delete_one({"_id": obj_id})
            if results:
                print(f"[DB] Assessment with ID {id} deleted successfully.")
            else:
                print(f"[DB] No assessment found with ID {id}.")
            return results
        except Exception as e:
            print(f"[DB] Error deleting assessment: {e}")
            return False
        
    def save_assessment_to_dataset(self, prompt, image_data,local_image_path):
        """
        Saves the assessment to an excell tadaset with columns: character name, prompt, generated image (path), highest similarity score, second highest sim score,
        ref image with sim, ref image with 2nd highest sim,  assessment, breach/not breach.
        """
        if self.results is None:
            print("assessment past, no need to save.")
            return  
        else:
            # print("@@@@@@@@\n", self.results)
            # current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')#gets the current time in UTC
            # character_name = self.results.get("image_to_json", {}).get("celebrity", {}).get("name", "Unknown")
            # #generated_image_path = getattr(self, "image_url", "No image path")
            # # facial_similarity_score = self.results.get("image_to_json", {}).get("celebrity", {}).get("facial_similarity_score", 0)
            #     # Extract top 2 similarity scores
            # top_2 = self.results.get("clip_similarity", {}).get("top_2", [])
            # first = top_2[0] if len(top_2) > 0 else {}
            # second = top_2[1] if len(top_2) > 1 else {}

            # first_highest_similarity_score = first.get("score", 0)
            # second_highest_similarity_score = second.get("score", 0)
            # ref_image_with_sim = first.get("filename", "No image")
            # ref_image_with_2nd_highest_sim = second.get("filename", "No image")
            # assessment = self.results.get("violations", "No assessment")
            # breach = self.results.get("breach", False)
            # violation = self.results.get("violations", [])

            # data = {
            #     "timestamp": [current_time],
            #     "character_name": [character_name],
            #     "prompt": [prompt],
            #     "generated_image_local_path": [local_image_path],
            #     "ref_image_with_sim": [ref_image_with_sim],
            #     "first_highest_similarity_score": [first_highest_similarity_score],
            #     "ref_image_with_2nd_highest_sim": [ref_image_with_2nd_highest_sim],
            #     "second_highest_similarity_score": [second_highest_similarity_score],
            #     "assessment": [assessment],
            #     "breach": [breach],
            #     "violation": [violation]
            # }
            print("@@@@@@@@\n", self.results)
            current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')  # UTC time

            # -------- Character Name Extraction Logic -------- #
            image_to_json = self.results.get("image_to_json", {})

            if image_to_json:
                celebrity_data = image_to_json.get("celebrity")
                character_name = celebrity_data.get("name") if celebrity_data else None
            else:
                # Fallback to image_to_text
                image_to_text = self.results.get("image_to_text", "")
                character_name = image_to_text[:50] + "..." if image_to_text else "Unknown"

            # -------- Clip Similarity -------- #
            top_2 = self.results.get("clip_similarity", {}).get("top_2", [])
            first = top_2[0] if len(top_2) > 0 else {}
            second = top_2[1] if len(top_2) > 1 else {}

            first_highest_similarity_score = first.get("score", 0)
            second_highest_similarity_score = second.get("score", 0)
            ref_image_with_sim = first.get("filename", "No image")
            ref_image_with_2nd_highest_sim = second.get("filename", "No image")

            # -------- Assessment & Violation -------- #
            assessment = self.results.get("violations", "No assessment")
            breach = self.results.get("breach", False)
            violation = self.results.get("violations", [])

            # -------- Final Data Dictionary -------- #
            data = {
                "timestamp": [current_time],
                "character_name": [character_name],
                "prompt": [prompt],
                "generated_image_local_path": [local_image_path],
                "ref_image_with_sim": [ref_image_with_sim],
                "first_highest_similarity_score": [first_highest_similarity_score],
                "ref_image_with_2nd_highest_sim": [ref_image_with_2nd_highest_sim],
                "second_highest_similarity_score": [second_highest_similarity_score],
                "assessment": [assessment],
                "breach": [breach],
                "violation": [violation]
            }
                        
            df = pd.DataFrame(data)
            csv_file_path = "assessment_dataset1.csv"

            if os.path.exists(csv_file_path):
                df.to_csv(csv_file_path, mode='a', index=False, header=False)
            else:
                df.to_csv(csv_file_path, index=False)