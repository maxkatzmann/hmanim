from setuptools import setup, find_packages

setup(
    name='hmanim',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'colour',
        'manim',
        'networkx',
        'numpy',
    ],
    python_requires='>=3.12',
    author='Maximilian Katzmann',
    author_email='max.katzmann@gmail.com',
    description='The hyperbolic extension of manim!',
    long_description=open('README.md').read(),
    url='https://github.com/maxkatzmann/hmanim',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
    ],
)
