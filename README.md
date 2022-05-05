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
    - example => scp -i ~/.ssh/eng119.pem -r ~/Downloads/sg_application ubuntu@ec2-54-75-49-179.eu-west-1.compute.amazonaws.com:~/.
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



