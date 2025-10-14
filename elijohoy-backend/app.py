from app.core.app_factory import create_app
from flask import request, jsonify
import os

app = create_app()

@app.route('/api', methods=['GET'])
def api_root():
    period = request.args.get('period')
    if period:
        return jsonify({"message": f"Periodo recibido: {period}"})
    return jsonify({"error": "Periodo no especificado"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)