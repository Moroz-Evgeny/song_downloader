from envparse import Env

env = Env()
env.read_envfile()

DOWNLOADS_DIR = env.str("DOWNLOADS_DIR")
CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
TOKEN_URL = env.str("TOKEN_URL")
API_URL = env.str("API_URL")