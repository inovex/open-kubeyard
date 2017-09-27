# Zeppelin

## Mount Notebooks from AWS:

Set the variables:

* awsAccessKeyId
* awsSecretAccessKey
* zeppelinNotebookS3Bucket
* zeppelinNotebookS3User
  
To protect your credentials use: 
 
 ``` sh
 echo -n "<your-awsAccessKeyId>" | base64
 echo -n "<your-awsSecretAccessKey>" | base64
 ```
 
## Use Local Notebooks

Dont set the Storage variable in Values
