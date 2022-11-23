import boto3
import uuid
from datetime import datetime
import json

# 콜드 스타트 시 초기화 할 자원들
dynamo = boto3.resource('dynamodb')
table = dynamo.Table('FunnelAnalysis')
mapping = {
    'www.instagram.com': 'INSTAGRAM',
    'twitter.com': 'TWITTER',
    'www.facebook.com': 'FACEBOOK'
}

def handler(event, context):
    '''
    이 람다 핸들러는, DynamoDB 테이블에 
    유입경로 로그 = (유저정보, referer 주소, 유입경로 라벨, 타임스탬프)를 생성합니다.
    '''
    print(event)
    userinfo = resolve_userinfo(event)
    referer = resolve_referer(event)
    funnel = resolve_funnel(mapping, referer)
    
    result = put_funnel_log(table, userinfo, referer, funnel)
    return {
        'statusCode': 302,
        'headers': {
            'Location': 'https://github.com/binchoo'
        },
        'body': json.dumps(result)
    }
    
def resolve_userinfo(event):
    return { # 임의로 반환
        'name': 'binchoo',
        'gender': 'MALE',
        'age': 26
    }

def resolve_referer(event):
    if 'referer' in event['headers']:
        return event['headers']['referer']
    elif 'Referer' in event['headers']:
        return event['headers']['Referer']
    return 'NONE'
    
# FIXED
def resolve_funnel(mapping, referer):
    '''
    mapping을 조회하여 referer에 대응하는 유입경로 라벨을 획득합니다.
    '''
    for k, v in mapping.items():
        if k in referer:
            return v
    return 'UNKNOWN'

def put_funnel_log(table, userinfo, referer, funnel):
    '''
    DynamoDB 테이블에 유입경로 로그를 저장합니다. 
    '''
    return table.put_item(
        Item={
            'uid': resolve_uuid(),
            'userinfo': userinfo,
            'referer': referer,
            'funnel': funnel,
            'timestamp': resolve_timestamp()
        }
    )
    
def resolve_uuid():
    return str(uuid.uuid4());
    
def resolve_timestamp():
    return str(datetime.now().timestamp())
