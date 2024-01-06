from setuptools import setup

setup(
    name='py-raytrace',
    version='0.1.0',
    packages=['py-raytrace'],
    install_requires=[
        'numpy',
        'Pillow',
        'tqdm',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'ray=py_raytrace.raytrace:main',
        ],
    },
    author='Pranav A.',
    author_email='pranavnasrani@gmail.com',
    description='A simple ray tracing application',
    license='MIT',
)

