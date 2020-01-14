import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize(
    'package_name',
    ['bash-completion', 'colordiff', 'curl', 'less', 'vim'],
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
