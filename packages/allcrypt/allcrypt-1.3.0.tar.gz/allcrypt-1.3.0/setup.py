from setuptools import setup, find_packages

setup(
    name='allcrypt',
    version='1.3.0',  # Update with your version number
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'allcrypt = allcrypt.main:main',
        ],
    },
)
