from setuptools import Extension, setup

main_ext = Extension(
    name='pylammpstrj',
    include_dirs=['pylammpstrj/include/'],
    sources=[
        'pylammpstrj/lammpstrj/atom.c',
        'pylammpstrj/lammpstrj/average.c',
        'pylammpstrj/lammpstrj/box.c',
        'pylammpstrj/lammpstrj/read.c',
        'pylammpstrj/lammpstrj/select.c',
        'pylammpstrj/lammpstrj/skip.c',
        'pylammpstrj/lammpstrj/trajectory.c',
        'pylammpstrj/pylammpstrjmodule.c'
    ],
    extra_compile_args=[
        '-g',
        '-O3',
        '-Wall',
        '-Wextra'
    ]
)

setup(
    ext_modules=[
        main_ext
    ]
)
