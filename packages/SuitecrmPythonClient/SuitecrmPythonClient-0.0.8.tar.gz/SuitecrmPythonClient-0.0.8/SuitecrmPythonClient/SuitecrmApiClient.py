import PythonAPIClientBase
from .SuitecrmLoginSession import SuitecrmLoginSessionBasedOnClientIdAndSecret
from .ResourceWrappers import moduleFactory
import json


class SuitecrmApiClient(PythonAPIClientBase.APIClientBase):
  api_prefix = '/legacy/Api/V8'

  refreshAuthTokenIfRequired = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True)

  def getLoginSessionBasedOnClientIdAndSecret(self, clientId, clientSecret):
    return SuitecrmLoginSessionBasedOnClientIdAndSecret(APIClient=self, clientId=clientId, clientSecret=clientSecret)

  def getModules(self, loginSession):
    result = self.sendGetRequest(
      url=self.api_prefix + '/meta/modules',
      loginSession=loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.raiseResponseException(result)

    resultDict = json.loads(result.text)
    if resultDict["data"]["type"] != "modules":
      raise Exception("Unexpected response")

    modules = {}
    for moduleKey in resultDict["data"]["attributes"].keys():
      modules[moduleKey] = moduleFactory(api_client=self, key=moduleKey, moduleData=resultDict["data"]["attributes"][moduleKey])

    return modules
