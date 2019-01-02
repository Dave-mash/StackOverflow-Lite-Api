from datetime import datetime, timedelta
import jwt
from instance.config import app_config

class BaseModel:

    @staticmethod
    def encode_auth_token(user_id):
        """ This method generates an authentication token """
        from app import create_app
        app = create_app()

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            res = token
        except Exception as e:
            res = e    
            
        return res

    @staticmethod
    def decode_auth_token(auth_token):
        """e
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        from app import create_app
        app = create_app()
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'