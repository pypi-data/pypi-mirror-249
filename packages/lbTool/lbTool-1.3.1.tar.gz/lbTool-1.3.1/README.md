## 模块介绍
### 通用模块 lbTool.Common  
内含：MD5加密、解析XML配置文件
### 数据库操作模块 lbTool.Db
依赖于pony包实现，以oracle连接串演示。目前支持（mysql/oracle）
```python
from lbTool.Db import *
# 依靠config.yml配置文件获取连接参数，可查看下方配置文件区域
# 创建连接 此方式可用可不用
# db_con = Database("oracle", user="user", password="pwd", dsn='host:port/sid')

# 获取连接 目前支持oracle/mysql
db_con = get_orm_con()
# 定义实体（不指定_table_则默认类名为表名，oracle模式名和表名需大写）
# max_len属性针对单个字段设置最大值，目前默认为1000，当字段值太长时，执行修改会报错
class Test(db_con.Entity):
    _table_ = ("模式名", "表名")
    id = PrimaryKey(int)
    name = Optional(str, max_len=2000)
    age = Optional(int)

# 获取封装操作实例 方式1
db = Db(db_con, is_create_table=False, show_sql=True)
# 查询
data = db.query(Test, id=1)

# 初始化Db方式操作 方式2
init_con(db_con)
# 根据主键查询
result = Test[1]
```
### 达梦数据库操作模块 lbTool.DmDb
依赖dmPython2.0实现
```python
from lbTool.DmDb import *

# 依靠config.yml配置文件获取连接参数，可查看下方配置文件区域
# 获取数据库连接1
# db = DmDatabase('ip:port', 'user', 'password')
# 获取数据库连接2
db = get_dm_con()

# 查询
sql = "select * from test where id=1"
data = db.query(sql)
sql1 = "select * from test where id=?"
data1 = db.query(sql1, 1)
sql2 = "select * from test where id=:id"
data2 = db.query(sql2, id=1)
# 查询列表
data_list = db.query_list(sql)
...
# 执行语句
up_sql = "update test set name=2"
db.execute(up_sql)
...
```
### AES/SM4加密模块 lbTool.EnCipher  
- AES  
```python
from lbTool.EnCipher import AesUtil

aes_key = "aes_key"
aes_iv = "aes_iv"
plaintext = "123"
aes_ciphertext = AesUtil.encrypt_cbc(aes_key, aes_iv, plaintext)
print("AES加密后===", aes_ciphertext)
aes_plaintext = AesUtil.decrypt_cbc(aes_key, aes_iv, aes_ciphertext)
print("AES解密后===", aes_plaintext)
```
- SM4
```python
from lbTool.EnCipher import Sm4Util

sm4_key = "sm4_key"
plaintext = "123"
sm4_ciphertext = Sm4Util.encrypt_ecb(sm4_key, plaintext)
print("SM4加密后===", sm4_ciphertext)
sm4_plaintext = Sm4Util.decrypt_ecb(sm4_key, sm4_ciphertext)
print("SM4解密后===", sm4_plaintext)
```
### 文件操作模块 lbTool.FileUtil
内含：数据流写文件，合并PDF，Word转PDF
### 日志操作模块 lbTool.Logging
默认在程序所在目录新建 Log/app_yyyymmdd.log 日志文件
```python
from lbTool.Logging import Logger

# 依靠log.yml配置文件获取参数，可查看下方配置文件区域
# 获取日志处理器 默认fileLogger文件输出,为空则控制台输出
logger = Logger()
logger.info("xxx")
```
## 配置文件
### 放在项目根路径config目录中 config.yml、log.yml
config/config.yml
<details>
<summary>点击查看具体代码</summary>

```yaml
database:
  driver: oracle
  host: localhost
  port: 1521
  user: user
  password: password
  db_name: orcl
  
#  driver: mysql
#  host: localhost
#  port: 3306
#  user: user
#  password: password
#  db_name: demo
```
</details>

config/log.yml
<details>
<summary>点击查看具体代码</summary>

```yaml
# DEBUG->INFO->WARNING->ERROR->CRITICAL
version: 1
disable_existing_loggers: False
formatters:
  simple:
    format: "%(asctime)s[%(levelname)s] - %(message)s"
  full:
    format: "%(asctime)s[%(levelname)s]%(filename)s->%(funcName)s|%(lineno)d - %(message)s"
#    datefmt: "%F %T"
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: full
  file_handler:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: simple
    filename: "app.log"
    maxBytes: 5242880
    backupCount: 1
    encoding: "utf8"
loggers:
  fileLogger:
    level: DEBUG
    handlers: [file_handler]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
  propagate: no
```
</details>