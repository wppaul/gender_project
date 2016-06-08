Project Name : Gender Identification and Sentiment Analysis on Twitter through machine learning approaches
==========================================================================================================

Author :  PENG WANG
Student Number : 680868
Supervisor : Prof. Richard Sinnott
Subject: COMP90055 COMPUTING PROJECT

*************** Boto Instructions *************************************

# Boto can be started individually by python command if required:
`python boto_install_VMS`

*************** Ansible Instructions **********************************

# The site yml files consists of few sub-yml files(boto,yml,allservers.yml,webservers.yml), and each yml file can run individually based on the requirements, roles has been created for enhacning the flexibility and reusability, this includes updatecache,sharedsoftware,machinelearningpackage, mountvolume,installcouchdb,pushfiles,startharvester,rails,startwebserver as well as startboto
# Instructions for system deployment automation

site.yml                # master playbook
startboto.yml           # playbook for starting boto
allservers.yml          # playbook for all servers
webservers.yml          # playbook for web servers 


#Run everything :
`ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts site`

#Run boto only :
`ansible-playbook -i hosts startboto.yml`

#Run all cloud services:
`ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts allservers.yml`

#Run web services only:
`ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts webservers.yml`

#creating new roles by ansible-galaxy:
`ansible-galaxy init rolename`

