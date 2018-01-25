"""
A simple script that serves as sandbox for trying out libcloud and python.
Getting acquainted with this is necessary before jumping into Errbot-libcloud integration.

** This is not a ready-to-go script! Read and modify before running!**

HOW TO RUN
----------

First read the script and ensure you have customized it as needed.

This script needs to be run within a virtualenv, make sure you have run:
pipenv install
pipenv shell

Then run
python samples/aws.py
"""

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeLocation,NodeSize
import sys,os
ACCESS_ID = os.environ['ERRBOT_AWS_ACCESS_KEY']
SECRET_KEY = os.environ['ERRBOT_AWS_SECRET_KEY']
AWS_ACCOUNT_ID = os.environ['ERRBOT_AWS_ACCOUNT_ID']
AWS_REGION = os.environ['ERRBOT_AWS_DEFAULT_REGION']
MY_IMAGE_ID = "ami-c24ef5bb"
MY_SIZE = "t2.medium"
MY_NODE_NAME = "test_node"
EC2Driver = get_driver(Provider.EC2)
driver = EC2Driver(ACCESS_ID, SECRET_KEY,region=AWS_REGION)

def usage():
    print("""
USAGE:
    python {0} [ARGS]
ARGS:
    create : create an instance named {5} using predefined AMI {1} and Size {2}.
    delete: delete instances matching name {5}
    list_images: list images and exit.
    list_instances: list running instances owned by {3} in region {4} and exit.
    """.format(sys.argv[0],MY_IMAGE_ID,MY_SIZE,AWS_ACCOUNT_ID,AWS_REGION,MY_NODE_NAME))

def parse_input():
    if len(sys.argv) < 2:
        usage()
        raise Exception("Incorrect Argument Length!")
    elif len(sys.argv) > 2:
        usage()
        raise Exception("Exactly 1 argument expected!")
    elif sys.argv[1] not in ['create','delete','list_images','list_instances']:
        usage()
        raise Exception("Unknown 1st Argument!")

    return sys.argv[1]

def getImage(image_id):
    images = driver.list_images(ex_owner=AWS_ACCOUNT_ID)
    image = [i for i in images if i.id == image_id][0]
    return image

def getSize(size_id):
    sizes = driver.list_sizes()
    size = [i for i in sizes if i.id == size_id][0]
    return size

def getNode(node_name):
    nodes = driver.list_nodes()
    node = [i for i in nodes if (i.name == node_name and i.state != 'terminated')][0]
    return node

def getLocation(location_id):
    locations = driver.list_locations()
    print(locations[0])
    location = [i for i in locations if i.id in location_id][0]
    return location

def create():
    if action_needed("create"):
        print("creating {0}".format(MY_NODE_NAME))
        node = driver.create_node(
                name=MY_NODE_NAME,
                size=getSize(MY_SIZE),
                image=getImage(MY_IMAGE_ID))
        print("waiting for node to be ready...")
        driver.wait_until_running([node])
    else:
        print("matching node already created, no action.")

def action_needed(action):
    nodes = driver.list_nodes()
    for n in nodes:
        print("node: {0}, image: {1}, ip: {2}".format(n.name,n.image,n.public_ips))
        if ((n.name == MY_NODE_NAME)):
            if (action == 'create'):
                return False
            elif (action == 'delete'):
                return True
            else: raise Exception("unknown: {0}".format(action))

    # if it reached here it means matching nodes are not found and create is needed..
    if (action == 'create'):
        return True
    elif (action == 'delete'):
        return False

def list_instances():
    """
    Lists instances regardless of their state.
    Terminated instances can be visible in the list for a short while.
    """
    for n in driver.list_nodes():
        print("node: {0}, image: {1}, status: {2}, ip: {3}".format(n.name,n.image,n.state,n.public_ips))

def delete():
    if action_needed("delete"):
        print("delete node named " + MY_NODE_NAME)
        node = getNode(MY_NODE_NAME)
        driver.destroy_node(node)
    else: print("matching nodes not found, delete not needed")
## MAIN

action = parse_input()
if action == 'list_images':
    img = getImage(MY_IMAGE_ID)
    print("node image: {0}".format(img))
    exit(0)
elif action == 'list_instances':
    print(list_instances())
    exit(0)
elif action == 'create':
    create()
elif action == 'delete':
    delete()
