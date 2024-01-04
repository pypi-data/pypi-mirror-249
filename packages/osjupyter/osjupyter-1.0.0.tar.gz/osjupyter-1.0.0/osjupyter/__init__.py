# in your_extension_name/__init__.py

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'js/osjupyter',  # Path in the `your_extension_name` directory
        'dest': 'osjupyter',  # directory name that Jupyter will recognize
        # JS module to load. Ensure this matches your JS file's path
        'require': 'osjupyter/main'
    }]
