
import os
import re
import socket
import requests
from apminsight import constants
from apminsight.logger import agentlogger
from apminsight.util import is_non_empty_string


class ConfigReader:

    @staticmethod
    def get_collector_host(license_key, info):

        host = os.getenv(constants.apm_collector_host, '')
        if is_non_empty_string(host):
            return host

        if 'apm_collector_host' in info and is_non_empty_string(info['apm_collector_host']):
            return info['apm_collector_host']

        if is_non_empty_string(license_key):
            if license_key.startswith('eu_'):
                return constants.eu_collector_host

            if license_key.startswith('cn_'):
                return constants.cn_collector_host

            if license_key.startswith('in_'):
                return constants.ind_collector_host

            if license_key.startswith('au_'):
                return constants.aus_collector_host
            
            if license_key.startswith('jp_'):
                return constants.jp_collector_host

            return constants.us_collector_host

        return ''


    @staticmethod
    def get_license_key(info):
        license_key = os.getenv(constants.license_key_env)
        if is_non_empty_string(license_key):
            return license_key
        if 'license_key' in info and is_non_empty_string(info['license_key']):
            return info['license_key']
        return ''

    @staticmethod
    def get_app_name(info):

        app_name = os.getenv(constants.apm_app_name)
        if is_non_empty_string(app_name) and re.fullmatch('^[A-Za-z0-9]+[-:@_/()|\\ A-Za-z0-9]*',app_name):
            return app_name
        if 'appname' in info and is_non_empty_string(info['appname']) and re.fullmatch('^[A-Za-z0-9]+[-:@_/()|\\ A-Za-z0-9]*',info['appname']):
            return info['appname']

        return constants.default_app_monitor_name


    @staticmethod
    def get_app_port(info):
        app_port = os.getenv(constants.apm_app_port)
        if is_non_empty_string(app_port) :
            return app_port
        if 'app_port' in info and is_non_empty_string(info['app_port']):
            return info['app_port']

        return constants.default_app_port

    @staticmethod
    def get_collector_port(info):
        collector_port = os.getenv(constants.apm_collector_port)
        if is_non_empty_string(collector_port):
            return collector_port
        if 'apm_collector_port' in info and is_non_empty_string(info['apm_collector_port']):
            return info['apm_collector_port']

        return constants.ssl_port

    @staticmethod
    def get_proxy_server_host(info):
        proxy_server_host = os.getenv('PROXY_SERVER_HOST')
        if is_non_empty_string(proxy_server_host):
            return proxy_server_host
        if 'proxy_server_host' in info and is_non_empty_string(info['proxy_server_host']):
            return info['proxy_server_host']
        return None

    @staticmethod
    def get_proxy_server_port(info):
        proxy_server_port = os.getenv('PROXY_SERVER_PORT')
        if is_non_empty_string(proxy_server_port):
            return proxy_server_port
        if 'proxy_server_port' in info and is_non_empty_string(info['proxy_server_port']):
            return info['proxy_server_port']
        return None

    @staticmethod
    def get_proxy_auth_username(info):
        proxy_auth_username = os.getenv('PROXY_AUTH_USERNAME')
        if is_non_empty_string(proxy_auth_username):
            return proxy_auth_username
        if 'proxy_auth_username' in info and is_non_empty_string(info['proxy_auth_username']):
            return info['proxy_auth_username']
        return None

    @staticmethod
    def get_proxy_auth_password(info):
        proxy_auth_password = os.getenv('PROXY_AUTH_PASSWORD')
        if is_non_empty_string(proxy_auth_password):
            return proxy_auth_password
        if 'proxy_auth_password' in info and is_non_empty_string(info['proxy_auth_password']):
            return info['proxy_auth_password']
        return None

    @staticmethod
    def get_fqdn():
        try:
            return socket.getfqdn()
        except Exception:
            agentlogger.info("while fetching fqdn")
        return ''
            
    @staticmethod
    def is_aws():
        try: 
            response = requests.get(constants.aws_url, timeout=0.005)
            if(response.status_code == 200 and  is_non_empty_string(response.text)):
                cloud_instance_id = response.text
                cloud_type = "AWS"
                return (True, cloud_type, cloud_instance_id)
        except Exception:
            agentlogger.info('AWS instance checking Failed')

        return False

    @staticmethod
    def is_azure(): 
        try:
            headers = {'content-type': 'application/json'}
            response = requests.get(constants.azure_url, headers=headers, timeout=0.005)
            if(response.status_code == 200 and is_non_empty_string(response.json().get('ID'))):
                cloud_instance_id = response.json().get('ID')
                cloud_type = "AZURE"
                return (True, cloud_type, cloud_instance_id)
        except Exception:
            agentlogger.info('Azure instance checking Failed')

        return False

    @staticmethod
    def get_docker_env_details():
        host_name = None
        host_type = None
        try:
            with open('/proc/self/cgroup','r') as cgroup:
                cgroup_info = cgroup.read()
                if(isinstance(cgroup_info,str) and is_non_empty_string(cgroup_info)):
                    line_with_id = [ info for info in cgroup_info.split('\n') if "docker/" in info]
                    if (line_with_id) :
                        id = line_with_id[0].split('docker/').pop()
                        host_name = id
                        host_type = 'DOCKER'
                        return (True, host_type, host_name) 
                    else :
                        agentlogger.info("Not a docker environment.") 
                else:
                    with open('/proc/self/cpuset','r') as cpuset:
                        cpuset_info = cpuset.read()
                        if(isinstance(cpuset_info,str) and is_non_empty_string(cpuset_info)):
                            id = cgroup_info.replace("/docker/","")
                            host_name = id
                            host_type = 'DOCKER'
                            return (True, host_type, host_name)
                        else :
                            agentlogger.info("Not a docker environment.") 
        except Exception:
            agentlogger.info('Exception checking docker environment')
        return (False, host_type, host_name)

    @staticmethod
    def get_cloud_details():
        aws =  ConfigReader.is_aws()
        azure = ConfigReader.is_azure()
        if aws:
            return aws 
        elif azure:
            return azure
        return (False, None, None)

    @staticmethod
    def using_exporter(info):
        using_exporter = info.get('exporter', True)
        if using_exporter:
            return True
        return False

    @staticmethod
    def get_exporter_status_port(info):
        exporter_status_port = os.getenv(constants.APM_EXP_STATUS_PORT)
        if is_non_empty_string(exporter_status_port):
            return exporter_status_port
        if 'exporter_status_port' in info and is_non_empty_string(info['exporter_status_port']):
            return info['exporter_status_port']
        return constants.default_exp_status_port

    @staticmethod
    def get_exporter_data_port(info):
        exporter_data_port = os.getenv(constants.APM_EXP_DATA_PORT)
        if is_non_empty_string(exporter_data_port):
            return exporter_data_port
        if 'exporter_data_port' in info and is_non_empty_string(info['exporter_data_port']):
            return info['exporter_data_port']
        return constants.default_exp_data_port
    
    @staticmethod
    def get_exporter_host(info):
        exporter_host = os.getenv(constants.APM_EXP_HOST)
        if is_non_empty_string(exporter_host):
            return exporter_host
        if 'exporter_host' in info and is_non_empty_string(info['exporter_host']):
            return info['exporter_host']
        return constants.localhost_str