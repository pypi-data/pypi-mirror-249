import requests


class PxApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_navigation(self):
        """Retrieve the top level navigation."""
        url = f"{self.base_url}/navigation"
        response = requests.get(url)
        return response.json()

    def get_navigation_id(self, id):
        """Retrieve navigation details for a specific ID."""
        url = f"{self.base_url}/navigation/{id}"
        response = requests.get(url)
        return response.json()

    def get_tables(self):
        """Retrieve a list of tables."""
        url = f"{self.base_url}/tables"
        response = requests.get(url)
        return response.json()

    def get_table_by_id(self, id):
        """Retrieve a specific table by ID."""
        url = f"{self.base_url}/tables/{id}"
        response = requests.get(url)
        return response.json()

    def get_table_metadata(self, id):
        """Retrieve metadata for a specific table."""
        url = f"{self.base_url}/tables/{id}/metadata"
        response = requests.get(url)
        return response.json()

    def get_codelist(self, id):
        """Retrieve a specific codelist by ID."""
        url = f"{self.base_url}/codelists/{id}"
        response = requests.get(url)
        return response.json()

    def get_table_data(self, id):
        """Retrieve data for a specific table."""
        url = f"{self.base_url}/tables/{id}/data"
        response = requests.get(url)
        return response.json()

    def get_config(self):
        """Retrieve API configuration."""
        url = f"{self.base_url}/config"
        response = requests.get(url)
        return response.json()


# # Example usage
# api = PxApi("https://api.example.com")
# navigation = api.get_navigation()
