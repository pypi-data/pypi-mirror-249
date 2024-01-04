# nn-freshdesk-client

This is the Python SDK for the Freshdesk API. It allows you to interact with the Freshdesk API using Python.

## Installation

You can install the package from PyPi using pip:

```bash
pip install nn-freshdesk-client
```

## Usage
After installation, you can import the package in your Python scripts as follows:
```python
import freshdeskclient
```

### Generate token
To generate a token to be used for authentication you can do this with this snippet:

```python
from bitlogclient import Token

token = Token(
    domain='your_domain',
    basic_auth_user= 'your_auth_user',
    basic_auth_password= 'your_auth_password',
    username='your_username', password='your_password).get_token()
```

### List available dataviews
To list all available dataviews you can use this snippet:

```python
from bitlogclient import Report

views = Report(
    token='your_token,
    domain='your_domain').list_views()
```

### Get dataview
To get data from a dataview without parameters you can use this snippet:

```python
from bitlogclient import Report

data = Report(
    token='your_token,
    domain='your_domain').get_view('your_view_name')
```

### Get dataview with parameters
To get data from a dataview with parameters you can use this snippet:

```python
from bitlogclient import Report, ReportParams

data = Report(
    token='your_token,
    domain='your_domain').get_view_with_params(
        'your_view_name',
        [
            ReportParams('from_date', 'date', '2023-01-01'),
            ReportParams('to_date', 'date', '2023-01-01'),
        ])
```
