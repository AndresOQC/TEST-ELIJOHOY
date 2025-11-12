from app.core.app_factory import create_app
from flask import request, jsonify, send_from_directory, abort
import os

app = create_app()


@app.route('/api', methods=['GET'])
def api_root():
    period = request.args.get('period')
    if period:
        return jsonify({"message": f"Periodo recibido: {period}"})
    return jsonify({"error": "Periodo no especificado"}), 400


# Serve avatar images from mounted folder (/app/static/avatars)
@app.route('/avatars/<tipo>', methods=['GET'])
def avatar_by_tipo(tipo):
    # Try several candidate locations for the avatars folder
    candidates = [
        os.path.join(app.root_path, 'static', 'avatars'),
        os.path.join(os.path.dirname(app.root_path), 'static', 'avatars'),
        '/app/static/avatars',
        os.path.join(os.getcwd(), 'static', 'avatars')
    ]

    avatar_dir = None
    for c in candidates:
        if os.path.isdir(c):
            avatar_dir = c
            break

    if not avatar_dir:
        app.logger.debug('Avatar folder not found. Candidates tried: %s', candidates)
        abort(404)

    try:
        files = os.listdir(avatar_dir)
    except Exception as e:
        app.logger.exception('Error listing avatar directory: %s', e)
        abort(404)

    for f in files:
        if f.lower().startswith(tipo.lower()):
            return send_from_directory(avatar_dir, f)

    abort(404)


@app.route('/avatars/files/<path:filename>')
def avatar_file(filename):
    avatar_dir = os.path.join(os.getcwd(), 'static', 'avatars')
    return send_from_directory(avatar_dir, filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)