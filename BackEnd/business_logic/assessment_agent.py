import json
import os
from string import Template
from core.init_llm import get_llm_client

class AssessmentAgent:
    def __init__(self, tools):
        """
        Initializes OpenAI Agent with function-callable tools.
        The `tools` parameter should be a dictionary of {function_name: function_reference}.
        """
        self.client = get_llm_client()

        self.tools = tools
        self.tool_schemas, self.tool_schema_dict = self._generate_tool_schemas()

        self.instructions = self._load_instructions("instruction_prompts/assessment_instructions.txt")
        print("initialized agent")

    def _load_instructions(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Instruction file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


    def _generate_tool_schemas(self):
        """Generate both a list (for OpenAI) and a dictionary (for lookup)"""
        tool_list = []
        tool_dict = {}

        for name, func in self.tools.items():
            # Ensure func has a schema attribute as JSON string
            if not hasattr(func, "schema"):
                raise AttributeError(f"Tool function '{name}' missing 'schema' attribute")

            try:
                parameters = json.loads(func.schema)
            except Exception as e:
                raise ValueError(f"Error parsing JSON schema for tool '{name}': {e}")

            tool_schema = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__,
                    "parameters": parameters
                }
            }
            tool_list.append(tool_schema)
            tool_dict[name] = tool_schema["function"]

        # print("_generate_tool_schemas tool_list:", tool_list)
        return tool_list, tool_dict

    def analyze_image(self, image_path, policy_text):
        """
        Uses OpenAI GPT-4 with function calling to dynamically decide when to use tools.
        Passes reference images dynamically when needed.
        """
        cleaned_instructions = self.instructions.replace("{ policy_text }", "${policy_text}")

        # Fill in the system prompt template
        system_prompt = Template(cleaned_instructions).safe_substitute(policy_text=policy_text)

        # Build messages list for OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Analyze this image and ensure it complies with the policy."},
            {"role": "user", "content": f"Image to check: {image_path}."},
        ]

        i = 0
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0

        while True:
            i += 1
            print("inside while loop #", i)

            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                tools=self.tool_schemas,
                tool_choice="auto",
                temperature=0.5
            )

            usage = response.usage
            print("Prompt tokens:", usage.prompt_tokens)
            print("Completion tokens:", usage.completion_tokens)
            print("Total tokens:", usage.total_tokens)
            total_prompt_tokens += usage.prompt_tokens
            total_completion_tokens += usage.completion_tokens
            total_tokens += usage.total_tokens


            response_message = response.choices[0].message  # Extract message

            if response_message.tool_calls:
                tool_outputs = []

                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except Exception as e:
                        arguments = {}
                        print(f"Warning: Failed to parse tool call arguments for {function_name}: {e}")

                    tool_call_id = tool_call.id
                    function_schema = self.tool_schema_dict.get(function_name)

                    if not function_schema:
                        tool_output = {"error": f"Schema not found for function: {function_name}"}
                    else:
                        required_params = function_schema.get("parameters", {}).get("required", [])
                        missing_params = [param for param in required_params if param not in arguments]

                        if missing_params:
                            tool_output = {"error": f"Missing required parameters: {missing_params}"}
                        elif function_name in self.tools:
                            try:
                                tool_output = self.tools[function_name](**arguments)
                            except Exception as e:
                                tool_output = {"error": f"Exception during tool execution: {e}"}
                        else:
                            tool_output = {"error": f"Tool {function_name} not found."}

                    if hasattr(tool_output, "dict"):
                        content_json = json.dumps(tool_output.dict())
                    else:
                        content_json = json.dumps(tool_output)

                    tool_outputs.append({
                        "role": "tool",
                        "name": function_name,
                        "tool_call_id": tool_call_id,
                        "content": content_json
                    })

                # Append the assistant message (with tool calls) and the tool responses
                messages.append(response_message)
                messages.extend(tool_outputs)

            else:
                # No more tool calls, the model has decided the breach
                content = response_message.content.strip()
                print("Final model content:", repr(content))  # Debug print

                print("==== FINAL TOKEN USAGE ====")
                print(f"Total prompt tokens:     {total_prompt_tokens}")
                print(f"Total completion tokens: {total_completion_tokens}")
                print(f"Total tokens overall:    {total_tokens}")
                print("============================")


                if not content:
                    print("Empty content returned from model")
                    return {"error": "Empty content from model"}

                try:
                    final_json = json.loads(content)
                    return final_json
                except Exception as e:
                    print(f"Failed to parse final JSON: {e}")
                    return {"error": "Invalid JSON from model", "raw_response": content}
