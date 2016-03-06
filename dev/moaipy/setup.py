from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

lib_jit = [
    'lib/jit/libbox2d.a',
    'lib/jit/libchipmunk.a',
    'lib/jit/libcontrib.a',
    'lib/jit/libcrypto.a',
    'lib/jit/libcurl.a',
    'lib/jit/libexpat.a',
    'lib/jit/libfreetype.a',
    'lib/jit/libglew.a',
    'lib/jit/libhost-modules.a',
    'lib/jit/libjansson.a',
    'lib/jit/libjpg.a',
    'lib/jit/libluacrypto.a',
    'lib/jit/libluacurl.a',
    'lib/jit/libluafilesystem.a',
    'lib/jit/libluajit.a',
    'lib/jit/libluasocket.a',
    'lib/jit/libluasql.a',
    'lib/jit/libmoai-box2d.a',
    'lib/jit/libmoai-chipmunk.a',
    'lib/jit/libmoai-core.a',
    'lib/jit/libmoai-http-client.a',
    'lib/jit/libmoai-fmod-studio.a',
    'lib/jit/libmoai-luaext.a',
    'lib/jit/libmoai-sim.a',
    'lib/jit/libmoai-untz.a',
    'lib/jit/libmoai-util.a',
    'lib/jit/libmongoose.a',
    'lib/jit/libogg.a',
    'lib/jit/libpng.a',
    'lib/jit/libSDL2.a',
    'lib/jit/libSDL2main.a',
    'lib/jit/libsfmt.a',
    'lib/jit/libsqlite3.a',
    'lib/jit/libssl.a',
    'lib/jit/libtinyxml.a',
    'lib/jit/libtlsf.a',
    'lib/jit/libuntz.a',
    'lib/jit/libvorbis.a',
    'lib/jit/libzlcore.a',
    'lib/jit/libzlib.a',
    'lib/jit/libzlvfs.a'
]

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
    'lib/nojit/libmoai-osx-spine.a',
    'lib/nojit/libmoai-osx-untz.a',
    'lib/nojit/libmoai-osx-zl-core.a',
    'lib/nojit/libmoai-osx-zl-crypto.a',
    'lib/nojit/libmoai-osx-zl-vfs.a',
    'lib/nojit/libmoai-osx.a',
    'lib/libfmod.dylib'
]


particle_presets_src = ["/Users/vavius/moai/projects/digit/cpp/ParticlePresets.cpp"]
particle_presets_includes = ["/Users/vavius/moai/projects/digit/cpp/"]

sources = ["moaipy.pyx", "lock.pxi"]

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("moaipy", sources + particle_presets_src, 
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
            # '/Users/vavius/moai/moai-new/3rdparty/LuaJIT-2.0.3/src/',
            '/Users/vavius/moai/moai-dev/src/',
            '/Users/vavius/moai/moai-dev/3rdparty/lua-5.1.3/src/',
            '/Users/vavius/moai/projects/digit/cpp/'
            ])
    ]
)