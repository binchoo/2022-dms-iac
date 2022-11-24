# SNS 연동 람다 만들기 w/ SAM

> 목표: AWS SAM CLI를 사용하여 CFN 스택을 생성하고 람다 소스코드 산출물을 클라우드 상에 배포할 수 있다.

AWS SAM으로 CloudFormation 스택을 만드는 과정을 간단하게 실습해 봅시다. 

SAM 템플릿 `template.yaml`은 하나의 SNS 토픽과, 이것을 이벤트 소스로 갖는 람다 하나를 명세합니다.

이전에 실습했던 `sns-lambda/sns-lambda-template.yaml`의 템플릿과 그 길이를 비교해 보세요. 훨씬 짧을 거예요. 

## 템플릿 살펴보기

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  sam-sns-lambda-template

  Example AWS SAM template to subscribe a lambda to an SNS topic.
Resources:
  SamPatientTopic:
    Type: AWS::SNS::Topic
    Properties:
      DisplayName: sam-patient-topic
      TopicName: sam-patient-topic

  SamPatientCheckoutFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.7 # 자신의 환경에 설치된 Python 버전에 맞추어 정의합니다. (3.6, 3.7, 3.8 중에서)
      CodeUri: .
      Handler: patient_checkout.handler # patient_checkout 모듈의 handler 함수를 지칭합니다.
      Events:
        NewPatient:
          Type: SNS
          Properties:
            Topic: !Ref SamPatientTopic
```

### Transform 영역

- 이 영역은 CloudFormation 템플릿을 처리할 때 사용할 매크로 시스템을 명시하는 장소입니다.

- 우리는 AWS SAM의 도움을 받을 것이기 때문에 `AWS::Serverless-2016-10-31`을 입력해 줍니다.

  https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html

### Resources 영역

#### SamPatientTopic

- 환자 정보를 송수신할 SNS 토픽을 명세합니다. 
- 구독자로 `SamPatientCheckoutFunction` 람다를 보유합니다.

#### SamPatientCheckoutFunction

- 환자를 체크아웃 처리하는 람다 함수를 표상합니다.
- `CodeUri`는 소스코드 혹은 소스코드 번들(.jar나 .zip)의 디렉토리 위치를 나타냅니다.
- `Handler`는 핸들러 함수의 위치를 나타냅니다.
  - 자바라면 `클래스명.메서드명`
  - 파이썬이라면 `모듈명.함수명`
- `Events`를 명시하여 이 람다를 구동할 수 있는 이벤트 소스를 설정할 수 있습니다. 
  - `SamPatientTopic`이 이벤트 소스로 등록되었습니다.

> AWS SAM의 간소화된 신택스를 사용하니 템플릿 파일의 길이가 무척 짧아졌습니다!

## 실습 과정

1. `template.yaml` 파일이 보이는 위치에서 cmd 혹은 bash 열기

2. 파이썬 버전 확인하기

   ```cmd
   python --version
   
   Python 3.7.4
   ```

3. `SamPatientCheckoutFunction`의 `Runtime` 속성을 자신의 파이썬 버전과 맞추기 (`3.7`, `3.8`, `3.9`에서)

4. `sam build` 실행하기

5. `sam deploy --guided` 실행하기

   - 스택 이름: `sam-sns-lambda`
   - 리전: `ap-northeast-2`
   - 나머지 설정 값들은 기본값을 써도 무방합니다.

6. AWS CloudFormation 콘솔> `sam-sns-lambda` 스택이 잘 생성되었는지 확인합니다.

7. 생성된 토픽의 ARN 주소 확인

   ```cmd
   aws sns list-topics
   ```

   ```json
   {
       "Topics": [
           {
               "TopicArn": "arn:aws:sns:ap-northeast-2:305992497901:sam-patient-topic"
           }
       ]
   }
   ```

8. 토픽을 향해 테스트용 환자 정보 발행

   ```
   aws sns publish --topic-arn arn:aws:sns:ap-northeast-2:305992497901:sam-patient-topic --message {\"name\":\"binchoo\"}
   ```

   - `--topic-arn`: `patient-topic`의 ARN 주소
   - `--message`: 환자 정보 JSON 문자열. 따옴표 이스케이프 합니다.

9. 람다 함수가 환자 정보 메시지에 반응했는지 알아보기 위해 로그를 확인

   AWS Lambda 콘솔> `SamatientCheckoutFunction`> **Monitoring** 탭> **View cloudwatch logs** 이동> 가장 최신의 로그 스트림 선택> 로그 출력 확인

   ```
   2022-11-23T13:05:57.945+09:00	START RequestId: 0b03cf54-44bf-4c62-af10-cdc45ce4c3c0 Version: $LATEST
   2022-11-23T13:05:57.946+09:00	[{'name': 'binchoo', 'status': 'checkout'}]
   2022-11-23T13:05:57.946+09:00	END RequestId: 0b03cf54-44bf-4c62-af10-cdc45ce4c3c0
   ```

## Q&A

> 람다의 이벤트 소스가 될 수 있는 것들을 알고 싶어요.

AWS::Severelss::Function 자원에 대한 AWS SAM 문서를 확인해 보시기 바랍니다. `Events` 속성을 작성하는 방법이 자세하게 나와있습니다.

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-resource-function-syntax

