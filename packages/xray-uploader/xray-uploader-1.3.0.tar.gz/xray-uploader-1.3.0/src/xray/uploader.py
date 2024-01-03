import logging
import requests
import json
import os
from src.helper.logger import logger
from src.helper.junit_xml import JunitXml


class Uploader:
    def __init__(self, client_id, client_secret):
        self._id = client_id
        self._secret = client_secret
        self._token = None

    def fetch_token(self):
        url = 'https://xray.cloud.getxray.app/api/v1/authenticate'
        cloud_auth = {
            'client_id': self._id,
            'client_secret': self._secret
        }
        logger.debug('try to get the token from xray.')
        res = requests.post(url=url, data=cloud_auth)
        try:
            assert res.status_code == 200
        except:
            logging.error(res.text)
            raise
        self._token = res.text.strip('"')
        logger.debug('Get the token successfully.')

    @staticmethod
    def dump_info(info_json, execution_summary, project_id, testplan_id):
        info = {
            'fields': {
                'project': {
                    'id': project_id
                },
                'summary': execution_summary,
                'issuetype': {
                    'id': '10221'
                }
            }
        }
        if testplan_id:
            info['xrayFields']['testPlanKey'] = testplan_id
        logger.info(f'Posted info {info}')
        json.dump(info, open(info_json, 'w'))

    def import_execution(self, junit_xml, execution_summary, project_id, testplan_id, safe_mode=False):
        """
        :param junit_xml: junit format xml file path
        :param execution_summary: test execution summary
        :param project_id: jira project id, string type
        :param testplan_id: test plan id, string type
        :param safe_mode: boolean type, false by default, otherwise it will remove test case nodes which do not have
        child node "property" and corresponding attributes "test_key" and "value" inside.
        """
        self.fetch_token()
        if safe_mode:
            updated_xml = junit_xml.replace('py_result', 'xray_result')
            JunitXml(junit_xml).dump_xray_format_xml(updated_xml)
        else:
            updated_xml = junit_xml
        url = 'https://xray.cloud.getxray.app/api/v1/import/execution/junit/multipart'
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        info_json = os.path.join(os.path.dirname(__file__), 'info_temp.json')
        self.dump_info(info_json, project_id, testplan_id, execution_summary)
        files = {
            'info': open(info_json, 'rb'),
            'results': open(updated_xml, 'rb')
        }
        logger.debug('Try to import the execution into xray.')
        logger.info(f'Headers: {json.dumps(headers)}')
        res = requests.post(url, headers=headers, files=files)
        logger.info(f'Status code: {res.status_code}')
        try:
            assert res.status_code == 200
            logger.info(res.text)
        except:
            logging.error(res.text)
            raise
        logger.debug('Import the execution into xray successfully.')

