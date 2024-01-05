![alt text](https://i.imgur.com/jVdp3yy.png)

<div id="top"></div>

This repository holds the code for our Javascript/Typescript SDK.

## Commands

-   `poetry install` - Installs the dependencies
-   `poetry run pytest --tb=short --maxfail=100 -ra python_sdk_tests --api_key=YOUR_API_KEY_HERE -s` - Runs the tests (Need to have an API key. Run `create_sdk_test_account.py` in microservices-monorepo to get one.)

## Getting Started

### Installation

To install the SDK, `git clone` the repository and run `poetry install` in the root directory. This will install all the dependencies and build the SDK.

Alternatively, you can install the SDK directly from PyPi using `pip install pulsar-sdk-py`.

### Usage

To use the SDK, you need to import the `PulsarSDK` class from the `pulsar_sdk_py` package. You can then instantiate the class with your API key, and use the SDK to make requests to the API.

```python
from pulsar_sdk_py import PulsarSDK
from pulsar_sdk_py.enums import TokenType, ChainKeys

API_KEY = "API_KEY_HERE"
sdk = PulsarSDK(API_KEY)
token = sdk.tokens.get_token_info_by_address_and_chain(
    token_type=TokenType.ADDRESS, address="YOUR TOKEN ADDRESS", chain=ChainKeys.TERRA2
)
```

An example fetching wallet balances:

```python
import asyncio
from pulsar_sdk_py import PulsarSDK
from pulsar_sdk_py.enums import ChainKeys

API_KEY = "API_KEY_HERE"
sdk = PulsarSDK(API_KEY)


async def fetch_balances(wallet_address: str, chain: ChainKeys):
    responses_list = []
    async for wallet_balance in sdk.balances.get_wallet_balances(
            wallet_addr=wallet_address,
            chain=chain
    ):
        responses_list.append(wallet_balance)
    return responses_list


res = asyncio.get_event_loop().run_until_complete(
    fetch_balances("0x77984dc88aab3d9c843256d7aabdc82540c94f69", ChainKeys.ETHEREUM)
)
print(res)
```

It's important to notice that the SDK uses async generators to iterate through the responses. This means that you can use a `async for` loop to iterate through the responses. This is necessary because the SDK uses Websockets to fetch the data, and the responses are streamed in real time.

The above example will fetch you all the wallet balances for your wallet, provided the Chain is active in our environment.
For more information, check out our [documentation](http://pulsar.readme.io/).

## Pull Requests

In order to contribute, you need to create a new branch, make your changes and open a pull request. Before opening the pull request, run the tests to see if they pass locally. If you're adding a new feature, make sure to add tests for it. In order to run the tests, you will need to have a server instance running in your machine, and then pass an API key to the tests, like this: `poetry run pytest --tb=short --maxfail=100 -ra python_sdk_tests --api_key=YOUR_API_KEY_HERE -s`.

If the tests pass, you can open a pull request. This will then run the tests again, but on CircleCI connected to QA.

Make sure to update the `CHANGELOG.md` file with the changes you've made.

To publish this repository, save the PyPi credentials to Poetry:

1. Generate an API Token on PyPI:
    1. Log in to your PyPI account.
    2. Go to the API token section and create a new token (Account settings and scroll down).
    3. Copy the generated token; it will look like pypi-XXXXXXXXXXXXXXXX.
2. Store the Token with Poetry:
   Open your terminal.
   Run the following command:
    ```bash
    poetry config http-basic.pypi username __token__
    poetry config http-basic.pypi password your-api-token
    ```
    Replace your-api-token with the token you copied from PyPI.

## Publishing

### Running the Publish Script

After this, run `poetry run python publish_sdk.py --dry-run` to ensure everything builds correctly and the generated `.tar.gz` file has all the correct files (also check that the README file is not this one). If everything looks correct, run the same command without the dry run flag, and it will publish the package to PyPi.

### Incrementing Version

-   **Patch**: For backward-compatible bug fixes.
    ```bash
    poetry version patch
    ```
-   **Minor**: For backward-compatible new features.
    ```bash
    poetry version minor
    ```
-   **Major**: For changes that break backward compatibility.
    ```bash
    poetry version major
    ```

### Setting a Specific Version

You can also set the version directly:

```bash
poetry version 1.2.3
```

Replace `1.2.3` with your desired version number.

## Changelog

### 0.1.42

-   Initial release.
