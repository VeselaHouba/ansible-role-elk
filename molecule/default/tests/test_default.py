import os

import yaml

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_is_running(host):
    cmd = host.service('docker')
    assert cmd.is_running
    assert cmd.is_enabled


def test_docker_daemon_connection(host):
    c = host.run('docker ps')
    assert c.rc == 0


def test_docker_container_start(host):
    with host.sudo():
        c = host.run('docker run --rm alpine:3.12.0 cat /etc/alpine-release')
        assert c.rc == 0
        assert '3.12.0' in c.stdout


def test_services_running(host):
    c = host.run('docker ps')
    assert 'logstash' in c.stdout
    assert 'elasticsearch' in c.stdout
    assert 'cerebro' in c.stdout
    assert 'elastalert' in c.stdout
    assert 'kibana' in c.stdout
    assert c.rc == 0


def test_correct_version_running(host):
    stream = host.file('/tmp/ansible-vars.yml').content
    ansible_vars = yaml.load(stream, Loader=yaml.FullLoader)
    def_version = ansible_vars['elk_version']
    c = host.run('wget -qcO - --retry-connrefused localhost:9200')
    assert c.rc == 0
    assert def_version in c.stdout


def test_elastalert_connected(host):
    c = host.run('docker logs elastalert')
    assert 'Reading index mapping' in c.stdout
