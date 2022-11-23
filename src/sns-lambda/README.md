# SNS 연동 람다 만들기

AWS CLI로 AWS CloudFormation 서비스를 사용해 봅시다.

CFN 템플릿 `sns-lambda-template.yaml`은 SNS 토픽 하나와, 이 토픽을 구독하는 람다를 명세합니다.

## 시나리오

가정하는 시나리오는 병원에서 환자가 퇴원하는 상황입니다. 

수납을 완료한 환자 정보를 시스템에 전파하여 환자 상태를 `checkout`으로 변경합니다.

데이터베이스가 없기 때문에 print 문으로 변경된 환자 엔터티를 로그로 출력하는 걸로 끝냅시다.

## 템플릿 살펴보기

이번 템플릿은 길기 때문에 두 부분으로 쪼개서 보겠습니다.

### 전반부: SNS 토픽 및 보안 설정

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  sns-lambda-template

  Example CloudFormation template to subscribe a lambda to an SNS topic.
Resources:
  PatientTopic:
    Type: AWS::SNS::Topic
    Properties:
      DisplayName: patient-topic
      TopicName: patient-topic
      Subscription:
        - Protocol: lambda
          Endpoint: !GetAtt PatientCheckoutFunction.Arn

  PatientTopicPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      Topics:
        - !Ref PatientTopic
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action: 'sns:Publish'
            Resource: !Ref PatientTopic
            Principal:
              AWS: '*'
            Condition:
              ArnLike:
                AWS:SourceArn: !Sub 'arn:aws:*:*:${AWS::AccountId}:*'
```

#### PatientTopic

- 환자 정보를 송수신할 SNS 토픽을 명세합니다. 

- 구독자로 `PatientCheckoutFunction` 람다를 보유합니다.

#### PatientTopicPolicy

- SNS 토픽에 붙이는 보안 정책 자원입니다.

- 현재 계정 내 IAM 유저인 경우에만, 이 SNS 토픽에 메시지를 발행할 수 있습니다.

  따라서 제3자에게 이 토픽의 ARN이 노출되어도 그 사람은 메시지를 발행할 수 없습니다.

  허나 한 가지, 내 IAM 유저가 자체적으로 sns:Publish 권한이 없다면 메시지 발행은 불가합니다.

### 후반부: 람다 및 보안 설정

```yaml
  PatientCheckoutFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.7
      Handler: index.handler
      Code:
        ZipFile: |
          import json
          def handler(event, context):
            patients = [{'name': json.loads(record['Sns']['Message'])['name'], 'status': 'checkout'} for record in event['Records']]
            print(patients)
      Role: !GetAtt PatientCheckoutFunctionExecutionRole.Arn

  PatientCheckoutFunctionInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      Action: 'lambda:InvokeFunction'
      FunctionName: !Ref PatientCheckoutFunction
      Principal: sns.amazonaws.com

  PatientCheckoutFunctionExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
            Action:
              - sts:AssumeRole
      Path: "/"
      Policies:
        - PolicyName: root
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:*
                Resource: arn:aws:logs:*:*:*
