from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Visualization tool designed to analyze and illustrate the Lorenz Energy Cycle for atmospheric science.'
LONG_DESCRIPTION = 'This tool offers a unique perspective for studying the intricate processes governing atmospheric energetics and instability mechanisms. It visualizes the transformation and exchange of energy within the atmosphere,specifically focusing on the interactions between kinetic and potential energy forms as conceptualized by Edward Lorenz.'

setup(
    name="lorenz_phase_space",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Danilo Couto de Souza",
    author_email="danilo.oceano@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
