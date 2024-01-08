from asyn_http_request import *

# CLASS CONTAINING FUNCTIONS FOR API CALL
class ApiCalls(AsyncHttpRequest):
    def __init__(self, usermail, password):
        self.usermail = usermail
        self.password = password
        self.email_token = None
        self.login_token = None
        self.customerId = None
        self.targetBrowser = "chrome-incognito"
        self.dryRunFlag = False
        self.refnPlaybackFlag = True
        self.tcEnvironment = "general"
        self.userId = None

    async def login_email(self):
        url = "https://simplifyqa.app/authorize/email"
        headers = {"Content-Type": "application/json", "Authorization": ""}
        payload = {"email": self.usermail, "type": "web"}

        response_data = await self.make_post_request(url, headers, payload)
        if response_data:
            self.email_token = response_data.get("token")
            await self.login_local()

    async def login_local(self):
        url = "https://simplifyqa.app/authorize/local"
        headers = {"Content-Type": "application/json","Authorization": self.email_token,}
        payload = {
            "company": "Simplify3x",
            "email": self.usermail,
            "password": self.password,
            "type": "web",
        }

        response_data = await self.make_post_request(url, headers, payload)
        if response_data:
            self.login_token = response_data.get("token")
            userName = response_data.get("user").get("username")
            self.customerId = response_data.get("user").get("customerId")
            self.userId = response_data.get("user").get("id")
            projectIds = response_data.get("user").get("projects")
            print("\n\nLOGIN WAS SUCCESSFULL")
            await self.search(projectIds)

    async def search(self, projectIds):
        while True:
            print("\nSelect a Project ID:")
            for index, project_id in enumerate(projectIds):
                print(f"{index + 1}. {project_id}")

            choice = int(
                input("Enter your choice: ")
            )

            # VALIDATING USER INPUT FOR PROJECT INDEX
            if choice > len(projectIds) or choice <= 0:
                print("Invalid Choice")
            else:
                projectId = projectIds[choice - 1]
                print(projectId)
                searchString = input("Enter Serach String: ")
                url = "https://simplifyqa.app/search"
                headers = {"Content-Type": "application/json","Authorization": self.login_token,}
                payload = {
                    "searchColumns": [
                        {
                            "column": "name",
                            "value": searchString,
                            "regEx": True,
                            "type": "string",
                            "condition": "or",
                        },
                        {
                            "column": "description",
                            "value": searchString,
                            "regEx": True,
                            "type": "string",
                            "condition": "or",
                        },
                        {
                            "column": "moduleId",
                            "value": [],
                            "regEx": False,
                            "type": "array",
                            "condition": "or",
                        },
                        {
                            "column": "createdBy",
                            "value": [],
                            "regEx": False,
                            "type": "array",
                            "condition": "or",
                        },
                        {
                            "column": "updatedBy",
                            "value": [],
                            "regEx": False,
                            "type": "array",
                            "condition": "or",
                        },
                        {
                            "column": "customerId",
                            "value": self.customerId,
                            "regEx": False,
                            "type": "integer",
                        },
                        {
                            "column": "deleted",
                            "value": False,
                            "regEx": False,
                            "type": "boolean",
                        },
                        {
                            "column": "projectId",
                            "value": projectId,
                            "regEx": False,
                            "type": "integer",
                        },
                        {"column": "id", "sort": "dsc"},
                        {
                            "column": "code",
                            "value": searchString,
                            "regEx": True,
                            "type": "string",
                            "condition": "or",
                        },
                        {
                            "column": "userstoryId",
                            "value": [],
                            "regEx": False,
                            "type": "array",
                            "condition": "or",
                        },
                        {
                            "column": "createdOn",
                            "value": searchString,
                            "regEx": True,
                            "type": "date",
                            "condition": "or",
                        },
                        {
                            "column": "updatedOn",
                            "value": searchString,
                            "regEx": True,
                            "type": "date",
                            "condition": "or",
                        },
                        {
                            "column": "obsolete",
                            "value": False,
                            "regEx": False,
                            "type": "boolean",
                        },
                    ],
                    "startIndex": 0,
                    "limit": 5,
                    "collection": "testcase",
                }

                response_data = await self.make_post_request(url, headers, payload)
                if response_data and response_data.get('data') and response_data['data'].get('totalCount') == 0:
                    print("Test cases don't exist for the given search criteria.")
                    continue 

                testcase_data = {}
                for item in response_data["data"]["data"]:
                    testcase_id = item["id"]
                    created_by = None
                    for version in item.get("versions", []):
                        if "createdBy" in version:
                            created_by = version["createdBy"]
                            break
                    testcase_data[testcase_id] = {
                        "tcType": item["tcType"],
                        "tcName": item["name"],
                        "testcaseCode": item["code"],
                        "moduleId": item["moduleId"],
                        "tcdeletedFlag": item["versions"][0]["deleted"],
                        "tcVersion": item["versions"][0]["version"],
                        "tcVersionName": item["versions"][0]["name"],
                        "tccreatedBy": created_by,
                    }

    
                while True:
                    print("\nSelect a test to run:")
                    # PRINTING ALL TESTCASES
                    for index, (testcase_id, testcase_info) in enumerate(testcase_data.items()):
                        print(f"{index + 1}. Test ID: {testcase_id}, Test Name: {testcase_info['tcName']}")

                    idx = int(input("Enter your choice: "))

                    # VALIDATING USER INPUT
                    if idx > len(testcase_data) or idx<=0:
                        print("Invalid Choice")
                    else:
                        idx = idx - 1
                        await self.check_status()
                        await self.generate_local_execution_id(idx, testcase_data, projectId)
                        break
                break

    async def check_status(self):
        url = "http://localhost:4012/status"
        headers = {"Content-Type": "application/json", "Authorization": ""}
        payload = {"data": "Alive"}
        response_data = await self.make_post_request(url, headers, payload)

    async def generate_local_execution_id(self, idx, testcase_data, projectId):
        url = "https://simplifyqa.app/localexecution/tc"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.login_token,
            "Connection": "keep-alive",
        }
        selected_testcase = list(testcase_data.values())[idx]
        payload = {
            "customerId": self.customerId,
            "projectId": projectId,
            "userId": self.userId,
            "browserName": self.targetBrowser,
            "mbType": None,
            "devices": [self.targetBrowser],
            "version": selected_testcase.get("tcVersion"),
            "versionName": selected_testcase.get("tcVersionName"),
            "moduleId": selected_testcase.get("moduleId"),
            "testcaseCode": selected_testcase.get("testcaseCode"),
            "testcaseId": list(testcase_data.keys())[idx],
            "tcSeq": 1,
            "deleted": selected_testcase.get("tcdeletedFlag"),
            "createdBy": selected_testcase.get("tccreatedBy"),
            "environmentType": self.tcEnvironment,
            "name": selected_testcase.get("tcName"),
            "dryrun": self.dryRunFlag,
            "tcType": selected_testcase.get("tcType"),
            "referenceplayback": self.refnPlaybackFlag,
            "testdataItr": [],
            "testdataSelected": {},
        }

        response_data = await self.make_post_request(url, headers, payload)
        if response_data:
            parentId=response_data.get('data', [{}])[0].get('id')
            projectId=response_data.get('data', [{}])[0].get('projectId')
            await self.playback_steps(parentId,projectId)

    async def playback_steps(self,parentId,projectId):
        url = "http://localhost:4012/v1/playbacksteps"
        headers = {"Content-Type": "application/json", "Authorization": "","Connection":"keep-alive"}
        payload = {
                    "customerID": self.customerId,
                    "projectID": projectId,
                    "executionID": parentId,
                    "authKey": self.login_token,
                    "serverIp": "https://simplifyqa.app",
                    "mbType": None
                }

        response_data = await self.make_post_request(url, headers, payload)

