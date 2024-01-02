import requests
import json
import datetime
import time

#       This defines the 'SpiraTestExecute' class that provides the Python facade
#       for calling the REST web service exposed by SpiraTest
#
#       Author          Inflectra Corporation
#       Version         6.0.0
#       Notes           Requires Python 3.0 or later

class SpiraTestExecute:

        # The URL snippet used after the Spira URL
        REST_SERVICE_URL = "/Services/v6_0/RestService.svc/"
        # The URL spippet used to post an automated test run. Needs the project ID to work
        POST_TEST_RUN = "projects/%s/test-runs/record"

        def recordTestRun(self, test_case_id, release_id, test_set_id, start_date, end_date, execution_status_id, runner_name, test_name, assert_count, message, stack_trace):
                
                """
                Post the test run to Spira with the given credentials
                """
                url = self.url + self.REST_SERVICE_URL + \
                (self.POST_TEST_RUN % self.project_id)
                # The credentials we need
                params = {
                'username': self.username,
                'api-key': self.api_key
                }

                # The headers we are sending to the server
                headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': runner_name
                }

                # The body we are sending
                body = {
                # Constant for plain text
                'TestRunFormatId': 1,
                'StartDate': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'EndDate': end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'RunnerName': runner_name,
                'RunnerTestName': test_name,
                'RunnerMessage': message,
                'RunnerAssertCount': assert_count,
                'RunnerStackTrace': stack_trace,
                'TestCaseId': test_case_id,
                # Passes (2) if the stack trace length is 0
                'ExecutionStatusId': execution_status_id
                }

                # Releases and Test Sets are optional
                if(release_id != -1):
                        body["ReleaseId"] = int(release_id)
                if(test_set_id != -1):
                        body["TestSetId"] = int(test_set_id)

                dumps = json.dumps(body)

                response = requests.post(url, data=json.dumps(body), params=params, headers=headers)

                if response.status_code == 200:
                        print("Successfully recorded the result for test case: " + str(test_case_id))
                else:
                        print ("Failed to send results to SpiraTest: ", response.status, response.reason, output)
