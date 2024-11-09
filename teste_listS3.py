import boto3
def lambda_handler(event, context):
 
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::266549158321:role/role-secundary-describe-rds",
        RoleSessionName="cross_acct_lambda"
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    clients3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    try:
        # Lista todos os buckets
        response = clients3.list_buckets()
        
        # Extrai apenas os nomes dos buckets
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        print(f"Buckets encontrados: {bucket_names}")
        return {
            'statusCode': 200,
            'body': bucket_names
        }

    except Exception as e:
        print(f"Erro ao listar os buckets: {e}")
        return {
            'statusCode': 500,
            'body': f"Erro ao listar os buckets: {e}"
        }

    return "Hello from Lambda"