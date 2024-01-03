"""Entrypoint for the sketching library.

Entrypoint for the sketching library which includes the logic for the auto-renderer selection for
Sketch2D.

License:
    BSD
"""

import os
import typing

import sketching.abstracted

NOT_FOUND_MSG = 'Could not load a sketch backend. See https://sketchingpy.org/guides/start.html.'

has_app = False
has_static = False
has_web = False
in_notebook = False

app_exception = None
static_exception = None
web_exception = None


try:
    from sketching.sketch2dapp import Sketch2DApp
    has_app = True
except ModuleNotFoundError as e:
    app_exception = e


try:
    from sketching.sketch2dstatic import Sketch2DStatic
    has_static = True
except ModuleNotFoundError as e:
    static_exception = e


try:
    from sketching.sketch2dweb import Sketch2DWeb
    has_web = True
except ModuleNotFoundError as e:
    web_exception = e


try:
    in_notebook = "JPY_PARENT_PID" in os.environ
except:
    pass


Sketch2D: typing.Type[sketching.abstracted.Sketch] = sketching.abstracted.Sketch

if in_notebook:
    Sketch2D = Sketch2DStatic
elif has_app:
    Sketch2D = Sketch2DApp
elif has_static:
    Sketch2D = Sketch2DStatic
elif has_web:
    Sketch2D = Sketch2DWeb
else:
    print('Failed to load runtime. Debugging:')
    print('App: ' + str(app_exception))
    print('Static: ' + str(static_exception))
    print('Web: ' + str(web_exception))
    raise RuntimeError(NOT_FOUND_MSG)
