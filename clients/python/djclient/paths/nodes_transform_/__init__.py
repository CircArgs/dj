# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from djclient.paths.nodes_transform_ import Api

from djclient.paths import PathValues

path = PathValues.NODES_TRANSFORM_