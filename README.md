# CloudComputingWithAWS

- cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet (“the cloud”) to offer faster innovation, flexible resources, and economies of scale

# Benefits of Cloud Computing:
-	Security – monitored 24/7 to ensure confidentiality, integrity and availability of data.  All flowing data across the AWS global network automatically encrypted at the physical layer 
-	Availability – highest availability of any cloud provider.  Each region is fully isolated and comprised of multiple AZs, which are fully isolated partitions of infrastructure.  To better isolate any issues and achieve high availability, you can partition applications across multiple AZs in the same region.
-	Performance – Regions offer low latency, low packet loss, and high overall network quality.  Fully redundant 100 GbE fiber network backbone
-	Global footprint – flexibility in selecting a technology infrastructure that is closest to your primary target of users.  
-	Scalability – conceptually infinite scalability of the cloud.  No longer need to over provision to ensure you have enough capacity to handle business operations at the peak level of activity.  You can provision the amount of resources 
-	Flexibility - choosing how and where you want to run your workloads, and when you do you are using the same network, control plane, API's, and AWS services.  If you would like to run your applications globally you can choose from any of the AWS Regions and AZs. If you need to run your applications with single-digit millisecond latencies to mobile devices and end-users you can choose AWS Local Zones or AWS Wavelength. Or if you'd like to run your applications on-premises you can choose AWS Outposts.

# 3 Types of Cloud Computing
- Private Cloud (OnPrem): This model consists of an infrastructure that is owned by a single business. This model can be hosted in-house or can be externally hosted. Although expensive, the private cloud model is well suited for large organizations with a focus on security, customizability, and computing power.
- Public Cloud: This model consists of services and infrastructure that are shared by all organizations. With huge available space, scalability becomes easier in public cloud solutions. Organizations pay public cloud models on a pay-per-use basis, making it a suitable solution for smaller businesses looking out to save money.
- Hybrid Cloud: A combination of both public and private clouds, a hybrid cloud combines the two models to create a tailored solution that allows both platforms to interact seamlessly.


### AWS (Amazon Web Services) - launch a virtual machine
![diagram](AWS_workflow.png?raw=true "AWS_with_ssh")
- ensure file.pem is read-only `chmod 400 file.pem` and also located in .ssh directory 
- visit Amazon's Global Infrastructure
  - https://aws.amazon.com/about-aws/global-infrastructure/?nc2=type_a
  - sign in to the console or create account
  - under 'services' choose `EC2`
  - `launch instances`
  - `select` virtual machine with appropriate specs
    - Eng110 is using Ubuntu Server 18.04 LTS(HVM) 64-bit (x86)
  - choose an instance type (virtual servers with varying combinations of CPU, memory, storage, and networking capacity)
    - Eng110 is using `t2.micro`
  - bottom of screen click button `Next: Configure Instance Details`
    - choose number of instances
    - choose Network (Eng110 is using default)
    - choose Subnet (Eng110 is using Default in eu-west-1a)
    - Auto-assign Public IP `Enable`
    - Hostname type: Use subnet setting(IP name)
    - DNS Hostname: check box `Enable resource-based IPv4 (A record) DNS requests`
  - bottom of screen click button `Next: Add Storage`
  - Eng110 is using default storage device -> bottom of screen click button `Next: Add Tags`
  - `Add Tag`: key => `Name` value => `eng110_bens`
  - bottom of screen click button `Next: Configure Security Group`
  - either create a new security group or select an existing security group
    - if creating new:
      - follow naming conventions 
        - Security Group Name: `eng110_bens_sg_app`
        - Description: `eng110_bens_sg_app` or `eng110_bens_sg_app - Ben - Jack - Nikhil are only to use` for example
      - Type `SSH` we need for installations
      - Protocol `TCP`
      - Port Range `22` (SSH port)
      - Source `My IP` (Nobody else should be able to access our EC2 instances)
      - Description example `office ip - my ip`
      - click button `Add Rule` to configure for nginx
        - Type `HTTP`
        - Protocol `TCP`
        - Port Range `80`
        - Source `Anywhere`
        - Description example `for nginx - public access`
  - bottom of screen click button `Review and Launch`
    - this gives us an opportunity to view all the details before we purchase
      - click button `launch`
        - now we need to let AWS know that we want to launch this instance and we want to access using whichever key
          - create new key pair or select existing key pair
            - select from dropdown menu (eng110 is using `eng119 | RSA`) then click `Launch Instances`
          - click button `View Instances`
  - select checkbox for instance to display its information below
    - copy Public IPv4 address
    - click button `Connect`
  - We are using SSH client
    - copy example ssh code below for gitbash command to access
    - open an SSH client (gitbash) as admin
  - In gitbash navigate to .ssh directory and ensure the filename.pem key file is inside 
  - paste previously copied ssh code as gitbash command => (example): `ssh -i "eng119.pem" ubuntu@ec2-54-195-173-115.eu-west-1.compute.amazonaws.com` 
  - Now we've successfully landed on AWS
    - Does it have internet? `sudo apt-get update -y`
    - Upgrade: `sudo apt-get upgrade -y`
    - Install nginx: `sudo apt install nginx -y`
  - Once installed go back to 'Connect to instance' AWS page and select `EC2 Instance Connect` tab
    - copy Public IP address and paste into url bar of browser for access

