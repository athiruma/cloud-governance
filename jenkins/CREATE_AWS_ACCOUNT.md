# How to create a new user for cloud-governance
1. Create a IAM policy CloudGovernanceDeletePolicy
   1. Use [CloudGovernanceDeletePolicy.json](../iam/clouds/aws/CloudGovernanceDeletePolicy.json) to create the policy 
2. Create **cloud-governance-user** and add the above created policy.
3. Create s3 bucket to store policy results.


##  How to add AWS Creds to jenkins master.
1. Create a JSON file with below format and save it. [ Keep it safe ]
    ```commandline
    {
    "account1": {
       "AWS_ACCESS_KEY_ID": "acces_key",
       "AWS_SECRET_ACCESS_KEY" : "acees_secret",
       "BUCKET" : "bucket_name"
     },
    "account2": {
       "AWS_ACCESS_KEY_ID": "acces_key",
       "AWS_SECRET_ACCESS_KEY" : "acees_secret",
       "BUCKET" : "bucket_name"
     }
    } 
    ```
2. Login into the jenkins console.
3. Click on Manager Jenkins
4. Select Manage Credentials
5. Click on **System**, select the domain that your creds will be stored
   1. Add Credentials.
      1. Select **secret file**
      2. Give the Id
      3. Upload the json file
   2. Update Credentials
      1. Select the secret you want to upgrade.
      2. If it is a file secret.
      3. Upload the modified file.



