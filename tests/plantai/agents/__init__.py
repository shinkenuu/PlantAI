import json

from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from deepeval.test_case import ToolCall


def _get_tool_call_functions(messages: list[BaseMessage]):
    for message in messages:
        if not isinstance(message, AIMessage) or not message.additional_kwargs.get(
            "tool_calls"
        ):
            continue

        for tool_call in message.additional_kwargs["tool_calls"]:
            yield tool_call["function"]


def get_called_tool_calls(messages: list[BaseMessage]) -> list[ToolCall]:
    message_tool_calls = list(_get_tool_call_functions(messages))
    pass

    tool_calls = [
        ToolCall(
            name=tool_call["name"],
            input_parameters=json.loads(tool_call["arguments"]),
        )
        for tool_call in message_tool_calls
    ]

    return tool_calls


def get_called_tools_contents(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [
        tool_message.content
        for tool_message in messages
        if isinstance(tool_message, ToolMessage)
    ]
