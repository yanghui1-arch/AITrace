from setuptools import setup, find_packages

setup(
    name='at',
    version='0.1.0.beta',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "click>=8.3.0",
        "openai>=1.108.2",
    ],
    entry_points={
        "console_scripts": [
            "aitrace=at.cli:cli",
        ],
    },
    python_requires=">=3.12",
    include_package_data=True,
    description="AItrace CLI tool",
    author="yanghui",
    url='https://github.com/yanghui1-arch/AT'
)