### Adding App files and installing NodeJS (dependencies)
- migrate app and file.pem to cloud
  - scp file.pem localhost/address destination/address
    - example => `scp -i ~/.ssh/eng119.pem -r ~/Downloads/sg_application ubuntu@ec2-54-75-49-179.eu-west-1.compute.amazonaws.com:~/`.
  - access denied - port 22 unavailable - enter new ip in your security group
  - allow port 3000
- Install NodeJS dependencies
  - `sudo apt-get install nodejs -y`
  - `sudo apt-get install python-software-properties -y`
  - `curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -`
  - `sudo apt-get install nodejs -y`
- go to directory of app in app ec2 instance
  - `npm install`
  - `npm start`
- configure reverse proxy - app to work without port 3000
  - We have to redirect the incoming requests of localhost to our NodeJS application running on localhost:3000 
    - `sudo nano /etc/nginx/sites-available/default`
    - In the file, replace the contents of "location /" block to following:
      location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
      }
    - restart Nginx server `sudo service nginx restart` 

### Deploying for MongoDB
- create EC2 instance mostly the same way
  - When adding tags, key: Name  value: eng110_bens_mongodb
  - create a new security group
    - name: eng110_bens_sg_db
    - description: same
    - first change first SSH security group Source to My IP and Description to my ip + add `/32` CIDR block to end of ip address
    - Then `Add Rule`
    - Type: `Custom TCP`
    - Protocol: `TCP`
    - Port Range: `27017`
    - Source: `Custom` + fill in app's public ip address + add `/32` CIDR block to end of ip address
    - Description: app ip
- ssh into instance and continue with the following commands:

  - Install nginx: `sudo apt install nginx -y` 
  - `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv D68FA50FEA312927`
  - `echo "deb https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list`
  - `sudo apt-get update -y`
  - `sudo apt-get upgrade -y`
  - `sudo apt-get install -y mongodb-org=3.2.20 mongodb-org-server=3.2.20 mongodb-org-shell=3.2.20 mongodb-org-mongos=3.2.20 mongodb-org-tools=3.2.20`
  - `sudo systemctl status mongod`
  - `sudo systemctl start mongod`
  - `sudo systemctl enable mongod`
  - `sudo apt-get update -y`
