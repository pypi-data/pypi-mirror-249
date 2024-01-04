from PythonAPIClientBase import LoginSession
import requests
import json

access_api = "/legacy/Api/access_token"

class SuitecrmLoginSessionBasedOnClientIdAndSecret(LoginSession):
  APIClient = None
  clientId = None
  clientSecret = None
  authResponse = None
  def __init__(self, APIClient, clientId, clientSecret):
    self.APIClient = APIClient
    self.clientId = clientId
    self.clientSecret = clientSecret
    self.authResponse = None

    self._getNewAuthToken()
    if self.authResponse is None:
      raise Exception("Failed to establish login session using APIKey")

  def _getNewAuthToken(self, fromRefresh=False):
    self.currentAuthKey = None

    def injectHeaderFN(headers):
      headers["Content-type"] = "application/vnd.api+json"
      headers["Accept"] = "application/vnd.api+json"

    body = {
      "grant_type": "client_credentials",
      "client_id": self.clientId,
      "client_secret": self.clientSecret
    }

    result = self.APIClient.sendRequest(
      reqFn=requests.post,
      origin=None,
      url=access_api,
      data=json.dumps(body),
      loginSession=None,
      injectHeadersFn=injectHeaderFN,
      skipLockCheck=fromRefresh
    )
    if result.status_code != 200:
      return None

    self.authResponse = json.loads(result.text)

  def injectHeaders(self, headers):
    headers["Content-type"] = "application/vnd.api+json"
    headers["Accept"] = "application/vnd.api+json"
    headers["Authorization"] = "Bearer " + self.authResponse["access_token"]

  def refresh(self):
    #print("Call to EthosLoginSession Refresh - getting new token")
    self._getNewAuthToken(fromRefresh=True)
    #print("get new auth token returned")
    if self.currentAuthKey is None:
      #print("no auth key so returning false")
      return False
    #print("Returning true to signal to retry origional request")
    return True
