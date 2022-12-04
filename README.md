0. 필수요소

OS: Ubuntu 20.04 LTS
Dependencies:
Python 3.8.10
Apache 2.4.11
MariaDB 15.1

pip 다운로드목록 (Python Framework Requirement):
>> /home/kingbus/requirements.txt (pip freeze)

apache2 모듈 목록 (Loaded Modules) :
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



1. Channels 관련
모든 Channels관련 async(비동기) 응답은 daphne service가 담당하여 처리중.

/home/kingbus/ 내부에있는 kingbuschat/ 의 독자적인 프로젝트가 또 존재하는데,
그곳에서 asgi application인 daphne service가 돌아가며 처리하게끔 되어있고
모든 설정값은 /home/kingbus 의 프로젝트와 연동되어있음 (models, secret_key 등)

구조상 모든 async 응답은 ws(웹소켓) 가 유일, 고로 모든 http응답은 우선적으로 apache가 처리하며 ws요청은 rewrite engine을 통해 ws프로토콜로 daphne의 응답포트에 터널링 해줌
값 설정은 /etc/apache2/sites-enabled/000-default.conf 참고.


2. DB 관련
DB자체보다는 ORM관련임.
ORM남용시 쿼리 다수발생하는 고질적인 문제를 방지하기위해, runserver로 인한 debug모드 작동시, 터미널에 쿼리발생로그를 남기게 해놓음. 해당로그 참고하여 쿼리셋 발생 빈도를 줄일것. (작성날짜기준으로 최적화 완료)


3. 보안 관련
TODO:
Linux 자체의 보안 강화 (미사용 포트 차단 등)
django CORS, csrf
db 포트변경?
secret_key 관리 (모든 secret_key 또는 암호들은 secret_key.json 에 보관중. 보안대책 강구 요망)


4. Redis 관련
docker에서 독자적으로 돌아감. redis자체는 설정할필요없으나 추후 서비스를위해 자동실행되게 만들어야함 (sudo service)
실행방법은 instructions.txt 참고.
daphne에서만 사용. (비동기처리)
관련 튜토리얼 : 링크


99. 
home/kingbus/instructions.txt 에 기본적인 명령어들이있으니 참고할것.
프로젝트내부의 TODO, FIXME 또한 참고할것
