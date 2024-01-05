import os

"""
MarcusLion Global variable
"""

api_key = os.getenv('MARCUSLION_API_KEY', "b7f88c9c-94ba-11ee-b9d1-0242ac120002")
base_url = os.getenv('MARCUSLION_API_HOST', "https://qa1.marcuslion.com")
api_version = "/core/api/v2"
