import json
from .record import Record

class Module():
    api_client = None
    key = None
    initialData = None
    def __init__(self, api_client, key, initialData):
        self.api_client = api_client
        self.key = key
        self.initialData = initialData

    def __str__(self):
        return str(self.initialData)

    def getFields(self, loginSession):
        url = self.api_client.api_prefix + '/meta/fields/' + self.key
        result = self.api_client.sendGetRequest(
            url=url,
            loginSession=loginSession,
            injectHeadersFn=None
        )
        if result.status_code != 200:
            self.api_client.raiseResponseException(result)
        resultDict = json.loads(result.text)
        if resultDict["data"]["type"] != "fields":
            raise Exception("Unexpected response")
        return resultDict["data"]["attributes"]

    def createRecord(self, loginSession, attributes):
        url = self.api_client.api_prefix + '/module'
        post_data = {
            "data": {
                "type": self.key,
                "attributes": attributes
            }
        }
        result = self.api_client.sendPostRequest(
            url=url,
            data=json.dumps(post_data),
            loginSession=loginSession,
            injectHeadersFn=None
        )
        if result.status_code != 201:
            self.api_client.raiseResponseException(result)
        resultDict = json.loads(result.text)
        return Record(api_client=self.api_client, parent_module=self, key=resultDict["data"]["type"], initialData=resultDict["data"])

    def getRecordById(self, loginSession, id):
        url = self.api_client.api_prefix + '/module/' + self.key + "/" + id
        result = self.api_client.sendGetRequest(
            url=url,
            loginSession=loginSession,
            injectHeadersFn=None
        )
        if result.status_code != 200:
            self.api_client.raiseResponseException(result)
        resultDict = json.loads(result.text)
        return Record(api_client=self.api_client, parent_module=self, key=resultDict["data"]["type"], initialData=resultDict["data"])
