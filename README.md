# Ahri Database

## Create a free database for your development environment

## Build the image

```Dockerfile
# Coming soon
```

## Python requirements.txt

```py
click==7.1.1
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.11.1
MarkupSafe==1.1.1
pymongo==3.10.1
PyMySQL==0.9.3
Werkzeug==1.0.0
```

## How to use

### Get all database

`Get http://ip:port/database/?<option>=<args>&...`

| option | args         | explain    |
| ------ | ------------ | ---------- |
| type   | mongo, mysql | 数据库类型 |
| user   | ""           | 用户 token |

### Create new database

`POST http://ip:port/database/`

| option   | args         | explain    |
| -------- | ------------ | ---------- |
| type     | mongo, mysql | 数据库类型 |
| password | 密码         | 密码       |

### Drop a database

`POST http://ip:port/database/`

| option   | args         | explain    |
| -------- | ------------ | ---------- |
| type     | mongo, mysql | 数据库类型 |
| database | 数据库名     | 数据库名   |

## Powered By ahri 20200323
