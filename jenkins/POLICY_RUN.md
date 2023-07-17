## How to run cloud-governance container using jenkins slave

1. Create the policy.py file with the list of policy to run. 
    
    Below is the policy.py file to run one account.
```commandline
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
S3_BUCKET = os.environ['S3_BUCKET']
ES_HOST = os.environ['ES_HOST']
ES_PORT = os.environ['ES_PORT']
ES_INDEX = 'cloud-governance-index'

os.system(f'podman run --name cloud-governance -e policy="ec2_idle" -e AWS_ACESS_KEY_ID={AWS_ACCESS_KEY} -e AWS_SECRET_ACCESS_KEY_ID={AWS_SECRET_KEY} -e AWS_DEFAULT_REGION="us-east-2" -e es_host={ES_HOST} -e es_port={ES_PORT} -e es_index={ES_INDEX} -e policy_output="s3://{S3_BUCKET}/{LOGS}/{region}"  quay.io/ebattat/cloud-governance:latest')
os.system(f'podman run --name cloud-governance -e upload_data_es="upload_data_es"  -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e es_index="{es_index}" -e es_doc_type="{es_doc_type}" -e bucket="{S3_BUCKET}" -e policy="ec2_idle" -e AWS_DEFAULT_REGION="us-east-2" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_PERF}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest')


```

2. Now create a Jenkinsfile
```commandline
pipeline {
    options {
        disableConcurrentBuilds()
    }
    agent {
        docker {
            label 'cloud-governance-worker'
            image 'quay.io/athiru/centos-stream8-podman:latest'
            args  '-u root -v /etc/postfix/main.cf:/etc/postfix/main.cf --privileged'
        }
    }
    environment {
        AWS_ACCESS_KEY = credentials('AWS_ACCESS_KEY')
        AWS_SECRET_KEY = credentials('AWS_SECRET_KEY')
        S3_BUCKET = credentials('S3_BUCKET')
        ES_HOST = credentials('ES_HOST')
        ES_PORT = credentials('ES_PORT')
    }
    stages {
        stage('Checkout') { // Checkout (git clone ...) the projects repository
           steps {
                 checkout scm
           }
        }
        stage('Initial Cleanup') {
            steps {
                 sh '''if [[ "$(podman images -q quay.io/ebattat/cloud-governance 2> /dev/null)" != "" ]]; then podman rmi -f $(podman images -q quay.io/ebattat/cloud-governance 2> /dev/null); fi'''
            }
        }
        stage('Run Policies') {
            steps {
                 sh 'python3 policy.py'
            }
        }
        stage('Finalize Cleanup') {
            steps {
                 sh '''if [[ "$(podman images -q quay.io/ebattat/cloud-governance 2> /dev/null)" != "" ]]; then podman rmi -f $(podman images -q quay.io/ebattat/cloud-governance 2> /dev/null); fi'''
                 deleteDir()
            }
        }
    }
}

```

## How to update the jenkins credentials
1. Two ways to add the aws creds to jenkins
   1. Using the type secret text
      1. This method will help to add the individual account
   2. Using the jenkins secret file format
      1. This format will help to run multiple aws accounts using the single file.
      2. To use this format, need to store the file at secure place.
 