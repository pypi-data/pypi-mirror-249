from setuptools import setup

setup(
    name='osjupyter',
    version='1.0.0',
    description='Connects your Jupyter Notebook to Osyris Research Assistant',
    author='Osyris Technology',
    author_email='founders@osyris.io',
    packages=['osjupyter'],
    include_package_data=True,
    install_requires=[
        'notebook',  # Ensure the user has Jupyter Notebook
    ],
    package_data={
        # Include your JS files
        'osjupyter': ['js/osjupyter/*.js', 'js/osjupyter/*.svg', 'js/osjupyter/*.css'],
    },
    zip_safe=False
)
