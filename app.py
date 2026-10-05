from flask import Flask, jsonify, request

from calculator import ExpressionError, calculate
from database import (
    clear_history,
    delete_history,
    init_db,
    list_history,
    save_history,
)

HOST = "127.0.0.1"
PORT = 8000

app = Flask(__name__)
init_db()


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.post("/api/calculate")
def calculate_api():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(success=False, message="请求体必须是合法的 JSON 对象"), 400

    expression = data.get("expression")
    if not isinstance(expression, str):
        return jsonify(success=False, message="缺少 expression 字段"), 400

    try:
        expression = expression.strip()
        result = calculate(expression)
    except ExpressionError as error:
        return jsonify(success=False, message=str(error)), 400

    record_id, created_at = save_history(expression, str(result))
    return jsonify(
        success=True,
        id=record_id,
        expression=expression,
        result=result,
        created_at=created_at,
    )


@app.get("/api/history")
def history_api():
    return jsonify(success=True, data=list_history())


@app.delete("/api/history/<int:record_id>")
def delete_history_api(record_id):
    if delete_history(record_id):
        return jsonify(success=True, message="删除成功")
    return jsonify(success=False, message="记录不存在"), 404


@app.delete("/api/history")
def clear_history_api():
    clear_history()
    return jsonify(success=True, message="已清空历史记录")


@app.get("/api/health")
def health_api():
    return jsonify(success=True, message="ok")


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify(success=False, message="接口不存在"), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return jsonify(success=False, message="请求方法不被允许"), 405


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
