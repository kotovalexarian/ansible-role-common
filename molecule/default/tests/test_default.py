import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize(
    'package_name',
    [
        'apache2',
        'apt-transport-https',
        'bash-completion',
        'certbot',
        'colordiff',
        'curl',
        'gnupg',
        'gnupg2',
        'iptables-persistent',
        'less',
        'libapache2-mod-php',
        'nginx',
        'procps',
        'software-properties-common',
        'vim',
        'wget',
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


def test_apache_default_removed(host):
    assert host.file('/etc/apache2/sites-available/000-default.conf').exists
    assert not host.file('/etc/apache2/sites-enabled/000-default.conf').exists


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
    assert f.contains(
        'ssl_ciphers "ECDHE-ECDSA-CHACHA20-POLY1305:'
        'ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:'
        'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:'
        'ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:'
        'DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:'
        'ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:'
        'ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:'
        'ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:'
        'ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:'
        'DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:'
        'ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:'
        'AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:'
        'AES256-SHA:DES-CBC3-SHA:!DSS";'
    )
