from setuptools import setup, find_packages
# Read the contents of your README file
with open('README.md') as f:
    long_description = f.read()


setup(
    name='pathconf',
    version='1.0.9.7',  # Back to manual versioning
    packages=find_packages(),
    description='Uses os.walk to find and catalogue a given file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sam Kirby',
    author_email='sam.kirby@gagamuller.com',
    install_requires=[
        # Any dependencies you have, e.g., 'requests', 'numpy', etc.
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
)
