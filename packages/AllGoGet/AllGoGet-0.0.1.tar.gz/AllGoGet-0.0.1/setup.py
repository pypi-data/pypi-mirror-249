from setuptools import setup, find_packages

setup(
    name="AllGoGet",
    version="0.0.1",
    packages=find_packages(),

    # Metadata
    author="João Flávio Andrade Silva",
    author_email="joaoflavio1988@gmail.com",
    description="The AllGo package is a powerful tool that provides a seamless integration between the advanced features of MetaTrader5 and the analytical flexibility of pandas. It allows users to easily access and manipulate financial data directly from MetaTrader5 for detailed analysis within the familiar environment of pandas.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/joao-1988/AllGoGet",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],

    # Optional
    install_requires=['IPython', 'MetaTrader5', 'pandas']
)