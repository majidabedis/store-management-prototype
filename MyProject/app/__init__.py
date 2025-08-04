# from flask import Flask
# from app.config import Config
# from app.db.connection_manager import ConnectionManager
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     ConnectionManager.initialize_pool()
#
#     # ثبت کردن روت‌ها
#     from app.routes.product_routes import product_bp
#     app.register_blueprint(product_bp)
#
#     # هندل بستن کانکشن‌ها
#     @app.teardown_appcontext
#     def close_connection(error=None):
#         ConnectionManager.close_connection(error)
#
#     # return app
# #