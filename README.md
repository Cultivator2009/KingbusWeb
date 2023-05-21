## Django REST Framework (DRF) + React + MariaDB + Apache


해당 프로젝트는 창업 동아리 활동의 일환으로써, 배달의 민족과 유사한 사용자+실무자+관리자 3축 체제에서의 사용자 사용 목적에 기안한 전세버스 대절 플랫폼을 개발함과 동시에, 다른 서비스에서의 연동, 모바일 앱 환경 또한 목표를 둔 중규모 프로젝트입니다.

- 기반 :
서비스는 기본적으로 Django + Apache + MariaDB 를 기반으로 구축하였으며, API 사용 목적에 맞게끔 Django REST Framework를 활용하여, RESTful 한 API 구축을 장고에서 구현할 수 있게끔 하는 프레임워크를 사용하였습니다.

- RESTful API :
모든 API 응답은 JSON 형식으로 Serialization되어 넘겨주게 되어 있으며, 해당 플랫폼에선 모두 React가 처리하였습니다. React 프론트엔드 개발은 다른 팀원이 도맡아 하였기 때문에, POSTMAN+Discord를 활용한 API URI 협업 또한 장시간 진행하였습니다.   
각 기능별로 HTTP 응답코드, 메소드의 목적에 맞춰 최대한 체계적으로 API를 구현했습니다.

- JWT :
아직 프로젝트 프로토타입 단계이지만, 최소한의 프로젝트 보안 구성을 위해 JWT (drf-simplejwt) 를 사용하였고, 쿠키에 저장되는 AccessToken 주기를 짧게 유지하고 RefreshToken을 React 내부 변수로 안전하게 넘겨주는 식으로 구현하였습니다.
Token의 내용은 User 명과 같은 간결하게 필요한 요소만 골라 넣었고, 암호화는 RSA256 암호화 방식을 Django Secret 키와 연계하여 진행하였습니다.   
   
   
---------

해당 프로젝트는 개인적인 사정으로 인하여 팀원과의 모든 작업이 중단된 상태입니다.   
포트폴리오 용도로 Public으로 개방합니다.  

추후 개발 인계 혹은 참고용으로 인수인계를 남겨둘테니 참고 하시기 바랍니다.

---------

# 인수인계

### 0. 필수요소

- 기반 시스템   

```
OS:
    Ubuntu 20.04 LTS
Dependencies:
    Python 3.8.10
    Apache 2.4.11
    MariaDB 15.1
```

- pip 다운로드목록 (Python Framework Requirement):   
`pip freeze > /home/kingbus/requirements.txt`

- apache2 모듈 목록 (Loaded Modules) :   
```
 core_module (static)
 so_module (static)
 watchdog_module (static)
 http_module (static)
 log_config_module (static)
 logio_module (static)
 version_module (static)
 unixd_module (static)
 access_compat_module (shared)
 alias_module (shared)
 auth_basic_module (shared)
 authn_core_module (shared)
 authn_file_module (shared)
 authz_core_module (shared)
 authz_host_module (shared)
 authz_user_module (shared)
 autoindex_module (shared)
 deflate_module (shared)
 dir_module (shared)
 env_module (shared)
 filter_module (shared)
 headers_module (shared)
 mime_module (shared)
 mpm_event_module (shared)
 negotiation_module (shared)
 proxy_module (shared)
 proxy_ajp_module (shared)
 proxy_balancer_module (shared)
 proxy_connect_module (shared)
 proxy_html_module (shared)
 proxy_http_module (shared)
 proxy_wstunnel_module (shared)
 reqtimeout_module (shared)
 rewrite_module (shared)
 setenvif_module (shared)
 slotmem_shm_module (shared)
 status_module (shared)
 wsgi_module (shared)
 xml2enc_module (shared)
```


### 1. Channels 관련
모든 Channels관련 async(비동기) 응답은 daphne service가 담당하여 처리중.   
   
/home/kingbus/ 내부에있는 kingbuschat/ 의 독자적인 프로젝트가 또 존재하는데,   
그곳에서 asgi application인 daphne service가 돌아가며 처리하게끔 되어있고   
모든 설정값은 /home/kingbus 의 프로젝트와 연동되어있음 (models, secret_key 등)   
   
구조상 모든 async 응답은 ws(웹소켓) 가 유일, 고로 모든 http응답은 우선적으로 apache가 처리하며 ws요청은 rewrite engine을 통해 ws프로토콜로 daphne의 응답포트에 터널링 해줌   
값 설정은 /etc/apache2/sites-enabled/000-default.conf 참고.   


### 2. DB 관련
DB자체보다는 ORM관련임.   
ORM남용시 쿼리 다수발생하는 고질적인 문제를 방지하기위해, runserver로 인한 debug모드 작동시, 터미널에 쿼리발생로그를 남기게 해놓음. 해당로그 참고하여 쿼리셋 발생 빈도를 줄일것. (작성날짜기준으로 최적화 완료)   


### 3. 보안 관련
TODO:   
Linux 자체의 보안 강화 (미사용 포트 차단 등)   
django CORS, csrf   
db 포트변경?   
secret_key 관리 (모든 secret_key 또는 암호들은 secret_key.json 에 보관중. 보안대책 강구 요망)   


### 4. Redis 관련
docker에서 독자적으로 돌아감. redis자체는 설정할필요없으나 추후 서비스를위해 자동실행되게 만들어야함 (sudo service)   
실행방법은 instructions.txt 참고.   
daphne에서만 사용. (비동기처리)   
관련 튜토리얼 : [링크](https://www.youtube.com/watch?v=wLwu1NqU1rE)   


### 99. 
/home/kingbus/instructions.txt 에 기본적인 명령어들이있으니 참고할것.   
프로젝트내부의 TODO, FIXME 또한 참고할것   
