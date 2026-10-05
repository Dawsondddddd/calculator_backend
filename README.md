# 计算器系统 - 后端

前后端分离计算器系统的后端服务。负责表达式校验、解析、计算，以及计算历史的数据库存储。

## 技术栈

- Python 3.8+（开发环境 3.13）
- Flask：提供 HTTP 接口
- 标准库 `sqlite3`：持久化计算历史
- 手写递归下降解析器：完成表达式解析，不使用 `eval` / `exec`

## 目录结构

```
backend/
├── app.py             # 路由层：接口定义、参数校验、返回 JSON
├── calculator.py      # 业务层：表达式解析与计算
├── database.py        # 数据层：SQLite 增删查
├── requirements.txt   # 依赖清单
├── README.md
└── codestyle.md
```

## 运行环境

- Windows / macOS / Linux
- Python 3.8 及以上
- pip

## 安装方法

```bash
cd backend
pip install -r requirements.txt
```

## 启动方法

```bash
cd backend
python app.py
```

启动成功后输出：

```
 * Running on http://127.0.0.1:8000
```

## 配置说明

所有配置都在 `app.py` 顶部：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | 监听地址 |
| `PORT` | `8000` | 监听端口 |

数据库文件和表达式长度限制分别在 `database.py`、`calculator.py` 中：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `DB_PATH` | `backend/calculator.db` | SQLite 数据库文件 |
| `MAX_EXPRESSION_LENGTH` | `200` | 表达式最大长度 |

## 数据库初始化

服务启动时自动执行 `CREATE TABLE IF NOT EXISTS`，无需手动初始化。

表结构：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | INTEGER | 主键，自增 |
| `expression` | TEXT | 用户输入的表达式 |
| `result` | TEXT | 后端计算出的结果 |
| `created_at` | TEXT | 计算时间，格式 `YYYY-MM-DD HH:MM:SS` |

删除 `calculator.db` 文件即可清空数据并重新建库。

## API 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/calculate` | 计算表达式并保存历史 |
| GET | `/api/history` | 查询全部历史记录 |
| DELETE | `/api/history/{id}` | 删除指定历史记录 |
| DELETE | `/api/history` | 清空历史记录（附加功能） |
| GET | `/api/health` | 健康检查 |

### 计算

请求：

```json
{ "expression": "(1+2)*3" }
```

成功响应（200）：

```json
{ "success": true, "id": 1, "expression": "(1+2)*3", "result": 9, "created_at": "2026-10-05 10:20:00" }
```

失败响应（400）：

```json
{ "success": false, "message": "除数不能为 0" }
```

### 查询历史

响应（200）：

```json
{ "success": true, "data": [ { "id": 1, "expression": "1+2", "result": "3", "created_at": "2026-10-05 10:20:00" } ] }
```

## 支持的表达式

- 四则运算：`+`、`-`、`*`、`/`
- 复合表达式与优先级：`1 + 2 * 3`
- 括号：`(1 + 2) * 3`
- 一元正负号：`-5 + 8`、`3 * -2`
- 小数：`1.5 * 2`

## 安全说明

表达式的解析和计算由 `calculator.py` 中手写的递归下降解析器完成，全程没有使用 `eval`、`exec` 或任何等价的可执行任意代码的方式。SQL 全部使用参数化查询。

## 前后端连接方式

后端默认监听 `http://127.0.0.1:8000`，并通过 `after_request` 对所有响应添加 CORS 头（`Access-Control-Allow-Origin: *`），前端可以跨端口或直接用 `file://` 打开时访问。
