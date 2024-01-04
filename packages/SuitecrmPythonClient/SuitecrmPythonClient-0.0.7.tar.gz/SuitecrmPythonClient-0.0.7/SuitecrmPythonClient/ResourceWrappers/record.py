

class Record():
    api_client = None
    parent_module = None
    key = None
    initialData = None
    def __init__(self, api_client, parent_module, key, initialData):
        self.api_client = api_client
        self.parent_module = parent_module
        self.key = key
        self.initialData = initialData

    def __str__(self):
        return str(self.initialData)

    def getId(self):
        return self.getInitialData()["id"]

    def getInitialData(self):
        return self.initialData