- SSH into the app instance into the app directory
- create environment variable for database 
  - `sudo echo "export DB_HOST=mongodb://<db ip address>:27017/posts" >> ~/.bashrc`
  - `source ~/.bashrc`
  - `npm start`
  - if it doesn't allow connection, we can do it forcefully:
    - SSH into DB instance
    - `cd /etc`
    - `sudo nano mongod.conf`
    - go down to Network Interfaces and change bindIp: `0.0.0.0`
    - restart mongodb: `sudo systemctl restart mongod`
    - enable mongodb: `sudo systemctl enable mongod`
    - check status: `sudo systemctl status mongod`
    - have a look at changes to mongod.conf: `cat mongod.conf`
  - go to app ec2 instance in the app directory
    - `printenv DB_HOST` which will give you DB instance IP address
    - `node seeds/seed.js` you should get: Database cleared Database Seeded
    - `npm start`

### Amazon Machine Images (AMI)
![diagram](AmazonMachineImages.png?raw=true "Amazon Machine Images")
- supported and maintained image provided by AWS that provides the info required to launch an instance.
  - An AMI includes the following:
    - One or more Amazon Elastic Block Store (Amazon EBS) snapshots, or, for instance-store-backed AMIs, a template for the root volume of the instance(for example, an OS, an app server, and apps)
    - Launch permissions that control which AWS accounts can use the AMI to launch instances
    - A block device mapping that specifies the volumes to attach to the instance when it's launched
  
# Benefits of AMIs
  -	Rely on pre-configured templates that allow you to deploy one or more instances
  -	Quickly and efficiently determine what computing power, memory, storage, and other factors you need for your apps
  -	Low cost (it’s a virtual machine that runs in the cloud, and you can deploy and configure each one according to your business needs) no up-front costs as you might expect
  -	Speeds up configuration and deployment because the templates are well-known and defined for typical computing infrastructure needs.  The alternative is more complex where developers would have to define the parameters they need on their own data center servers or architect the virtual servers and settings on their own.  
  -	Flexibility – it can run Linux, Unix, Windows and you can augment the AMI with additional services (compressed, encrypted and secured no matter which OS)
  -	Most advantages same as using EC2 itself (pre-configured templates, pay-as-you-go cost structure, speed of deployment) + ability to scale and experiment with new features of an app or by releasing additional apps without worrying about the infrastructure itself.

  # Setting up AMI
  - In AWS services check to see you're in the right region (Ireland in our case)
  - ssh into ec2 app to ensure it's running ok
  - In AWS console select ec2 app instance within 'Actions' dropdown menu select `Image and templates` `Create image`
  - Image name: `eng110_benswen_app_ami`
  - Description: `eng110_benswen_app_ami_06/05/2022`
  - `Add tag` => key `Name` => Value `eng110_benswen_app_ami` 
  - `Create Image`
  - on the left of the console under Images select `AMIs New`
  - In the search bar above search for your built AMI and select it
  - `Launch Instance from AMI`
  - The rest of the steps are the same as when we launched an instance from Linux
    - Instance type: `t2.micro`
    - Configure Instance Details:
      - Network: vpc (default)
      - Subnet: DevOpsStudent default 1a
      - Auto-assign Public IP: `Enable`
    - Add volume: can stay as default
    - Add Tags: `key => Name value => eng110_benswen_app_from_ami`
    - Configure Security Group:
      - select existing app security group
    - Review Instance Launch:
      - `Launch`
      - select existing key pair
    - click instance link
    - ssh into this instance (change 'root' to 'ubuntu')
    - check nginx is running `sudo systemctl status nginx`
    - navigate to the app folder
    - `npm start`


### Amazon S3
![diagram](AWS_S3.png?raw=true "Amazon S3")
- Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability, data availability, security, and performance.  You can store and protect any amount of data for a range of use cases, such as data lakes, websites, mobile applications, backup and restore, archive, enterprise applications, IoT devices, and big data analytics.
- Install Python
  - `Python --version`
  - `sudo apt install python`
  - `sudo apt install python-pip -y`
  - `alias python=python3`
  - `sudo python -m pip install awscli`
  - `sudo python3 -m pip install boto3`
