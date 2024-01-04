from setuptools import setup, find_packages

setup(
    name='xytext',
    version='1.0.6',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Xytext',
    author_email='hello@xytext.com',
    description='API Wrapper for Xytext - LLM Interfaces for Production.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/xytext-ai/xytext',
    long_description_content_type='text/markdown',
    long_description="""# xytext

xytext is a Python client library for interacting with the Xytext API. It offers a simple way to send requests to the Xytext API and handle responses effectively. This package is designed to integrate Xytext API functionalities into Python applications.

Installation

Install xytext using pip:
```
pip install xytext
```

## Usage
To use xytext, you must have your Xytext API credentials: FUNC_ID, STAGE, and AUTH_TOKEN. These credentials are necessary to authenticate your requests.

## Example
```
from xytext import Xytext, XytextResponse

def example_usage():
    func_id = "your_func_id"
    stage = "your_stage"
    auth_token = "your_auth_token"

    xt = Xytext(func_id, stage, auth_token, timeout=900)
    try:
        response = xt.invoke("Your input text here")
        print(response.result)
    except Exception as e:
        print("Error:", str(e))

example_usage()
```


## API Reference

### Xytext
This is the primary class used to interact with the Xytext API.

#### Constructor
**Xytext(func_id, stage, auth_token, timeout=900)**

Parameters:

`func_id (String)` The function ID for the Xytext API.

`stage (String)` The stage of the API environment ("staging", "prod").

`auth_token (String)` Your authorization token for the Xytext API.

`timeout (Integer)` The timeout for the API request in seconds. Default is 900 seconds (15 minutes).


#### Methods

**invoke(input_text) Sends a request to the Xytext API.**


Parameters:

`input_text (String)` The text input for the API.

Returns: An instance of `XytextResponse`.

### XytextResponse
This class represents the response received from the Xytext API.

Properties
`raw_response` The complete response from the API as a Python dictionary.

`success` Boolean indicating if the API request was successful.

`message` A message from the API, typically containing error details if any.

`usage` Details about the usage of the API for this call.

`call_id` A unique identifier for the API call.

`result` The content returned by the API, either as a Python object or a string.


## Additional Information

Keep your API credentials secure. Avoid exposing them in client-side code. Utilize environment variables to safeguard your auth token.
Properly handle API responses and exceptions in your application to ensure robustness.

"""
)
