from setuptools import setup, find_packages

setup(
    name='py-raytrace',
    version='0.5.1',
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
    package_data={
        'py_raytrace': [
            'objects.json'
        ],  # Assuming 'objects.json' is in the same directory as 'py-raytrace' module
    },
    author='Pranav A.',
    author_email='prnv.school@gmail.com',
    description='A simple ray tracing application',
    license='MIT'
)
