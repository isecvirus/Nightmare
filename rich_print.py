from rich.console import Console


def rprint(data, highlight:bool=True, **kwargs):
    Console().print(data, **kwargs, highlight=highlight)