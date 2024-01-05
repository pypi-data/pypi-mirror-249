import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

install_requires = [
   'aiohttp==3.7.4', 'typing-extensions~=3.10.0.0', 'iso8601', 'pytz', 'requests==2.24.0', 'httpx==0.23.0'
]

tests_require = [
      'pytest', 'pytest-mock', 'pytest-asyncio', 'asynctest', 'aiohttp', 'mock', 'freezegun==1.0.0', 'respx==0.19.2'
]

setuptools.setup(
    name="metaapi_cloud_risk_management_sdk",
    version="2.0.2",
    author="MetaApi DMCC",
    author_email="support@metaapi.cloud",
    description="Python SDK for MetaApi risk management API. Can execute trading risk restrictions, forex challenges "
                "and competitions in a cloud on both MetaTrader 5 (MT5) and MetaTrader 4 (MT4) (https://metaapi.cloud)",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords=['metaapi.cloud', 'MetaTrader', 'MetaTrader 5', 'MetaTrader 4', 'MetaTrader5', 'MetaTrader4', 'MT', 'MT4',
              'MT5', 'forex', 'equity tracking', 'risk management', 'API', 'REST', 'client', 'sdk', 'cloud', 'ftmo',
              'prop trading', 'proprietary trading'],
    url="https://github.com/metaapi/metaapi-risk-management-python-sdk",
    include_package_data=True,
    package_dir={'metaapi_cloud_risk_management_sdk': 'lib'},
    packages=['metaapi_cloud_risk_management_sdk'],
    install_requires=install_requires,
    tests_require=tests_require,
    license='SEE LICENSE IN LICENSE',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)