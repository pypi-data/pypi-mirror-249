import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("anywidget_ipyniivue")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class NiivueWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    value = traitlets.Unicode("https://niivue.github.io/niivue-demo-images/mni152.nii.gz").tag(sync=True)
    color = traitlets.Unicode("gray").tag(sync=True)
