from langchain_core.messages import BaseMessage, ToolMessage


def get_called_tools_names(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [
        tool_message.name
        for tool_message in messages
        if isinstance(tool_message, ToolMessage)
    ]


def get_called_tools_contents(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [
        tool_message.content
        for tool_message in messages
        if isinstance(tool_message, ToolMessage)
    ]
