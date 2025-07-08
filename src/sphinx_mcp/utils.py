def check_server_filter_for_artefacts(arguments: list, artefacts: dict) -> bool:
    """
    Check if the provided server name exists in the artefacts dictionary.
    """
    if len(arguments) == 1 and arguments[0] not in artefacts:
        raise RuntimeError(
            f"No MCP server specification exists by the name '{arguments[0]}'."
        )
