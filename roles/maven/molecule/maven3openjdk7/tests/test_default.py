import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_maven_installed(host):

    # Maven expected version major
    maven_major = '3'

    # Maven expected version minor
    maven_minor = '0.5'

    # Maven expected version
    expected_maven_version = maven_major + '.' + maven_minor

    # Maven Home Path
    expected_maven_home_path = '/opt/maven/maven-{}'\
                               .format(expected_maven_version)

    # Maven archive file
    expected_maven_archive_path = '/tmp/maven-{}.tar.gz'\
                                  .format(expected_maven_version)

    # Check Maven Home Path exists
    assert host.file(expected_maven_home_path).exists
    assert host.file(expected_maven_home_path).is_directory

    # Maven Downloaded file
    maven_archive = host.file(expected_maven_archive_path)

    # Check that Maven Archive exists
    assert maven_archive.exists
    assert maven_archive.is_file

    # Run Maven home
    m2_home = host.run('. {} && echo $M2_HOME'
                       .format('/etc/profile.d/maven_home.sh'))\
                  .stdout.split('\n')[0]

    # Get M2_HOME
    assert m2_home == expected_maven_home_path
