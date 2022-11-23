import boto3
from boto3.dynamodb.conditions import Key
import json

# 콜드 스타트 시 초기화 할 자원들
dynamo = boto3.resource('dynamodb')
table = dynamo.Table('FunnelAnalysis')

def handler(event, context):
    '''
    이 람다 핸들러를 호출할 때의 URL 경로를 토대로
    DynamoDB에서 유입경로 로그를 쿼리하고, 그 갯수를 세어 반환합니다.
    '''
    print(event)
    funnel = event['path'].upper()
    
    result = table.query(
        IndexName='FunnelQueryingIndex', 
        Select='COUNT', 
        KeyConditionExpression=Key('funnel').eq(funnel))
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'funnel': funnel,
            'count': result['Count']
        })
    }
