


from setuptools import setup, find_packages


setup(
    name='Librflxlang',
    version='0.16.1.dev11+g1ee14612f.d20240103',
    packages=['librflxlang'],
    package_data={
        'librflxlang':
            ['*.{}'.format(ext) for ext in ('dll', 'so', 'so.*', 'dylib')]
            + ["py.typed"],
    },
    zip_safe=False,
)
