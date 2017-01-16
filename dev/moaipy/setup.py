from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

lib_nojit = [
    'lib/nojit/libmoai-osx-3rdparty-core.a',
    'lib/nojit/libmoai-osx-3rdparty-crypto.a',
    'lib/nojit/libmoai-osx-3rdparty-sdl.a',
    'lib/nojit/libmoai-osx-apple.a',
    'lib/nojit/libmoai-osx-audio-sampler.a',
    'lib/nojit/libmoai-osx-box2d.a',
    'lib/nojit/libmoai-osx-crypto.a',
    'lib/nojit/libmoai-osx-ct-util.a',
    'lib/nojit/libmoai-osx-fmod-studio.a',
    'lib/nojit/libmoai-osx-http-client.a',
    'lib/nojit/libmoai-osx-http-server.a',
    'lib/nojit/libmoai-osx-image-jpg.a',
    'lib/nojit/libmoai-osx-image-png.a',
    'lib/nojit/libmoai-osx-image-pvr.a',
    'lib/nojit/libmoai-osx-image-webp.a',
    'lib/nojit/libmoai-osx-luaext.a',
    'lib/nojit/libmoai-osx-sdl.a',
    'lib/nojit/libmoai-osx-sim.a',
    'lib/nojit/libmoai-osx-spine-v3.a',
    'lib/nojit/libmoai-osx-untz.a',
    'lib/nojit/libmoai-osx-zl-core.a',
    'lib/nojit/libmoai-osx-zl-crypto.a',
    'lib/nojit/libmoai-osx-zl-vfs.a',
    'lib/nojit/libmoai-osx.a',
    'lib/libfmod.dylib'
]

import os
import os.path

moai_root = os.environ["MOAI_ROOT"]
cdir = os.path.dirname(os.path.realpath( __file__ ))
extensions_path = os.path.abspath(os.path.join(cdir, "../../extensions"))


extensions_src = []

for f in os.listdir(extensions_path):
    filename = os.path.join(extensions_path, f)
    ext = os.path.splitext(f)[1][1:]
    if os.path.isfile(filename) and ext == 'cpp':
        extensions_src.append( filename )
        print("Added extension file: %s" % filename)

# extensions_src = [ os.path.join(extensions_path,"ParticlePresets.cpp") ]
extensions_includes = [ extensions_path ]

sources = ["moaipy.pyx", "lock.pxi"]

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("moaipy", sources + extensions_src, 
            language="c++",
            extra_objects=lib_nojit,
            
            extra_link_args=[
            '-framework', 'OpenGL',
            '-framework', 'GLUT',
            '-framework', 'CoreServices',
            '-framework', 'ApplicationServices',
            '-framework', 'AudioToolbox',
            '-framework', 'AudioUnit',
            '-framework', 'CoreAudio',
            '-framework', 'CoreGraphics',
            '-framework', 'CoreLocation',
            '-framework', 'Foundation',
            '-framework', 'GameKit',
            '-framework', 'QuartzCore',
            '-framework', 'StoreKit',
            '-framework', 'SystemConfiguration',
            ],

            include_dirs=[
            os.path.join(moai_root, 'src'),
            os.path.join(moai_root, '3rdparty/lua-5.1.3/src'),
            extensions_path,
            ])
    ]
)