- Configure AWS
  - `aws configure`
    - 1 aws_access_key:
    - 2 aws_secret_key:
    - 3 format: json
    - 4 regions: eu-west-1
    - `aws s3 ls`
- create bucket in S3
  - `aws s3 mb s3://eng110-ben`
- create text document in ec2 instance
  - `sudo nano test.txt`
- upload file from ec2 to s3
  - `aws s3 cp test.txt s3://eng110-ben/`
- download file from s3 to ec2
  - `aws s3 cp s3://eng110-ben/test.txt test.txt`
- remove file
  - `aws s3 rm s3://eng110-ben/test.txt`
- remove bucket
  - `aws s3 rb s3://eng110-ben`


### AWS Autoscaling group
![diagram](autoScaling.png?raw=true "AWS Autoscaling")
- Contains a collection of Amazon EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management. Both maintaining the number of instances in an Auto Scaling group and automatic scaling are the core functionality of the Amazon EC2 Auto Scaling service.  the Auto Scaling group adjusts the desired capacity of the group, between the minimum and maximum capacity values that you specify, and launches or terminates the instances as needed.
# Benefits
  - Better fault tolerance.  Amazon EC2 auto Scaling can detect when an instance is unhealthy, terminate it, and launch an instance to replace it. You can also configure Amazon EC2 Auto Scaling to use multiple Availability Zones. If one Availability Zone becomes unavailable, Amazon EC2 Auto Scaling can launch instances in another one to compensate
  - Better availability. Amazon EC2 Auto Scaling helps ensure that your application always has the right amount of capacity to handle the current traffic demand
  - Better cost management. Amazon EC2 Auto Scaling can dynamically increase and decrease capacity as needed. Because you pay for the EC2 instances you use, you save money by launching instances when they are needed and terminating them when they aren't
# Load balancing
  - the process of distributing network traffic across multiple servers. This ensures no single server bears too much demand. By spreading the work evenly, load balancing improves application responsiveness. It also increases availability of applications and websites for users.
# Listener groups
  - Before you start using your Application Load Balancer, you must add one or more listeners. A listener is a process that checks for connection requests, using the protocol and port that you configure. The rules that you define for a listener determine how the load balancer routes requests to its registered targets.
# Launch Template for ASG
  - When you create an Auto Scaling group, you must specify the necessary information to configure the Amazon EC2 instances, the Availability Zones and VPC subnets for the instances, the desired capacity, and the minimum and maximum capacity limits.
  - o	To configure Amazon EC2 instances that are launched by your Auto Scaling group, you can specify a launch template or a launch configuration. 
# Launch Configuration vs Launch Template
  - Launch configuration is an instance configuration template that an Auto Scaling group uses to launch EC2 instances.  When you create a launch configuration, you specify information for the instances.  You can only specify one launch configuration for an Auto Scaling group at a time, and you can’t modify a launch configuration after you’ve created it.  Launch templates instead allow you to have multiple versions of a template
# Autoscaling policy options
  - With step scaling and simple scaling, you choose scaling metrics and threshold values for the CloudWatch alarms that invoke the scaling process. You also define how your Auto Scaling group should be scaled when a threshold is in breach for a specified number of evaluation periods

## Create launch template
  - open Amazon EC2 console
  - On navigation pane, under Instances, choose `Launch Templates`
  - Choose `Create launch template`
  - Name, description
  - check box 'provide guidance to help..'
  - add tag => name, value
  - browse AMI - click free tier, select ubuntu 18.04
  - Instance type - t2.micro
  - key pair - eng119
  - select existing security group
  - user data - script
    - #!/bin/bash
    - sudo apt-get update -y
    - sudo apt-get upgrade -y
    - sudo apt-get install nginx -y
    - sudo systemctl restart nginx -y
    - sudo systemctl enable nginx -y

