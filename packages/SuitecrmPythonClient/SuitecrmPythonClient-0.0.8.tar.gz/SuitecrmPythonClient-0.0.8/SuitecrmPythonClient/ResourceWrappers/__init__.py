
from .module import Module

def moduleFactory(api_client, key, moduleData):
    return Module(api_client, key, moduleData)
