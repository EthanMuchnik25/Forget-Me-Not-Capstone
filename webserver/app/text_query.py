from app.config import Config

# Import database
if Config.DATABASE_VER == "RDS":
    # TODO BAD BAD BAD BAD Make good interface
    from app.database.rds import rds_database
elif Config.DATABASE_VER == "SQLITE":
    from app.database.sqlite import TODO
else:
    raise NotImplementedError


def handle_text_query(query):
    if query == 'swaglab':
        response = {
            'imageUrl': '/static/swaglab.jpg',
            'success': True
        }
    elif query == 'sign':
        response = {
            'imageUrl': 'https://i.redd.it/87xuofmvnlud1.png',
            'success': True
        }
    else:
        response = {
            'success': False,
            'message': 'random message'
        }