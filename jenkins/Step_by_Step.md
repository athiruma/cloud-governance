# Adding jenkins slave
1. Install java-11-jdk 
    ```commandline
    sudo yum install java-11-openjdk-devel
    ```
2. Install docker on [Fedora](https://docs.docker.com/engine/install/fedora/)
   ```commandline
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
    sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
    sudo systemctl start docker   
    ```
3. Create Jenkins user
   ```commandline
    useradd jenkins -U -s /bin/bash
   passwd jenkins
    ```
4. Add jenkins user to sudoers file
    ```
   $ vi /etc/sudoers
   jenkins ALL=(ALL) NOPASSWD: ALL
   ```
5. Giving permissions to jenkins user to run docker container
    ```
   sudo chown jenkins:jenkins /var/run/docker.sock
    ```

6. Run the cloud_governance_stack [ ElasticSearch, Kibana, Grafana]
    ```commandline
    # using docker-compose.yml
    # detached mode
    docker-compose -f [docker_compose_file_path](jenkins/docker-compose.yml) up -d
    # down the containers
    docker-compose -f [docker_compose_file_path](jenkins/docker-compose.yml) down
    ```

# Connect Jenkins slave to master
1. Goto Jenkins master.
2. Click on **Manage Jenkins**
3. CLick on **Manager Nodes and Clouds**
4. Click on New Node
5. Add details like node **Name**
6. Configure Node
   1. Remote root directory: **/home/jenkins**
   2. LaunchMethod: Launch agents via ssh
      1. Host: **hostname**
      2. Credentials: *select you creds from drop down*
         1. ADD CREDS: select kind as Username with password
      3. Host key Verification Strategy: _Non verifying Verification Strategy_
      4. Click on Advanced:
         1. Port: 22/
         2. JavaPath: /usr/bin/java
7. Click on save.
8. Check logs, if slave is connected to master or not.


# Managing elastic search indexes

1. ElasticSearch indexes, can be used for all the accounts
   1. Create one elasticsearch index for the policies. ex: **cloud-governance-ec2-index**
   2. Create other elasticsearch index for the cost reports. 
      So that we can differentiate two indexes data. 
      For managing all accounts the index should have the **global** keyword.
      ex:- **cloud-governance-global-cost-reports**