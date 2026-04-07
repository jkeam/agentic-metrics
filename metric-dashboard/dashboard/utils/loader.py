from flask import current_app
from importlib.util import spec_from_file_location, module_from_spec
from sys import modules
from pathlib import Path
import os

def call_dynamic_function(file_path, function_name, *args, **kwargs):
    # 1. Convert string path to a Path object and get the module name
    path = Path(file_path)
    module_name = path.stem

    # 2. Create a module spec and the module itself
    spec = spec_from_file_location(module_name, file_path)
    module = module_from_spec(spec)
    
    # 3. Add to sys.modules (optional but recommended for consistency)
    modules[module_name] = module
    
    # 4. Execute the module so the functions actually exist
    spec.loader.exec_module(module)

    # 5. Get the function and call it
    func = getattr(module, function_name)
    return func(*args, **kwargs)

def dynamically_load_charts(span, events):
    dynamic_charts = {}
    dynamic_chart_path = current_app.config["DYNAMIC_CHART_PATH"]
    if dynamic_chart_path:
        # nonrecursive
        for file in Path(dynamic_chart_path).glob('*.py'):
            try:
                filename = file.name
                pretty_filename = Path(filename).stem.replace("_", " ").title()
                dynamic_charts[pretty_filename] = call_dynamic_function(
                    os.path.join(dynamic_chart_path, filename),
                    "run",
                    span,
                    events
                )
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print(f"Error type: {type(e).__name__}")
    return dynamic_charts
