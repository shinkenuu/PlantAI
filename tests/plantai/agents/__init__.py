from langchain_core.messages import BaseMessage, ToolMessage


def get_called_tool_names(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [
        tool_message.name
        for tool_message in messages
        if isinstance(tool_message, ToolMessage)
    ]
