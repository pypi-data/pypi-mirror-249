# setup.py
from setuptools import setup, find_packages

setup(
    name="adix",
    version="0.0.1a1",
    author='imooger',
    description='Automatic data analysis tool',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        # List any dependencies here
        'pandas>=2.1.0',
        'numpy>=1.26.2',
        'matplotlib>=3.8.2',
        'seaborn>=0.13.0',
        'scipy>=1.11.4',
        'Jinja2>=3.1.2',
        'notebook>=7.0.6',
        'wordcloud>=1.8.1',
    ],
    python_requires='>=3.10',
)
