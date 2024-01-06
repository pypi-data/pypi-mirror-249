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
from freshdeskclient import API
```

### Initialize the API
To initialize the API, you need your Freshdesk domain and API key:

```
api = API(domain='your_domain', api_key='your_api_key')
```

### List all tickets
To list all tickets, you can use the list_all method of the Tickets API:

```python
tickets = api.tickets.list_all()
```
You can also list all tickets updated between two dates, you can use the list_all_between_dates method of the Tickets API:

```python
tickets = api.tickets.list_all()
```


### List all conversations for a ticket
To list all conversations for a ticket, you also need the ticket ID:

```
conversations = api.conversations.list_all(ticket_id='your_ticket_id')
```

### Example usage of params
You can use kwargs to pass query parameters to the freshdesk API.
For example:
```python
tickets = api.tickets.list_all(updated_since = '2000-01-01T00:00:00Z')
```

Please refer to the [Freshdesk API documentation](https://developers.freshdesk.com/api/)
for more details on the available endpoints and their parameters.