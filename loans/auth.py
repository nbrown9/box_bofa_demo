from boxsdk import JWTAuth
from boxsdk import Client


auth = JWTAuth(
    client_id='2xld7m3w2j9hvjy60aq951lc68u2ocfv',
    client_secret='gFZg7dhe4Rr2eSIW1D7aZJs6WjXSGI2J',
    enterprise_id='15270599',
    jwt_key_id='qtm1mgfu',
    rsa_private_key_file_sys_path='loans/private_key.pem',
    rsa_private_key_passphrase='nb062795',
)

access_token = auth.authenticate_instance()

client = Client(auth)

ned_stark_user = client.create_user('Ned Stark')
