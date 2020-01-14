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
