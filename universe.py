from llms.gpt import generate_text


def next_state(action_result: str):
    system_prompt = f"""You are responsable for simulating how agent's actions affect the world.
Be fair, let some chaos happen rarely and make sure its fulfilling sometimes"""

    user_prompt = action_result

    prompt = f"""### System: {system_prompt}

### User: {user_prompt}

### Assistant: """

    assistant = generate_text(prompt)
    return assistant
