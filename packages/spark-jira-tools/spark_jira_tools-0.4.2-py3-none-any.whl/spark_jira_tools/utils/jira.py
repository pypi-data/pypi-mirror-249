import json

import requests


class Jira(object):

    def __init__(self, username=None, token=None, proxy=False):
        self._session = requests.Session()
        self.base_url = "https://jira.globaldevtools.bbva.com"
        self.base_path = "/rest/auth/1/session"
        self.proxies = proxy
        url = f"{self.base_url}{self.base_path}"
        if username is None and token is None:
            payload = json.dumps({
                "username": "jonathan.quiza",
                "password": "MTc1MzM5NzEyMTA0OqK/nSm+o45gAPayE0q6nkd25xIE"
            })
        else:
            payload = json.dumps({
                "username": username,
                "password": token
            })

        self.current_proxies = {
            'https': 'http://118.180.54.170:8080',
            'http': 'http://118.180.54.170:8080'
        }

        self.headers = {
            'Content-Type': 'application/json'
        }
        if not self.proxies:
            self.r = self._session.post(url, headers=self.headers, data=payload)
        else:
            self.r = self._session.post(url, headers=self.headers, data=payload, proxies=self.current_proxies)
        self.cookies = requests.utils.dict_from_cookiejar(self.r.cookies)

        self._session.cookies.update(self.cookies)
        self._session.headers.update(self.headers)

        if not self.proxies:
            self._session.proxies.update({})
        else:
            self._session.proxies.update(self.current_proxies)

    def get_key_issue(self, issue):
        result_dict = dict()
        result_list = list()
        self.base_path = f"/rest/api/2/issue/{issue}"
        url = f"{self.base_url}{self.base_path}"
        r = self._session.get(url)
        response = r.json()
        result_dict["id"] = response.get("id")
        result_dict["key"] = response.get("key")
        result_dict["self"] = response.get("self")
        result_dict["fields"] = response.get("fields")
        result_list.append(result_dict)
        return result_list

    def get_search_issue(self, assignee=None, table_name=None):
        from dateutil.relativedelta import relativedelta
        from datetime import datetime

        current_date = datetime.now() - relativedelta(months=3)
        current_date = current_date.strftime("%Y-%m-%d")

        data = {
            "jql": f"project='19803' AND assignee='{assignee}' AND updatedDate>='{current_date}' "
                   f"AND summary ~ '{table_name}' and  (status in ('New', 'Analysing', 'Ready', 'In Progress', 'Read To Verify', 'DISCARDED', 'Deployed'))",
            "fields": ["key", "summary", "assignee", "status"]
        }
        payload = json.dumps(data)
        self.base_path = f"/rest/api/2/search"
        url = f"{self.base_url}{self.base_path}"
        r = self._session.post(url, data=payload)
        response = r.json()
        issues = response.get("issues")

        issue_list = list()
        for issue in issues:
            issue_dict = dict()
            issue_dict["id"] = issue.get("id")
            issue_dict["key"] = issue.get("key")
            issue_dict["summary"] = issue.get("fields").get("summary")
            issue_dict["assignee"] = issue.get("fields").get("assignee").get("name")
            issue_dict["status"] = issue.get("fields").get("status").get("name")
            issue_list.append(issue_dict)

        return issue_list

    def generated_issue(self, summary=None, description=None, assignee=None,
                        labels=None, feature_pad=None, acceptance_criteria=None,
                        code_team_backlog=None):
        issue_dict = {
            "fields": {"project": {"key": "PAD3"},
                       "summary": f"{summary}",
                       "description": f"{description}",
                       "issuetype": {"name": "Historia"},
                       'assignee': {'name': f'{assignee}'},
                       'priority': {'name': 'Medium'},
                       'labels': labels,
                       'customfield_10004': f"{feature_pad}",
                       'customfield_10260': f"{acceptance_criteria}",
                       'customfield_10270': {'id': '20247'},
                       'customfield_13300': [f"{code_team_backlog}"],
                       'customfield_18001': {'id': '91610'},
                       }

        }
        payload = json.dumps(issue_dict)
        self.base_path = f"/rest/api/2/issue"
        url = f"{self.base_url}{self.base_path}"
        r = self._session.post(url, data=payload)
        response = r.json()
        return response

    def update_issue(self, issue, data):
        self.base_path = f"/rest/api/2/issue/{issue}"
        url = f"{self.base_url}{self.base_path}"
        self._session.put(url, data=data)
