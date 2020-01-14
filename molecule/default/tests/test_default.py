import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize(
    'package_name',
    [
        'bash-completion',
        'colordiff',
        'curl',
        'iptables-persistent',
        'less',
        'vim',
    ],
)
def test_packages(host, package_name):
    assert host.package(package_name).is_installed


def test_vim_config(host):
    f = host.file('/etc/vim/vimrc.local')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644


def test_default_editor(host):
    f = host.file('/usr/bin/editor')

    assert f.exists
    assert f.is_symlink
    assert f.linked_to == '/usr/bin/vim.basic'


@pytest.mark.parametrize('version', [4, 6])
def test_iptables_config(host, version):
    f = host.file('/etc/iptables/rules.v%d' % version)

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644


def test_nginx_default_removed(host):
    assert host.file('/etc/nginx/sites-available/default').exists
    assert not host.file('/etc/nginx/sites-enabled/default').exists


def test_certbot_exe(host):
    f = host.file('/usr/local/bin/certbot-auto')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o755


def test_certbot_cli_config(host):
    f = host.file('/etc/letsencrypt/cli.ini')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644


def test_certbot_nginx_config(host):
    f = host.file('/etc/letsencrypt/options-ssl-nginx.conf')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
