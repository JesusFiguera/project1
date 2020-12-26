from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='123912kjsfhs812321',
        DATABASE_HOST='localhost',
        DATABASE_PASSWORD='70242526e',
        DATABASE_USER='Jesus',
        DATABASE='usuarios',
    )

    import db

    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    return app



application = create_app()