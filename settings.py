from envparse import Env

env = Env()
env.read_envfile()

DOWNLOADS_DIR = env.str("DOWNLOADS_DIR")