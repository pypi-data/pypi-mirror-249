import supabase
import sys


async def load_pyodide_modules():
    import micropip

    # ModuleNotFoundError: The module 'ssl' is unvendored from the Python standard library in the Pyodide distribution.
    # See https://pyodide.org/en/stable/usage/loading-packages.html for more details.
    await micropip.install("ssl")


if sys.platform == "emscripten":
    load_pyodide_modules()

__version__ = "0.1.4"


def Client():
    # TODO dont hard code this
    supabase_url: str = "https://api.humata.ai"
    supabase_anon_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlbnpmb2RxdWF0amNheHFoYm1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzI0Mzg4MDYsImV4cCI6MTk4ODAxNDgwNn0.5YmrDS0ie09qbFdRBZpX9ygXQSi82F5g25tRk57OKT4"
    return supabase.create_client(supabase_url, supabase_anon_key)
