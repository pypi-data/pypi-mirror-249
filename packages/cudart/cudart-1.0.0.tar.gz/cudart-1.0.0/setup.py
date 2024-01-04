from setuptools import Extension, setup

ext = Extension(
    name='cudart',
    sources=['cudart.c'],
    define_macros=[
        ('Py_LIMITED_API', 0x030A0000),
    ],
    py_limited_api=True,
)

setup(
    name='cudart',
    version='1.0.0',
    ext_modules=[ext],
)
