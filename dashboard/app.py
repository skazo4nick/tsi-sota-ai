import os
import logging
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "devkey"),
        DEBUG= os.environ.get("DEBUG", "True") == "True"
    )
    
    # Load test config if passed in
    if test_config:
        app.config.update(test_config)
    
    # Setup logging
    logging.basicConfig(level=logging.DEBUG if app.config["DEBUG"] else logging.INFO)
    
    # Register routes via blueprint if app grows
    @app.route("/")
    def index():
        return render_template("index.html")

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        # In production, do not reveal error details to the user.
        return render_template("500.html"), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))