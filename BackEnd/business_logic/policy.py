from datetime import datetime, timezone
import json
from database.policy_DB import PolicyDB
from .policy_agent import PolicyAgent
from .policy_validation import validate_policy
import pdb  # Import the Python debugger

class Policy:
    def __init__(self,  db = None):
        if db is None:
                db = PolicyDB()
        self.db = db
    
    def create_policy(self, NL_input: str) -> dict:
        """
        Converts natural language input to a structured policy dictionary.
        """
        policy_agent = PolicyAgent(NL_input)
        generated_policy = policy_agent.generate_policy()
        print("generated policy after agent\n")
       
        validated_policy = validate_policy(generated_policy)
        print("\nvalidated_policy\n", validated_policy)
        print("\ntypeof validated_policy is:\n ", type(validated_policy))
        if not validated_policy:
            raise ValueError("Policy validation failed.")

        self.policy = validated_policy.model_dump()  # store the dict version
        print("\n###################################################\n\n self.policy", json.dumps(self.policy, indent=2)) 
        print("\ntypeof policy is:\n ", type(self.policy))
        id = self.insert_policy()
        #print("typeof policy is: ", type(self.policy))
        return self.policy, id

    def insert_policy(self) -> str | None:
        """
        gets a policy adds the current time and saves it in the database.
        Returns the inserted policy ID or None on failure.
        """
        from json import dumps
        print("Inserting policy:\n", dumps(self.policy, indent=2))

        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')#gets the current time in UTC
        self.policy["created_at"] = current_time
        self.policy["updated_at"] = current_time

        validated_policy = validate_policy(self.policy) #makes sure the policy is in the correct formats
        if not validated_policy:
            print("Policy validation failed.")
            return None
        
        return self.db.insert_policy(validated_policy.model_dump())  # trune the policy to dict format and then Saves the validated policy to the database


    def get_policy(self, policy_id: str) -> dict | None:
        """
        Retrieves a policy by ID.
        """
        #pdb.set_trace()  # This will drop you into interactive debugging
        """Fetches the policy document and formats it into a readable text for assessment."""
        try:
            policy_doc = self.db.get_policy(policy_id)
            if not policy_doc:
                print(f"Policy with ID {policy_id} not found.")
                return ""

            # Compose a descriptive text from the policy document
            name = policy_doc.get("name", "")
            domain = policy_doc.get("domain", "")
            description = policy_doc.get("description", "")
            scope = policy_doc.get("scope", "")
            constraints = policy_doc.get("constraints", [])
            prohibited_actions = policy_doc.get("prohibited_actions", [])

            # Format it into a text blob
            policy_text = f"Policy Name: {name}\n"
            policy_text += f"Domain: {domain}\n"
            policy_text += f"Scope: {scope}\n"
            policy_text += f"Description: {description}\n"
            policy_text += "Constraints:\n" + "\n".join(f"- {c}" for c in constraints) + "\n"
            policy_text += "Prohibited Actions:\n" + "\n".join(f"- {a}" for a in prohibited_actions)

            return policy_text

        except Exception as e:
            print(f"Error retrieving policy: {e}")
            return ""


    def delete_policy(self, policy_id: str) -> bool:
        """
        Deletes a policy by ID.
        """
        return self.db.delete_policy(policy_id)
