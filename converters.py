def list_converter(value: str) -> list[str]:
    value = value.strip()

    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError()
    
    return [
        item.strip() 
        for item 
        in value.removeprefix("[").removesuffix("]").split(",")
    ]