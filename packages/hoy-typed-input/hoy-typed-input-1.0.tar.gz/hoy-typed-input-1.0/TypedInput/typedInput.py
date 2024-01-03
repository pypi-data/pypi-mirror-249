def typedInput(text: str, desiredType: type):
    assert desiredType in [ int, float, str, bool ], "Invalid type"
    assert type(text), "Invalid input"
    
    while True:
        try:
            return desiredType(input(text))
        except ValueError:
            continue
