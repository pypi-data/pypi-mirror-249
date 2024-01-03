def typedInput(text: str, desiredType: type, defaultValue=None):
    assert desiredType in [ int, float, str, bool ], "Invalid type"
    assert type(text), "Invalid input"
    
    if defaultValue != None:
        assert type(defaultValue) == desiredType, "Invalid default value"
    
    while True:
        try:
            desiredInput = input(text)
            return desiredType(desiredInput) if desiredInput != "" else defaultValue
        except ValueError:
            continue