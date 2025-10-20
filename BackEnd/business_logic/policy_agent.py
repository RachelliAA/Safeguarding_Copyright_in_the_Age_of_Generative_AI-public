# import json
# from instruction_prompts import policy_instruction
# from core.init_llm import init_llm_client


# class PolicyAgent:
#     def __init__(self, NL_policy, model="gpt-4"):
#         self.NL_policy = NL_policy
#         self.model = model
#         self.instructions = self.load_instructions(policy_instruction)
#         self.llm_client = self.get_llm_client()

#     def load_instructions(self, file_path):
#         """Load instructions from a separate file."""
#         with open(file_path, "r") as file:
#             return file.read()


#     def generate_policy(self):
#         """Generate a policy based on natural language input."""

#         messages = [
#             {"role": "system", "content": self.instructions},
#             {"role": "user", "content": self.NL_policy}
#         ]

#         response = self.llm_client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             max_tokens=500
#         )
#         print("FULL response from gpt:\n ",response)
#         response_content = response.choices[0].message.content.strip("```json").strip("```")
#         print("\n\n\n\n response_content: ",response_content)
#         return json.loads(response_content)


import json
from core.init_llm import get_llm_client  

class PolicyAgent:
    def __init__(self, NL_policy, model="gpt-4"):
        self.NL_policy = NL_policy
        self.model = model
        self.instructions = self._load_instructions("instruction_prompts/policy_instructions.txt")  
        self.llm_client = get_llm_client()

    def _load_instructions(self, file_path):
        """Load instructions from a separate file."""
        with open(file_path, "r") as file:
            return file.read()

    def generate_policy(self):
        """Generate a policy based on natural language input."""
        print("NL_policy: ", self.NL_policy)
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": self.NL_policy}
        ]

        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500
        )

        print("FULL response from gpt:\n ",response)
        response_content = response.choices[0].message.content.strip("```json").strip("```")
        print("\n\n\n\n response_content: ",response_content)
        full_response = json.loads(response_content)
        return full_response["policy"]

        # # Extract content, strip triple backticks and 'json' if present
        # content = response.choices[0].message.content
        # # Remove markdown JSON code block wrappers if present
        # if content.startswith("```json"):
        #     content = content[len("```json"):].strip()
        # if content.endswith("```"):
        #     content = content[:-3].strip()

        # print("\n\nParsed content:\n", content)
        # try:
        #     policy_json = json.loads(content)
        # except json.JSONDecodeError as e:
        #     print("Error decoding JSON from response:", e)
        #     raise

        # return policy_json
