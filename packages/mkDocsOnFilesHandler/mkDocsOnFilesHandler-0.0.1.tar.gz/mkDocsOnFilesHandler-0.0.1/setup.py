from setuptools import setup

setup(
    name='mkDocsOnFilesHandler',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    entry_points={
    'mkdocs.plugins': [
        'mkDocsOnFilesHandler = mkDocsOnFilesHandler.main.py: mkDocsOnFilesHandler',
    ]
}
)