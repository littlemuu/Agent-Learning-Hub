import json


def add(a: int, b: int) -> int:
    return a + b

def multiply(a:int,b:int)->int:
    return a*b


tools = {
    "add": add,
    "multiply":multiply,
}


def fake_model(messages: list[dict]) -> str:
    """Return a fake structured model response for learning the agent loop."""
    last_message = messages[-1]

    if last_message["role"] == "tool":
        return json.dumps(
            {
                "type": "final_answer",
                "answer": f"Final answer: {last_message['content']}",
            }
        )

    user_input = last_message["content"]

    if "10" in user_input and "20" in user_input:
        return json.dumps(
            {
                "type": "tool_call",
                "action": "add",
                "arguments": {
                    "a": 10,
                    "b": 20,
                },
            }
        )
    
    if "6" in user_input and "7" in user_input:
        return json.dumps(
            {
                "type":"tool_call",
                "action": "multiply",
                "arguments":{
                    "a":6,
                    "b":7,
                },
            }
        )

    return json.dumps(
        {
            "type": "final_answer",
            "answer": "I do not know which tool to call.",
        }
    )


def agent_loop(user_input: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "user", "content": user_input},
    ]

    for _step in range(max_steps):
        model_output = fake_model(messages)

        try:
            data = json.loads(model_output)
        except json.JSONDecodeError:
            return "Error: model output is not valid JSON."

        output_type = data.get("type")

        if output_type == "final_answer":
            return data.get("answer", "")

        if output_type != "tool_call":
            return f"Error: unknown output type: {output_type}"

        action = data.get("action")
        arguments = data.get("arguments", {})

        if action not in tools:
            return f"Error: unknown tool: {action}"

        if not isinstance(arguments, dict):
            return "Error: arguments must be an object."

        if action == "add":
            if "a" not in arguments or "b" not in arguments:
                return "Error: add requires arguments a and b."
            if not isinstance(arguments["a"], int) or not isinstance(arguments["b"], int):
                return "Error: add arguments a and b must be integers."
            
        if action == "multiply":
            if "a" not in arguments or "b" not in arguments:
                return "Error: multiply requires arguments a and b."
            if not isinstance(arguments["a"], int) or not isinstance(arguments["b"], int):
                return "Error: multiply arguments a and b must be integers."

        tool_func = tools[action]

        try:
            tool_result = tool_func(**arguments)
        except Exception as exc:
            return f"Error: tool execution failed: {exc}"

        messages.append(
            {
                "role": "tool",
                "name": action,
                "content": str(tool_result),
            }
        )

    return "Error: reached max steps."


if __name__ == "__main__":
    answer = agent_loop("What is 10 plus 20?")
    print(answer)
    result=agent_loop("what is 6 times 7")
    print(result)
