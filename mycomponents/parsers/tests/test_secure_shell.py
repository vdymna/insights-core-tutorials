from mycomponents.parsers.secure_shell import SSHDConfig
from mycomponents.parsers import secure_shell
from insights.tests import context_wrap
import doctest


SSHD_CONFIG_INPUT = """
#    $OpenBSD: sshd_config,v 1.93 2014/01/10 05:59:19 djm Exp $

Port 22
#AddressFamily any
ListenAddress 10.110.0.1
Port 22
ListenAddress 10.110.1.1
#ListenAddress ::

# The default requires explicit activation of protocol 1
#Protocol 2
Protocol 1
"""


def test_sshd_config():
    sshd_config = SSHDConfig(context_wrap(SSHD_CONFIG_INPUT))
    assert sshd_config is not None
    assert 'Port' in sshd_config
    assert 'PORT' in sshd_config
    assert sshd_config['port'] == ['22', '22']
    assert 'ListenAddress' in sshd_config
    assert sshd_config['ListenAddress'] == ['10.110.0.1', '10.110.1.1']
    assert sshd_config['Protocol'] == ['1']
    assert 'AddressFamily' not in sshd_config
    ports = [l for l in sshd_config if l.keyword == 'Port']
    assert len(ports) == 2
    assert ports[0].value == '22'


def test_sshd_documentation():
    env = {
        'sshd_config': SSHDConfig(context_wrap(SSHD_CONFIG_INPUT))
    }
    failed, total = doctest.testmod(secure_shell, globs=env)
    assert failed == 0


SSHD_CONFIG_INPUT_2 = """
Port 22
Port 22
"""


def test_sshd_corner_cases():
    sshd_config = SSHDConfig(context_wrap(SSHD_CONFIG_INPUT_2))
    assert sshd_config.last('ListenAddress') is None
    assert sshd_config['AddressFamily'] is None
    ports = [l for l in sshd_config if l.keyword == 'Port']
    assert len(ports) == 2
    assert ports[0].value == '22'
