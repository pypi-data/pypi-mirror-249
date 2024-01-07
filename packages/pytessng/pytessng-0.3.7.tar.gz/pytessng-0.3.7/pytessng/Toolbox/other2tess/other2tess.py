from .opendrive2tess import opendrive2tess
from .shape2tess import shape2tess
from .osm2tess import osm2tess
from .excel2tess import excel2tess


def other2tess(netiface, params, mode):
    if mode == "opendrive":
        opendrive2tess.opendrive2tess(netiface, params)
    elif mode == "shape":
        shape2tess.shape2tess(netiface, params)
    elif mode == "osm":
        osm2tess.osm2tess(netiface, params)
    elif mode == "excel":
        excel2tess.excel2tess(netiface, params)
    else:
        raise Exception("No this import mode!")
