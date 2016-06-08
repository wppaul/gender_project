# Author :  PENG WANG
# Student Number : 680868
# Supervisor : Prof. Richard Sinnott
# Subject: COMP90055 COMPUTING PROJECT
# Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches

import boto
import time
from boto.ec2.regioninfo import RegionInfo

#Set up the region and Establish the connection
region=RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ec2_comm = boto.connect_ec2(aws_access_key_id='1bf4fd7557a84d559ae85a9455837b78', aws_secret_access_key='9c8d5a0fae2c4c87bd86e42d3ae9fe33', is_secure=True, 
	region=region, port=8773, path='/services"})/Cloud', validate_certs=False)

#This is used to store the ip addresses of Virtual Machines
VM_ips = []
print("Connection is established!")

#Check Security group and add new groups as well as rules if needed

def check_group_status(groupname):
	check = False
	group = ec2_comm.get_all_security_groups()
	for g in group:
	    if g.name == groupname:
	        check = True
	return check

def create_security_group(groupname):
	check = check_group_status(groupname)
	if check == False:
		print("creating security group for %s!" %groupname)
		security_group = ec2_comm.create_security_group(groupname,"allowing %s access!" %groupname)
		if groupname == 'ssh':
			print("adding the new rules for %s!" %groupname)
			security_group.authorize("tcp",22,22,"0.0.0.0/0")
		elif groupname == 'http':
		    print("adding the new rules for %s!" %groupname)
		    security_group.authorize("tcp",80,80,"0.0.0.0/0")
		    security_group.authorize("tcp",443,443,"0.0.0.0/0")
		    security_group.authorize("tcp",5984,5984,"0.0.0.0/0")
	else:
	    print("This Security Group of \"%s\" is available to use!" %groupname)

# Function for Launching Instances
def launch_instance(num_of_instance):
	num = num_of_instance
	for i in range(num):
		ec2_comm.run_instances('ami-000037b9', key_name='project_key', placement='melbourne',instance_type='m1.small', security_groups=['http','ssh'])

# Function for creating and attaching volumes based on the placement of Instance
def attach_volume(instance):
	vol = ec2_comm.create_volume(50,instance.placement)
	vol.attach(instance.id,"/dev/vdc")
	
#  Verify the system status and perform the functions correspondingly
def check_status():
	print("Creating instances......")
	print('Waiting for instances to start......')
	launch_instance(4)
	reservations = ec2_comm.get_all_reservations()
	for i in range(len(reservations)):
		instance = reservations[i].instances[0]
		status = reservations[i].instances[0].update()
		while status == 'pending': # wait till instance is running
			time.sleep(30)
			print("VM%s is %s" %(i,status))
			status = reservations[i].instances[0].update()
		if status == 'running':    # if instance is running then attach the volume correspondingly
			instance.add_tag("Name","VM%s"%i)
			VM_ips.append(instance.ip_address)
			attach_volume(instance)
			print("Instance VM%s is now ready to use" %i)
		else:
			print('Instance VM%s status:' %i + status)

#generate basic host file for ansible automation processes
def output_host_file():
    info = '\n'.join(VM_ips)
    path = '/Users/Paul/desktop/hosts'
    user = 'ansible_user=ubuntu'
    key = 'ansible_private_key_file=/Users/Paul/Desktop/project_key.pem'
    with open(path,'w') as f:
    	f.write('[allservers]\n'+info+'\n\n[allservers:vars]\n'+ user + '\n'+ key)
    print('The ansible host file is generated!')

create_security_group('http')
create_security_group('ssh')
check_status()
output_host_file()
print("Congratulations! The systems are successfully established!!!")