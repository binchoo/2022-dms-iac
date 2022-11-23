# S3 버킷 만들기

AWS CloudFormation을 간단하게 실습해 봅시다. 

CFN 템플릿 `s3-bucket-template.yaml`은 S3 버킷 자원 한 개를 명세합니다. 

## 템플릿 살펴보기

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Parameters:
  InputBucketName:
    Type: String
    Default: demo-bucket
    Description: Input the name of a bucket you are creating.
    AllowedPattern: "[a-z0-9\\-]+"
    ConstraintDescription: NO UPPERCASE FOR A BUCKET NAME.
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::Region}-${AWS::AccountId}-${InputBucketName}"
Outputs:
  BucketName:
    Value: !Ref S3Bucket
    Description: Name of the sample Amazon S3 bucket.
```

### Parameters 영역

- 버킷의 이름을 외부에서 주입받기 위해 `InputBucketName` 이라는 파라미터를 선언했습니다. 템플릿을 제출하는 시점에 이 값이 반드시 명세되어야 합니다.
- 버킷의 이름에는 대문자 알파벳이 오지 않아야 합니다. 따라서 입력 값 형식이 제한되었다는 점도 확인하세요.

### Resources 영역

- 버킷 자원을 하나 명세합니다. 「논리적 자원명」은 `S3Bucket`입니다.
- 버킷의 이름은 리전 명, 계정 번호, 파라미터로 입력 받은 버킷 이름의 접합으로 구성됩니다.

### Outputs 영역

- 생성된 「버킷의 이름」을 반환하도록 출력이 하나 정의됩니다. 논리적 자원명과 버킷 이름은 다릅니다. 

## 실습 과정

1. AWS CloudFormation 콘솔> **Create Stack**> With new resources
2. Prerequisite - Prepare template> **Template is ready** 선택
3. Specify template> **Upload a template file** 선택> **Choose file** 클릭
4. `s3-bucket-template.yaml` 템플릿 업로드
5. Stack name> **Stack Name**: `s3-bucket`
6. Parameters> **InputBucketName:** 여러분이 자유롭게 설정
7. **Next**를 누르며 끝까지 진행> 스택 생성.

## Q&A

> `!Ref S3Bucket`이 반환하는 값이 버킷 이름이라는 걸 어찌 알 수 있나요? 

당연히 [공식 문서](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#aws-properties-s3-bucket-return-values)를 보셔야 합니다. CFN 공식 문서는 각 자원 별 `!Ref` 내재 함수의 반환값과, `!GetAtt`로 참조할 수 있는 속성에 대해 설명하고 있습니다.  AWS를 공부할 때는 인터넷에 나돌아 다니는 글을 지양하고, 반드시 공식 자료를 함께 체크하세요. 

