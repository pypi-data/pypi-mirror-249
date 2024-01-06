OlapSDK
===============
module mining data in OLAP

Prepare
Đảm bảo rằng image phải được cài đặt mysql-devel, trong Dockerfile thêm dòng sau trước khi install requirements

```
RUN yum install -y gcc
RUN yum install -y python38-devel mysql-devel
RUN ln -s /usr/include/python3.8 /usr/local/include/python3.8
```

Usage

* Get profile by id
```python
from mobio.libs.olap.mining_warehouse.profiling.mysql_dialect.profiling_dialect import ProfilingDialect

profile_data = ProfilingDialect(olap_uri="uri").get_profile_by_criteria(merchant_id="merchant_id", profile_id="profile_id", lst_criteria=["cri_merchant_id", "cri_profile_id", "cri_name"])
print(profile_data)
```

Release notes:
* 0.1.12 (2024-01-06):
  * support HA
* 0.1.11 (2023-12-07):
  * port libs
* 0.1.4 (2023-11-28):
  * fix validate column name, support dynamic field with prefix
* 0.1.3 (2023-11-27):
  * remove m-utilities, chỉ dependence m-logging để support python3.8
* 0.1.2 (2023-11-27):
  * alter table
* 0.1.1 (2023-11-24):
  * support lấy profile by id, hỗ trợ việc masking data


## Note prepare from MySQL-Client
### Linux
Note that this is a basic step. I can not support complete step for build for all environment. If you can see some error, you should fix it by yourself, or ask for support in some user forum. Don't file a issue on the issue tracker.

You may need to install the Python 3 and MySQL development headers and libraries like so:

<code>$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential </code># Debian / Ubuntu

<code>% sudo yum install python3-devel mysql-devel</code> # Red Hat / CentOS

Then you can install mysqlclient via pip now:

<code>$ pip install mysqlclient</code>