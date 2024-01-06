import requests

class Tickets:
    def __init__(self, api):
        self._api = api

    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all tickets based on the provided parameters.
        Using endpoint: tickets
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters.
                        'updated_since': if provided, fetches tickets updated since the provided timestamp.
                        'per_page': defaults to 100 if not provided.
                        'page': if provided, fetches that specific page of tickets.
        
        Returns:
        list: Returns a list of all tickets based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get("tickets", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get("tickets", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
            
        return all_pages
    
    def list_all_deleted(self, **kwargs) -> list[dict]:
        """
        Lists all deleted tickets.
        Using endpoint: tickets?filter=deleted
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters.
                        'updated_since': if provided, fetches tickets updated since the provided timestamp.
                        'per_page': defaults to 100 if not provided.
                        'page': if provided, fetches that specific page of tickets.
        
        Returns:
        list: Returns a list of all deleted tickets.
        """
        
        kwargs["filter"] = "deleted"
        return self.list_all(**kwargs)
    
    def list_all_spam(self, **kwargs) -> list[dict]:
        """
        Lists all tickets marked as spam.
        Using endpoint: tickets?filter=spam
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters.
                        'updated_since': if provided, fetches tickets updated since the provided timestamp.
                        'per_page': defaults to 100 if not provided.
                        'page': if provided, fetches that specific page of tickets.
        
        Returns:
        list: Returns a list of all tickets marked as spam.
        """
        
        kwargs["filter"] = "spam"
        return self.list_all(**kwargs)

    def list_all_between_dates(self, updated_since: str, updated_until: str,
                                **kwargs) -> list[dict]:

        """
        Lists all tickets updated between the specified dates based on the provided parameters.
        
        Parameters:
        updated_since (str): The start datetime in the format 'YYYY-MM-DDTHH:MM:SS'.
        updated_until (str): The end datetime in the format 'YYYY-MM-DDTHH:MM:SS'.
        **kwargs: Used for additional query params.
        
        The following params will always be overwritten:
        'per_page': 100.
        'order_by': 'updated_at'.
        'order_type': 'asc'.
        'page': 1.
        
        Returns:
        list: Returns a list of all tickets updated between the specified dates based on the provided parameters.
        """
        kwargs.update({
            'per_page': 100,
            'updated_since': updated_since,
            'order_by': 'updated_at',
            'order_type': 'asc',
            'page': 1
            })
        
        all_pages = []
        while True:

            data = self._api._get("tickets", params=kwargs)
            data = [row for row in data if row['updated_at'] <= updated_until]
            
            all_pages.extend(data)
            if not data or len(data) < kwargs["per_page"]:
                break
            
            kwargs["page"] += 1
            
        return all_pages

class Groups:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all groups based on the provided parameters.
        Using endpoint: admin/groups
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of contacts.
        
        Returns:
        list: Returns a list of all groups based on the provided parameters.
        """
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get("admin/groups", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get("admin/groups", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
            
        return all_pages


class Agents:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all agents based on the provided parameters.
        Using endpoint: agents
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of contacts.
        
        Returns:
        list: Returns a list of all agents based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get("agents", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get("agents", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
            
        return all_pages
        

class Conversations:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, ticket_id: str, **kwargs) -> list[dict]:
        """
        Lists all conversations for a given ticket based on the provided parameters.
        Using endpoint: tickets/{ticket_id}/conversations
        
        Parameters:
        ticket_id (str): The ID of the ticket for which to list the conversations.
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of conversations.
        
        Returns:
        list: Returns a list of all conversations for the given ticket based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get(f"tickets/{ticket_id}/conversations", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get(f"tickets/{ticket_id}/conversations", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
        
        return all_pages


class Contacts:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all contacts based on the provided parameters.
        Using endpoint: contacts
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'updated_since': if provided, fetches contacts updated since the provided timestamp.
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of contacts.
        
        Returns:
        list: Returns a list of all contacts based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get(f"contacts", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get(f"contacts", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
        
        return all_pages


class SatisfactionRatings:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all satisfaction ratings based on the provided parameters.
        Using endpoint: surveys/satisfaction_ratings
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'created_since': if provided, fetches satisfaction ratings
                                        created since the provided timestamp.
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of satisfaction ratings.
        
        Returns:
        list: Returns a list of all satisfaction ratings based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get(f"surveys/satisfaction_ratings", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get(f"surveys/satisfaction_ratings", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
        
        return all_pages

class Surveys:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all surveys based on the provided parameters.
        Using endpoint: surveys
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'created_since': if provided, fetches surveys created
                                        since the provided timestamp.
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of surveys.
        
        Returns:
        list: Returns a list of all surveys based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get(f"surveys", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get(f"surveys", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
        
        return all_pages
    
class Products:
    def __init__(self, api):
        self._api = api
    
    def list_all(self, **kwargs) -> list[dict]:
        """
        Lists all surveys based on the provided parameters.
        Using endpoint: Products
        
        Parameters:
        **kwargs (dict): Variable length argument list containing query parameters. 
                        'per_page': defaults to 100 if not provided. 
                        'page': if provided, fetches that specific page of products.
        
        Returns:
        list: Returns a list of all products based on the provided parameters.
        """
        
        if "per_page" not in kwargs:
            kwargs["per_page"] = 100
        
        if "page" in kwargs:
            return self._api._get(f"products", params=kwargs)
        
        all_pages = []
        while True:
            kwargs["page"] = kwargs.get("page", 0) + 1

            data = self._api._get(f"products", params=kwargs)
            all_pages.extend(data)
            
            if not data or len(data) < kwargs["per_page"]:
                break
        
        return all_pages
    

class API:
    """
    A class used to represent the Freshdesk API.
    
    Documentation and available **kwargs to be found at:
    https://developers.freshdesk.com/api/
    ...

    Attributes
    ----------
    tickets : Tickets
        a reference to the Tickets API
    groups : Groups
        a reference to the Groups API
    agents : Agents
        a reference to the Agents API
    conversations : Conversations
        a reference to the Conversations API
    contacts : Contacts
        a reference to the Contacts API
    satisfaction_ratings : SatisfactionRatings
        a reference to the SatisfactionRatings API
    surveys : Surveys
        a reference to the Surveys API
    products : Products
        a reference to the Products API

    """
    def __init__(self, domain, api_key):
        
        self._api_url = f"https://{domain}.freshdesk.com/api/v2/"
        self._session = requests.Session()
        self._session.auth = (api_key, "X")
        self._session.headers = {"Content-Type": "application/json"}
        
        self.tickets = Tickets(self)
        self.groups = Groups(self)
        self.agents = Agents(self)
        self.conversations = Conversations(self)
        self.contacts = Contacts(self)
        self.satisfaction_ratings = SatisfactionRatings(self)
        self.surveys = Surveys(self)
        self.products = Products(self)

    def _validate_response(self, response: requests.Response):
        try:
            data = response.json()
        except ValueError:
            data = {}
        
        error_message = f'Request failed with status {response.status_code}'
        if 'errors' in data:
            error_message = data["errors"]
        elif 'message' in data:
            error_message = data["message"]
        
        if response.status_code == 429:
            raise Exception(f'Rate limit exceeded for another {response.headers.get("Retry-After")} secconds.')
        
        if 400 <= response.status_code < 500:
            raise Exception(error_message)
        
        elif 500 <= response.status_code < 600:
            raise Exception(f'Server error {response.status_code}')

        return data
    
    def _get(self, endpoint, params={}):
        response = self._session.get(f"{self._api_url}/{endpoint}", params=params)
        return self._validate_response(response)
