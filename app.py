# app.py
from flask import Flask, jsonify, request
import importlib.util
import traceback

app = Flask(__name__)

@app.route('/run_test/<test_name>', methods=['GET'])
def run_test(test_name):
    try:
        # Динамически импортируем тест из папки /tests
        spec = importlib.util.spec_from_file_location(
            test_name, 
            f"tests/{test_name}.py"
        )
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Запускаем тест (предполагаем, что в тесте есть функция `run()`)
        result = test_module.run()  
        return jsonify({"status": "success", "result": result})
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == '__main__':
    app.run(debug=True)