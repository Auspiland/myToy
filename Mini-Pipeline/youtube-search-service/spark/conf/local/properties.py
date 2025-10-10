QUERYTIMEOUT = 70

# History
EVENTLOG_DIR = ""

# Storage
WAREHOUSE_DIR = ""

NFS_MOUNT_PATH = ""
NFS_REAL_PATH = ""

## 이하 전부 NodePort 로 구성 
## -------------------------------
# Opensearch
ES_NODES = "172.16.16.172:30200" 

# Kafka

HADOOP_HA_DEFAULTFS = None # NN 단일구성 상태

# Hive & Catalog DB settings
HIVE_METASTORE_URIS = ""
DEFAULT_DATABASE = "default"

# HDFS current active NameNode & Legacy support 
#from cep_common.hdfs_utils import get_active_hdfs_host as hdfs
# Active NameNode on Spark init.
#active_nn = hdfs(["t3q-hdfs.search.svc.cluster.local"]) # svc name
active_nn = ""
# Hadoop
HADOOP_NODE = f""
HADOOP_WEBHDFS = f""
HADOOP_FS_DEFAULTFS = f""
