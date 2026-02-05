Youtube URL → 문장전처리 및 kafka, opensearch upload로 E2E 파이프라인

Docker를 이용하여 container로 구현하였으며, 모두 Streaming mode로 실행됩니다.

## **전체 아키텍쳐**

<img width="3305" height="1713" alt="image" src="https://github.com/user-attachments/assets/496e58b4-e70a-4b00-aa70-fd22c28186a7" />


전체 아키텍쳐는 위와 같습니다.

### **Network Architecture**


각 박스는 하나의 컨테이너를 지칭하며,  파란색/초록색/주황색을 각 docker-compose.yml 파일로 구성하였습니다.

Kafka broker들과 Spark 컨테이너 및 Fastapi, Nginx 컨테이너는 Shared-net이라는 내부 네트워크로 연결하여 `container_name:PORT`로 통신할 수 있었습니다.

Opensearch 컨테이너들은 독립적인 네트워크로 구성하여 Spark-app과 Search_contatiner에서 `host.docker.internal:PORT`로 통신할 수 있었습니다.

### WEB

WEB에서 `localhost`로 진입 후, 각 서비스를 선택하면 Nginx가 각 서비스에 맞는 fast-api container로 요청하여 접속합니다. Channel search는 유튜브 채널코드로 youtube script를 추출할 수 있으며, 이는 opensearch db에 저장됩니다. 스크립트 검색에서 단어를 검색하면, 제목에서 찾아 전처리된 스크립트를 불러옵니다.

<img width="5564" height="1538" alt="image" src="https://github.com/user-attachments/assets/f3dc48af-4505-4499-becf-67fcc5f5a640" />


### Pipeline

User-container는 코드를 input으로 받게 되면, spark-app container에 통신합니다.

spark app 컨테이너는 다음과 같은 디렉토리로 구성되어 있으며, spark코드로 kafka와 opensearch에 입력과 출력을 실행합니다. 채널코드를 입력하면, 스크립트를 로드하는 파일인 `throwing_json.py`가 selenium을 사용하면서, docker로 환경을 구성하는데 어려움을 겪어 local에서 돌리며 container에 마운트된 폴더에 파일을 전송하게 됩니다. 

<img width="3495" height="2250" alt="image" src="https://github.com/user-attachments/assets/31ca72d4-6a49-4a27-9e43-dccedb76bc2a" />



**spark-app** 컨테이너의 `main.py`가 실행되면, **spark** 및 전체 세션을 만들고, 모든 **query**를 **start**하게 됩니다. 그후`readStream`을 활용하여 마운트된 폴더를 감시하며 json파일이 추가되면, 그 파일을 Spark Dataframe으로 변환하여 Kafka의 **“analysis” topic**에 저장합니다. (그렇기 때문에 세션이 모두 시작되기 전에  `throwing_json.py`를 실행하게 되면, 너무 빨리 들어간 파일은 처리되지 못합니다.)

그 후 **Kafka의 메세지를 감지**하여 dataframe을 꺼내고, 가공하며 다시 **Kafka**의 또 다른 **Topic**과 **Opensearch**에 저장합니다. 여기서 가공은 모델 없이, **Kiwipiepy**와 룰베이스를 활용한 **오탈자 수정, 문장 분리, 불용어 처리**를 진행하였습니다.

Kiwipiepy를 docker로 띄우는 것은 Dockerfile에서 C언어 관련 시스템 패키지를 구성하여 해결하였습니다.

**Transfer**함수는 Kiwi 패키지를 적용시키기 위해, **F.pandas_udf**를 활용하여 실행시켰습니다.

**awaitTermination** 함수는 코드를 **Block** 시키기 때문에, 여러 query를 함께 추적할 수 없어서 **Timeout Trigger**를 걸어 stop 처리로 구현하였습니다. 

### Kafka

Kafka는 **Producer, Consumer**로 구성할 수 있지만, 의존성 파일을 이용해 spark 코드로 구현하였습니다.

`bitnami/kafka:3.7.0` 이미지를 기반으로 구축하였고, **Zookeeper**를 제거한 **kRaft mode**로 구성하였습니다. **broker00**을 제일 먼저 실행한 후, 정보를 broker00에만 전송하여 **Controller**가 되도록 했습니다.

Docker-compose파일에서 cluster_ID를 지정하고 docker volume을 만들어 컨테이너를 재시작하더라도 정보가 유지되도록 했습니다. 

Checkpoint를 지정하고 `kafka.bootstrap.servers` 와 컨테이너 이름으로 spark와 연결한 후 `writeStream`으로 기록하였습니다.

### Opensearch

Opensearch 또한 spark 코드로 구현하였습니다.

`opensearchproject/opensearch` 이미지를 기반으로 구축하였으며, node는 하나만 사용했습니다.  **HTTPS** 옵션은 off 하였습니다.

Opensearch도 `writeStream` 을 활용하여 데이터를 삽입하였고, search-container에서는 **opensearch Client**를 생성하고 query를 던져 데이터를 WEB에 출력하였습니다.

모든 dataframe 확인 및 디버깅은 **writeStream**의 **Console** 옵션을 활용했습니다.

---

<!-- AUTO-UPDATE:START -->
<!-- 이 섹션은 GitHub Actions에 의해 자동으로 업데이트됩니다 -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 176d8462bcd20f91b600d342bb176de847c6032c -->
