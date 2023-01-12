import boto3
import json

# Specify the EndPoint
ENDPOINT_NAME = 'sagemaker-xgboost-2023-01-09-08-07-05-195'

# Initialize the Sagemaker Client
runtime = boto3.client('runtime.sagemaker',
    region_name='us-east-1',
    aws_access_key_id='ASIA4JKKWWZPRCMQZ4GS',
    aws_secret_access_key='TY8h6F/yQpqZ0gtN1WxXrdYcfhsEyM0Bn4vcPg2w',
    aws_session_token='FwoGZXIvYXdzECkaDLxX3yrgkQ5ao6FaOCK+AezpomLRthSNq/tQixkJYpUCMhY15zPuugKrq+1yXkzNZKKvyVY/MFOn9SMSuo9r/SrH073T+xZVNI1+0VjAj/ghMCZN6272zwRaFrbHLJyP2OhgM9O1Hc83qauixf2pRbPIr6jzYtsDCypthw5zFUlZdZBMPX1muSJZdn3AxWce1Ij6sAx0nQHETmNPWHrrxXNzsXbKSCy7jh5AFPAhmolqwEmfwbrUT2mI5FbQyPrxbLgt5ENifwVlx3pR8aEokYfvnQYyLTE/q4EfP3zdBfbGWYNcTCbrNr+Qds9E3G80TdkzB6h688VgsX8xWm+HAgKuFw=='
)

print(vars(runtime))


data = {'data': '1, 0, 0.0, 0.0, 5849, 0.0, 0.0, 360.6, 1.0, 2'}
payload = data['data']
print(payload)

#Invoke the Rede EndPoint
response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                    ContentType='text/csv',
                                    Body=payload)

print(response) 
result = json.loads(response["Body"].read().decode())
print(result*100)