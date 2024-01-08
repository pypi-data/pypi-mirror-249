import sys
import typing
from . import object_quick_effects
from . import screen_play_rendered_anim
from . import constraint
from . import uvcalc_lightmap
from . import anim
from . import object
from . import sequencer
from . import file
from . import view3d
from . import presets
from . import uvcalc_follow_active
from . import add_mesh_torus
from . import wm
from . import userpref
from . import mesh
from . import clip
from . import spreadsheet
from . import geometry_nodes
from . import uvcalc_transform
from . import freestyle
from . import assets
from . import rigidbody
from . import node
from . import object_randomize_transform
from . import object_align
from . import console
from . import vertexpaint_dirt
from . import image
from . import bmesh

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