## Create auto scaling group
  - sign into AWS management console
  - choose template
  - next
  - choose eu-west-1a, 1b, 1c
  - next
  - new load balancer
  - internet-facing
  - default routing - create target group
  - next
  - autoscaling: desired cap-2, min cap-2, max cap-3
  - target tracking scaling policy
  - next
  - next
  - add tags: Name, eng110-bens-asg-resources
  - next
  - create auto scaling group

## Monitoring

# create an SNS topic
  - open the Amazon SNS console 
  - On the Amazon SNS dashboard, under 'Common actions', choose `Create Topic`
  - choose `Standard`
  - in the 'Create new topic' dialog box, for 'Topic name', enter a name for the topic
  - Choose `Create Topic`
  - copy the 'Topic ARN' for the next task
# subscribe to an SNS topic
  - In the navigation pane, choose `Subscriptions, Create subscription`
  - In the 'Create subscription' dialog box, for 'Topic ARN', paste the topic ARN that you created in the previous task
  - for 'Protocol', choose `Email`
  - for 'Endpoint', enter an email address, then choose `Create subscription`
  - from your email application, open the message from AWS and confirm your subscription
# Set Cloudwatch alarms for Amazon SNS metrics
  - sign in to AWS Management Console and open the CloudWatch console
  - choose `Alarms`, then choose the `Create Alarm` button.  This launches the 'Create Alarm' wizard
  - be sure you're in the right region
  - scroll through the Amazon SNS metrics to locate the metric you want to place an alarm on.  Under Metrics choose `EC2` and `by auto scaling group` Select your choice and `Continue`
  - Fill in the Name, Description, Threshold, and Time values for the metric, and then choose `Continue`
  - Configure actions
    - select SNS topic
    - auto scaling action
  - Choose `Alarm` as the alarm state.
  - choose existing Amazon SNS topic or create new one
  - choose `Continue`
  - `Create Alarm`

### AWS Networking - VPC Architecture
![diagram](subnetsInVPC.png?raw=true "CIDR block")
- Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network that you've defined. This virtual network closely resembles a traditional network that you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS


# What is a subnet?

  - A subnet is a range of IP addresses in your VPC. You can launch AWS resources into a specified subnet. Use a public subnet for resources that must be connected to the internet, and a private subnet for resources that won't be connected to the internet.


# What is a CIDR block?
![diagram](cidr.png?raw=true "CIDR block")
  - CIDR blocks are groups of addresses that share the same prefix and contain the same number of bits.
  - CIDR, which stands for Classless Inter-Domain Routing, is an IP addressing scheme that improves the allocation of IP addresses. It replaces the old system based on classes A, B, and C. This scheme also helped greatly extend the life of IPv4 as well as slow the growth of routing tables.
  - CIDR IP addresses are composed of two sets of numbers. The network address is written as a prefix, like you would see a normal IP address (e.g. 192.255.255.255). The second part is the suffix which indicates how many bits are in the entire address (e.g. /12).

# Sub-mask
![diagram](tabel-CIDR.png?raw=true "sub-mask")
  - Every device has an IP address with two pieces: the client or host address and the server or network address. IP addresses are either configured by a DHCP server or manually configured (static IP addresses). The subnet mask splits the IP address into the host and network addresses, thereby defining which part of the IP address belongs to the device and which part belongs to the network.
  - A subnet mask is a 32-bit number created by setting host bits to all 0s and setting network bits to all 1s. In this way, the subnet mask separates the IP address into the network and host addresses.
  - The “255” address is always assigned to a broadcast address, and the “0” address is always assigned to a network address. Neither can be assigned to hosts, as they are reserved for these special purposes.

# IP-networking
  - An IP network is a communication network that uses Internet Protocol (IP) to send and receive messages between one or more computers. As one of the most commonly used global networks, an IP network is implemented in Internet networks, local area networks (LAN) and enterprise networks.
  - A private IP network allows data to be shared between connected devices securely, by enforcing password protected connectivity that allows only those devices in your office or home to access the IP network.

