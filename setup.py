from distutils.core import setup

setup(
    name='got_fleas',
    veresion='0.1',
    packages=['got_fleas'],
    entry_points={
        'console_scripts': [
            'gotfleas = got_fleas.main:main',
        ],
    },
)
