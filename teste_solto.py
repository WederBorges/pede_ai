try:
    try:
        int("abc")
    except ValueError as e:
        raise RuntimeError("deu ruim") from e
except RuntimeError as err:
    print(repr(err.__cause__))   # o ValueError original