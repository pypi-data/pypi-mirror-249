

def get_version() -> str:
    import importlib.metadata
    return importlib.metadata.version('foxlator_lib')


__all__ = [
    'get_version'
]
