# 2022-dms-iac

2022학년도 2학기 건국대학교차세대분산시스템 

Infrastructura as a Code 

AWS CloudFormation & SAM CLI 실습 수업

## 실습 목록

- [**s3-bucket**](https://github.com/binchoo/2022-dms-iac/tree/master/src/s3-bucket)

  ![](https://img.shields.io/badge/s3--06A0CE?logo=amazons3&color=569A31&labelColor=FFFFFF) 

  AWS CFN 서비스를 간단히 데모합니다. AWS 콘솔에서 CFT를 제출하여 CFN 스택을 생성하고 하나의 S3 버킷을 배치해 봅니다. 더불어, 파라미터 영역 및 출력 영역의 역할을 확인해 봅니다.

- [**sns-lambda**](https://github.com/binchoo/2022-dms-iac/tree/master/src/sns-lambda)

  ![](https://img.shields.io/badge/lambda--06A0CE?logo=awslambda&color=FF9900&labelColor=FFFFFF) ![](https://img.shields.io/badge/sns--06A0CE?logo=amazonsqs&color=FF4F8B&labelColor=FFFFFF)

  AWS CFN CLI를 사용하여 스택을 생성하고, SNS 토픽을 이벤트 소스로 하는 람다 하나를 배치해 봅니다.

- [**sam-sns-lambda**](https://github.com/binchoo/2022-dms-iac/tree/master/src/sam-sns-lambda)

  ![](https://img.shields.io/badge/aws%20sam--06A0CE?logo=amazonaws&color=4053D6&labelColor=FFFFFF&logoColor=4053D6) ![](https://img.shields.io/badge/lambda--06A0CE?logo=awslambda&color=FF9900&labelColor=FFFFFF) ![](https://img.shields.io/badge/sns--06A0CE?logo=amazonsqs&color=FF4F8B&labelColor=FFFFFF) 

  간소화 된 신택스의 CFT와 AWS SAM CLI를 활용합니다.**sns-lambda**와 동일한 아키텍처를 구성할 뿐만 아니라, 로컬 코드베이스의 람다 코드를 클라우드 상으로 배포하는 과정을 알아봅니다.

- [**funnel-analysis**](https://github.com/binchoo/2022-dms-iac/tree/master/src/funnel-analysis)

  ![](https://img.shields.io/badge/aws%20sam--06A0CE?logo=amazonaws&color=4053D6&labelColor=FFFFFF&logoColor=4053D6) ![](https://img.shields.io/badge/dynamodb--06A0CE?logo=amazondynamodb&color=4053D6&labelColor=FFFFFF&logoColor=4053D6)![](https://img.shields.io/badge/lambda--06A0CE?logo=awslambda&color=FF9900&labelColor=FFFFFF) ![](https://img.shields.io/badge/event%20bridge--06A0CE?logo=amazonapigateway&color=FF4F8B&labelColor=FFFFFF)
  
  유입경로 분석 서버리스 파이프라인의 청사진을 작성하여 클라우드 위에 편리하게 구축해 봅시다.

## 사전 준비물

1. [AWS SAM CLI](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

   ※ AWS SAM CLI는 [AWS CLI](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions)에 의존성이 있습니다. 미리 설치하세요.

2. 자신의 IAM User가 세팅된 CLI 환경

   ※ [aws configure 명령어](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-files.html)

3. Python 3.7, 3.8, 3.9 중 하나가 세팅된 환경

   ※ [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#) 등을 활용하세요.

4. YAML 작성에 도움이 되는 에디터

## 도움이 될 모든 자료

남들이 떠먹여 주지 않는 기술 주제를 언젠가 마주하게 됩니다. 이런 상황에 대비하려면 스스로의 리서치 방식을 정립하세요.

알 수 없는 출처의 글에 의존하면, 단기간에 궁금증을 해소하거나 저자의 주관적인 인사이트를 공유 받는 장점이 있습니다. 그러다가 여러 번 데이다 보면, 원본 내용을 크로스 체크하는 부수적인 시간을 갖게 되실 겁니다.

처음부터 공신력 있는 정보 소스를 일관적으로 이용하는 것을 추천합니다. 

### AWS CLI Command Reference

https://docs.aws.amazon.com/cli/latest/index.html

### CFN Template Anatomy

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html

### CFN Resource and Property Reference

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

- [s3 bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
- [sns topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)
- [sns topic policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html)
- [lambda function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html)
- [lambda permission](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html)
- [serverless function](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/sam-resource-function.html)
- [dynamodb table](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html)
- [apigateway version2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html)
- [serverless httpapi](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-httpapi.html)

### AWS SAM Resource and Property Reference

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-resources-and-properties.html

### AWS SAM CLI Command Reference

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html

- [sam build](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html)
- [sam package](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html)
- [sam deploy](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)

### AWS SAM CLI Github Repository

https://github.com/aws/aws-sam-cli

Sam CLI를 다루는 저장소입니다.

### AWS SAM Github Repository

https://github.com/aws/serverless-application-model

Sam Transform 매크로를 다루는 저장소입니다.

### AWS SAM Java REST Application Example

https://github.com/aws-samples/aws-sam-java-rest