```

#### PatientCheckoutFunction

- 환자를 체크아웃 처리하는 람다 함수를 표상합니다.
- `Code` 속성과 `Role` 속성은 필수 속성입니다.
- 데모의 구조를 간단하게 하려고, 인라인 파이썬 코드를 지니도록 했습니다.
-  `PatientCheckoutFunctionExecutionRole`의 권능을 사용합니다.

#### PatientCheckoutFunctionInvokePermission

- Lambda 함수에 붙이는 보안 정책 자원입니다. 정책이 허용하는 인원이 함수를 실행시킬 수 있습니다.
- Amazon SNS 서비스가 이 함수를 호출하는 것을 허용했습니다.  이 함수는 `PatientTopic` 토픽의 구독자이므로,환자 정보가 도착시 SNS 서비스에서 함수를 호출시킬 수 있어야 하기 때문입니다.

#### PatientCheckoutFunctionExecutionRole

- Lambda 함수에 붙이는 IAM 역할입니다. 

- IAM 유저에게 IAM 퍼미션을 붙이듯이, AWS 서비스에 IAM 역할을 붙여줄 수 있습니다. 

- 이 IAM 역할은 람다 서비스가 착용 가능합니다. (모자나 완장으로 비유해서 생각하세요.)

- 이 역할을 착용한 람다는 CloudWatch Logs에 로그를 전송할 권능을 획득합니다.

  

> 보안 설정이 귀찮고 까다롭습니다. 
>
> 이 때, AWS SAM이 유용한 솔루션이 될 것입니다. SAM은 다음 실습에서 다룹니다. 

## 실습 과정

1. `sns-lambda-template.yaml` 파일이 보이는 위치에서 cmd 혹은 bash 열기

2. AWS CLI를 사용하여 CFN에 CFT 전송하기

   ```cmd
   aws cloudformation create-stack --stack-name sns-lambda --template-body file://sns-lambda-template.yaml --capabilities CAPABILITY_IAM
   ```

   - `--stack-name`: sns-lambda
   - `--template-body`: file://sns-lambda-template.yaml
   - `--capabilities`: CAPABILITY_IAM (CFN이 IAM 자원을 만드는 걸 허락한다는 뜻)

3. CFN 스택이 다 만들어질 때까지 대기

4. 생성된 토픽의 ARN 주소 확인

   ```cmd
   aws sns list-topics
   ```

   ```json
   {
       "Topics": [
           {
               "TopicArn": "arn:aws:sns:ap-northeast-2:305992497901:patient-topic"
           }
       ]
   }
   ```

5. 토픽을 향해 테스트용 환자 정보 발행

   ```
   aws sns publish --topic-arn arn:aws:sns:ap-northeast-2:305992497901:patient-topic --message {\"name\":\"binchoo\"}
   ```

   - `--topic-arn`: `patient-topic`의 ARN 주소
   - `--message`: 환자 정보 JSON 문자열. 따옴표 이스케이프 합니다.

6. 람다 함수가 환자 정보 메시지에 반응했는지 알아보기 위해 로그를 확인

   AWS Lambda 콘솔> `PatientCheckoutFunction`> **Monitoring** 탭> **View cloudwatch logs** 이동> 가장 최신의 로그 스트림 선택> 로그 출력 확인

   ```
   2022-11-23T13:05:57.945+09:00	START RequestId: 0b03cf54-44bf-4c62-af10-cdc45ce4c3c0 Version: $LATEST
   2022-11-23T13:05:57.946+09:00	[{'name': 'binchoo', 'status': 'checkout'}]
   2022-11-23T13:05:57.946+09:00	END RequestId: 0b03cf54-44bf-4c62-af10-cdc45ce4c3c0
   ```

## Q&A

> aws cloudformation 혹은 aws sns 처럼 AWS CLI의 사용법은 어떻게 알 수 있나요?

당연히 공식 문서를 참고하시면 됩니다. CLI 공식 문서를 링크로 첨부드리겠습니다. 

각 서비스 별로 사용가능한 API를 매우 자세하게 알 수 있습니다.

- AWS CLI 문서: https://docs.aws.amazon.com/cli/latest/index.html
- AWS CloudFormation CLI 문서: https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html
- AWS SNS CLI 문서: https://docs.aws.amazon.com/cli/latest/reference/sns/index.html

> 각 AWS의 자원에 필요한 보안 설정을 어떻게 알 수 있나요?

보안은 AWS에서 매우 중요하게 다뤄집니다. 보안 설정을 하지 않으면 해당 자원을 누릴 수 없는 경우가 왕왕 있습니다.

각 자원의 공식 문서에서 Security, Permission, Access Control 등의 단어가 있는 섹션을 참조하십시오. 자원을 이용하기 위해 어떤 보안 정책이나 보안 자원이 추가로 붙어야 하는지 알 수 있습니다.

- AWS Lambda Permissions> Lambda Execution Role: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html

- AWS Lambda Permissions> Resource-based policies: https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html

- AWS SNS Topic Access Control: https://docs.aws.amazon.com/sns/latest/dg/sns-authentication-and-access-control.html#access-control

  