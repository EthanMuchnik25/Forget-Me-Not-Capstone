from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    get_jwt, get_jwt_identity


from app.config import Config

# Import database
if Config.DATABASE_VER == "RDS":
    from app.database.rds import db_write_line
elif Config.DATABASE_VER == "SQLITE":
    raise NotImplementedError
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db import db_register_user, db_get_user_pw,\
        db_add_token_blacklist, db_check_token_blacklist
else:
    raise NotImplementedError



def register_user(uname, pw):
    pw_hash = generate_password_hash(pw, Config.JWT_HASH_FN)

    return db_register_user(uname, pw_hash)
    


# TODO: we keep issuing tokens if the user is already logged in, we should 
# disable the old one -> in this case need to store logged-on status, or last 
# token. Do later
def login_user(uname, pw):
    pw_hash = db_get_user_pw(uname)

    if pw_hash == None:
        return False, "User does not exist"
    
    if not check_password_hash(pw_hash, pw):
        return False, "Incorrect password"
    
    # NOTE: potential for weird races if we chnage this. Probably try to 
    # reset whole token database in this case.
    access_token = create_access_token(identity=uname, expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES)
    return True, access_token


# TODO untested
def logout_user(uname, jwt):
    jti = jwt['jti']
    exp = jwt['exp']
    db_add_token_blacklist(jti, exp)

# TODO untested
def check_blocklist(payload):
    jti = payload['jti']
    return db_check_token_blacklist(jti)

# TODO unregister user behavior
# def unregister_user():
#     pass
