from flask import jsonify
from src.main.config.logger import logger


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": str(e)}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method Not Allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Error interno: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logger.exception(f"Excepción no controlada: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
