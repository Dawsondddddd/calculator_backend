# 后端代码规范

## 规范来源

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## 命名

- 模块、函数、变量使用 `snake_case`，例如 `save_history`、`record_id`。
- 类名使用 `CapWords`，例如 `ExpressionParser`。
- 常量使用全大写 `UPPER_CASE`，例如 `DB_PATH`、`MAX_EXPRESSION_LENGTH`。
- 私有实现通过命名表达意图，不滥用前置下划线。

## 格式

- 使用 4 个空格缩进，不使用 Tab。
- 每行不超过 100 个字符。
- 顶层定义之间空 2 行，类内方法之间空 1 行。
- 运算符两侧、逗号之后加空格。
- 文件编码统一使用 UTF-8。

## 注释与文档

- 每个模块写模块级 docstring，说明职责。
- 公开函数写 docstring，说明参数含义和异常行为。
- 注释解释“为什么”，不重复代码本身。

## 异常处理

- 用户输入错误抛出 `ExpressionError`，由 HTTP 层转换成 400 响应。
- 数据库等内部错误不向外暴露细节，统一返回 500。
- 不使用裸 `except:`，只捕获明确预期的异常类型。

## SQL 与安全

- 所有 SQL 使用参数化查询（`?` 占位符），禁止字符串拼接 SQL。
- 禁止对用户输入使用 `eval`、`exec` 或等价的可执行任意代码的方式。
- 对输入做长度限制和字符白名单校验。

## 分层职责

- 路由层（`app.py`）只做参数校验和响应封装，不写业务逻辑。
- 业务层（`calculator.py`）不导入 Flask，保证可以单独测试。
- 数据层（`database.py`）只封装数据库操作，不感知 HTTP。
