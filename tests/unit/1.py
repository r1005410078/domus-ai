from openai import OpenAI
import json
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

# Convert Pydantic model to JSON Schema
client = OpenAI(base_url='https://api.openai-proxy.org/v1', api_key=lambda: "sk-mH6M90p4io1JreghOnvnQ5Cq6PqegWW5IxIf9rUnzShoiBI5")

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"],
    "additionalProperties": False
}

# Call the API with structured output
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "张三，28岁"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Person",
            "schema": schema,
            "strict": True  # Enforce strict validation
        }
    }
)

# Parse the result
result_text = response.choices[0].message.content
# result_dict = json.loads(result_text)
# person = Person(**result_dict)
# print(person)  # Person(name='张三', age=28)