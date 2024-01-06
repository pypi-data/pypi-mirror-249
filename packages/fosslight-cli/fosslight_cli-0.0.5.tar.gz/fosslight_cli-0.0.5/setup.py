# setup.py
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()


if __name__ == '__main__':
    setup(
        name='fosslight_cli',
        version='0.0.5',
        packages=find_packages(),
        install_requires=required,
        python_requires=">=3.8",
        entry_points={
            'console_scripts': [
                "fosslight-cli = src.__main__:main",
            ]
        },
        license='Apache-2.0',
        url='https://github.com/fosslight/fosslight_cli',
        download_url='https://github.com/fosslight/fosslight_cli',
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    )
