# References:
# https://docs.pytest.org/en/latest/fixture.html#fixture-function

import pytest
import os
CONFIG = {
    'access_id': os.environ['ERRBOT_AWS_ACCESS_KEY'],
    'secret_key': os.environ['ERRBOT_AWS_SECRET_KEY'],
    'account_id': os.environ['ERRBOT_AWS_ACCOUNT_ID'],
    'region': os.environ['ERRBOT_AWS_DEFAULT_REGION'],
    'keypair': os.environ['ERRBOT_AWS_KEYPAIR_NAME'],
}

@pytest.fixture
def constants():
    return {
        "TEST_AMI_ID": 'ami-c24ef5bb',
        "TEST_NODE_NAME": 'test_node',
        "TEST_NODE_SIZE": 't2.micro'
    }


@pytest.fixture
def config():
    return CONFIG

@pytest.fixture(scope='class')
def driver():
    """
    Get an initialized libcloud driver.
    """

    from libcloud.compute.types import Provider
    from libcloud.compute.providers import get_driver
    xy = get_driver(Provider.EC2)
    libcloud_driver = xy(CONFIG['access_id'], CONFIG['secret_key'], region=CONFIG['region'])

    return libcloud_driver

@pytest.fixture
def awsadapter():
    """
    Return an initialized AwsAdapter object.
    """
    from awsadapter import AwsAdapter
    return AwsAdapter(CONFIG)

