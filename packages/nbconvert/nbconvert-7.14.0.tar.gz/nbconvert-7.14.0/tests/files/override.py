c = get_config()  # type:ignore  # noqa

# Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ["notebook2.ipynb"]
c.NbConvertApp.export_format = "python"
