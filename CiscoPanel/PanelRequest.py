import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#   每个设备有不同的账号密码
#   先设定每个设备账号密码都一样

class PanelRequest:
    urls_hostname = {
        "https://192.168.88.10": "hostname",
        "https://192.168.88.11": "hostname"
    }

    def __init__(self, switchuser, switchpassword):
        self.headers = {'content-type': 'application/json-rpc'}
        self.switchuser = switchuser
        self.switchpassword = switchpassword
        self.payload = [
            {
                "jsonrpc": "2.0",
                "method": "cli",
                "params": {
                    "cmd": "",
                    "version": 1
                },
                "id": 1
            }
        ]

    @classmethod
    def update_hostname(cls):
        pr = PanelRequest("admin", "admin")
        for k in cls.urls_hostname.keys():
            cls.urls_hostname[k] = pr.show_hostname(k)

    @classmethod
    def get_device_names(cls):
        return list(cls.urls_hostname.values())

    @classmethod
    def get_url(cls, now_device):
        for k, v in cls.urls_hostname.items():
            if v in now_device:
                return k

    def login(self, url="https://192.168.88.10"):
        # 验证密码在某设备的正确性
        headers = {'content-type': 'application/json'}
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.switchuser,
                    "pwd": self.switchpassword
                }
            }
        }
        response = requests.post(url + "/api/aaaLogin.json", json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def run(self, url, cmd):
        self.payload[0]["params"]["cmd"] = cmd
        response = requests.post(url + "/ins", data=json.dumps(self.payload), headers=self.headers,
                                 auth=(self.switchuser, self.switchpassword), verify=False)
        result = response.json()
        if result["result"] is None:
            return "None"
        else:
            return result["result"]["body"]

    def show_mac_address_table(self, url):
        return self.run(url, "show mac address-table")

    def show_version(self, url):
        return self.run(url, "show version")

    def hostname(self, url, name):
        self.run(url, "hostname " + name)

    def show_running_config(self, url):
        return self.run(url, "show running-config")

    def show_hostname(self, url):
        return self.run(url, "show hostname").get("hostname")

    def show_interface_counters(self, url):
        return self.run(url, "show interface counters")

    def show_ip_interface_brief(self, url):
        tmp = self.run(url, "show ip interface brief")
        if tmp == "None":
            return "None"
        else:
            tmp = tmp["TABLE_intf"]["ROW_intf"]
            if isinstance(tmp, dict):
                return [tmp]
            else:
                return tmp

    def show_processes_memory(self, url):
        return self.run(url, "show processes memory")

    def show_processes_cpu(self, url):
        return self.run(url, "show processes cpu")




if __name__ == '__main__':
    # PanelRequest.update_hostname()
    panel_request = PanelRequest()
    # panel_request.switchpassword = "admin"
    # panel_request.switchuser = "admin"
    print(panel_request.login("admin", "admin", "https://192.168.88.10"))
    # print(panel_request.hostname("https://192.168.88.10", "shit"))
    # panel_request.login(url, "admin", "admin")
    # print(panel_request.show_mac_address_table())
    # print(panel_request.show_running_config())
    # print(panel_request.show_version())
    # print(panel_request.show_hostname())
    # print(panel_request.show_interface_counters())
    # print(panel_request.show_ip_interface_brief())
    # print(panel_request.show_processes_cpu())
    # print(panel_request.show_processes_memory())




