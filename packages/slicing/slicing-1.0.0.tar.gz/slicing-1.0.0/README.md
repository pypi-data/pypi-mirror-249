# 支持的文件格式
 - gz
 - zip
 - sql

# 分割 SQL
## 调用方式
```python
from pathlib import Path

# absolute_file_path 读取文件的绝对路径
# absolute_out_put_folder 输出的文件夹的绝对路径
# 返回的 任务ID
task_id = SliceFactory.slice(absolute_file_path=Path("D:\\workspace\\Resources\\eclinical_edc_prod_21_20230630025243.sql.gz"), 
                   absolute_out_put_folder=Path("YYYYY"))

```
### 输出的结果
![img.png](img.png)

|                                  | | 
|----------------------------------| ----- |
| YYYYY                            | 输出的文件夹 |
| cdfe5a8a9811459d9b0a940aa86abd89 | 根据任务 ID 生成的对应文件夹 |
| CREATE                           | 创建 表单的 SQL 语句 |
| INSERT| 插入 表单数据的 SQL 语句 |
| file_list.json | 生成的文件信息 |

SQL 文件名的格式:{表名}-{uuid}

# 获取 SQL 文件信息

```python
# where SQL 文件夹的绝对路径
file_list = FileInfoList(
        where=Path("D:\\aws\\eclinical40_auto_testing\\slicing\\src\\slicing\\XXXX\\89f20cdac717425091fb0fb9220481fe"))
```
## 文件信息
|          |                             |
|----------|-----------------------------|
| sql_type | CREATE(创建表单) 或 INSERT(插入数据) |
 | name     | 文件的全名 {table}-{id}          |
| table    | 表名                          |
| id       | uuid                        |

## 获取表名
```python
file_list = FileInfoList(where="文件夹的绝对路径")

# FileInfoList.CREATE_LIST  创建表单S表名
# FileInfoList.INSERT_LIST  插入表单数据的表名
# FileInfoList.ALL_LIST     所有创建表单和插入表单数据的表名的交集
file_list.table(mode=FileInfoList.CREATE_LIST)

```

## 根据表名获取 文件信息
```python
file_list = FileInfoList(where="文件夹的绝对路径")

# FileInfoList.CREATE_LIST  创建表单的SQL
# FileInfoList.INSERT_LIST  插入表单数据的SQL
# FileInfoList.ALL_LIST     所有创建表单和插入表单数据的所有SQL
# 返回的是一个列表
sqls = file_list.find("eclinical_crf_item", mode=FileInfoList.ALL_LIST)
```

## 获取 文件信息
```python
file_list = FileInfoList(where="文件夹的绝对路径")

# FileInfoList.CREATE_LIST  创建表单的SQL
# FileInfoList.INSERT_LIST  插入表单数据的SQL
# FileInfoList.ALL_LIST     所有创建表单和插入表单数据的所有SQL
# 返回的是一个列表
sqls = file_list.lists(mode=FileInfoList.INSERT_LIST)
```