from datetime import datetime, timedelta
import jwt

class JWT_Auth():
    def __init__(self, algorithm='HS256'):
        self.algorithm=algorithm
        
    def generate_token(self, user,secret, exp_delta_seconds):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=exp_delta_seconds)
        }
        jwt_token = jwt.encode(payload, secret, self.algorithm)
        return jwt_token
    
    def check_token(self, token, secret):
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
            return True
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
    
    