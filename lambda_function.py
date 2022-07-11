import json
import boto3
import datetime

def revert_cis_1_20(event):
    s3 = boto3.client('s3')
    bucketName = event['detail']['requestParameters']['bucketName']
    try:
            response = s3.get_public_access_block(
                Bucket=bucketName
            )
            if( response['PublicAccessBlockConfiguration']):
                
                status1 = response['PublicAccessBlockConfiguration']['BlockPublicAcls'] \
                &response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] \
                &response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] \
                &response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
                
                if not status1:
                    response1 = s3.put_public_access_block(
                                Bucket=bucketName,
                                PublicAccessBlockConfiguration={
                                'BlockPublicAcls': True,
                                'IgnorePublicAcls': True,
                                'BlockPublicPolicy': True,
                                'RestrictPublicBuckets': True})
    except Exception as e:
        print(str(e))
    
def lambda_handler(event, context):
    if event['detail']['eventName'] == "PutBucketPublicAccessBlock":
        revert_cis_1_20(event)
    return{
        "statusCode": "200"
    }
