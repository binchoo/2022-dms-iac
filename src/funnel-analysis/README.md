# CFN & SAM 실습

> 목표: 
> - 아키텍처 뷰를 참고하며 CloudFormation 템플릿을 작성할 수 있다. 
> - 자원을 명세하는 방법을 AWS 공식 문서를 참고하여 알아낼 수 있다. 
> - AWS 콘솔이나 CLI 사용 경험에 비추어, 배치해야만 하는 자원을 유추할 수 있다.
> - AWS SAM CLI를 통해 CFN 스택을 만들고, 람다 소스코드 산출물을 업로드하여 클라우드 상에 배포할 수 있다.

## 유입경로 파이프라인

### 템플릿 처음부터 작성하기

#### AWSTemplateFormatVersion 영역

#### Transform 영역

#### Resources 영역

1. `FunnelAnalysisTable` 
   - 속성 명세하기
   - 보조 인덱스 명세하기

2. `FunnelLoggingFunction`
   - 간단한 신택스로 `FunnelAPI`의 `GET /home` 경로와 연동하기

3. `FunnelQueryingFunction`
   - API GW와 프록시 통합을 맺을 떄는, 간단한 신택스가 없습니다. 
   - 따라서 이후 필요한 모든 자원을 생성할 것입니다.

4. `FunnelApi`
5. `FunnelQueryRoute` 
   - `GET /funnel/{proxy+"`를 표상하는 API 경로를 명세하기

6. `FunnelQueryIntegration`
   - `FunnelQueryingFunction`과 `FunnelQueryRoute`를 이어줄 통합

- `FunnelQueryingFunctionInvokePermission`

  -  `FunnelApi`가 `FunnelQueryingFunction`을 호출할 수 있도록 보안 정책 수립.

### SAM Build & Deploy
