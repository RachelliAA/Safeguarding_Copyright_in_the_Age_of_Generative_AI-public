
from datetime import datetime, timezone


class Action:
    def __init__(self, action_db, model: str, provider: str ,user_id: int = None, prompt: str = None, image_url: str = None):
        """
        - provider: image generation provider (e.g., "together")
        - model: default model to use
        - storage: instance of an image storage service (e.g., S3Storage)
        """
        self.action_DB = action_db
        self.action_id = None
        self.action_type = "image_generation"
        self.time_stamp= None
        self.user_id = user_id
        self.prompt = prompt
        self.provider = provider
        self.model = model
        self.image_url = image_url

    def insert_action(self):
        """
        Insert the action into the database.
        """
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')#gets the current time in UTC
        self.time_stamp = current_time
        action_data = {
            "action_type": self.action_type,
            "time_stamp": self.time_stamp,
            "user_id": self.user_id,
            "prompt": self.prompt,
            "provider": self.provider,
            "model": self.model,
            "image_url": self.image_url
        }
        print("Inserting action:\n", action_data)
        id = self.action_DB.insert_action(action_data)
        if not id:
            raise ValueError("Failed to insert action into the database.")
        self.action_id = id
        print("Action inserted with ID in action:", self.action_id)
        return self.action_id
    
    def get_action(self, id: str):
        """ Retrieve an action document by ID."""
        action = self.actionDB.get_action(id)
        if action:
            self.action_id = action.get("action_id")
            self.action_type = action.get("action_type")
            self.time_stamp = action.get("time_stamp")
            self.user_id = action.get("user_id")
            self.prompt = action.get("prompt")
            self.provider = action.get("provider")
            self.model = action.get("model")
            self.image_url = action.get("image_url")
        return action
    
    def delete_action(self, id: str):
        """Delete an action by ID."""
        return self.actionDB.delete_action(id)
    






      