# Internet gateway
![diagram](internetGateway.png?raw=true "internet gateway")
  - An internet gateway is a horizontally scaled, redundant, and highly available VPC component that allows communication between your VPC and the internet. An internet gateway enables resources (like EC2 instances) in your public subnets to connect to the internet if the resource has a public IPv4 address or an IPv6 address.
  - Similarly, resources on the internet can initiate a connection to resources in your subnet using the public IPv4 address or IPv6 address. For example, an internet gateway enables you to connect to an EC2 instance in AWS using your local computer.
  - An internet gateway serves two purposes: to provide a target in your VPC route tables for internet-routable traffic, and to perform network address translation (NAT) for instances that have been assigned public IPv4 addresses.

# Routing table
![diagram](routingtable.svg?raw=true "routing table")
  - traffic light
  - A routing table contains the information necessary to forward a packet along the best path toward its destination. Each packet contains information about its origin and destination. Routing Table provides the device with instructions for sending the packet to the next hop on its route across the network.

# NACL (Network Access Control List)
![diagram](NACL.jpg?raw=true "Network Access Control List")
  - an added layer of security for your VPC that acts as a firewall for controlling traffic in and out of one or more subnets. You might set up network ACLs with rules similar to your security groups in order to add an additional layer of security to your VPC.
  - Security groups are tied to an instance whereas Network ACLs are tied to the subnet.
  - Security groups are stateful. This means any changes applied to an incoming rule will be automatically applied to the outgoing rule. e.g. If you allow an incoming port 80, the outgoing port 80 will be automatically opened.
  - Network ACLs are stateless. This means any changes applied to an incoming rule will not be applied to the outgoing rule. e.g. If you allow an incoming port 80, you would also need to apply the rule for outgoing traffic.

## Setting up a VPC
# Create VPC
  - Search for and select VPC
  - On the left hand side select 'Your VPCs'
  - Select the 'Create VPC' button
  - Select the 'VPC Only' option
  - Name/tags as per the naming convention
  - In IPv4 CIDR define the value as '10.0.0.0/16'
  - No IPv6
  - Set 'Tenancy' to default
  - Select 'Create VPC' - isolated space in Ireland - empty, the address has been validated

# Create Internet gateway
  - from the VCP dashboard
  - select 'Internet gateway' on the left hand side
  - select 'Create internet gateway'
  - Name/tags as per the naming convention
  - select 'Create internet gateway'

# Attach IG to VPC
  - From Internet gateway select your IG
  - From 'Actions' select 'attach to VPC'
  - Select your VPC
  - Select 'Attach internet gateway'

# Create subnet
  - Select 'Subnet' on left hand side
  - Select 'Create subnet'
  - Select your VPC
  - Name/tags as per the naming convention
  - Preference - no preference
  - In IPv4 CIDR define the value as '10.0.2.0/24'

# Create route table with subnet
  - From your Route select 'Routes' tab
  - Select 'Edit routes'
  - Select 'Add route'
    - Select 'Internet gateway' from dropdown list
    - define the value with '0.0.0.0/0' => Public use
  - Select 'Save changes'
  - Select the 'Subnet associations' tab
  - Select 'Edit subnet associations'
  - Select your subnet
  - Select 'Save association'

# Testing VPC
  - EC2 Dashboard > AMIs
  - Select your AMI
  - Launch instance from AMI
  - Go through usual process
    - in networking select your VPC
  - Connect to EC2
  - 

## Stateless vs Stateful
![diagram](statelessVSstateful.png?raw=true "Stateless vs Stateful")
  - Stateful services keep track of sessions or transactions and react differently to the same inputs based on that history. 
    - Stateful: Store additional information server-side, recording the state of the current transaction and waiting for the next instructions.
  - Stateless services rely on clients to maintain sessions and center around operations that manipulate resources, rather than the state.
    - Stateless: Store additional information client-side, passing along additional information with each step reminding  the server of the previous steps.  In practice, this is usually implemented using cookies or localStorage.
    - 
 