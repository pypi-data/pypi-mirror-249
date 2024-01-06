from setuptools import setup, find_packages

setup(
    name='py-raytrace',
    version='0.4.3',
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),  # Updated package name to use underscores
    install_requires=[
        'numpy',
        'Pillow',
        'tqdm',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'ray=py_raytrace.py_raytrace:main',
            'raytrace=py_raytrace.py_raytrace:main',
            'py-raytrace=py_raytrace.py_raytrace:main',
        ],
    },
    author='Pranav A.',
    author_email='prnv.school@gmail.com',
    description='A simple ray tracing application',
    license='MIT'
)
