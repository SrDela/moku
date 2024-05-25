try:
    import pydantic

    PYDANTIC_AVAILABLE = pydantic.__version__.startswith("2.")
except ImportError:
    PYDANTIC_AVAILABLE = False
