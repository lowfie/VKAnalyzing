import environs

env = environs.Env()
env.read_env()

VK_TOKEN = env.str('VK_TOKEN')

USER_DB = env.str('USER_DB')
PASSWORD_DB = env.str('PASSWORD_DB')
HOST_PORT = env.str('HOST_PORT')
DATABASE = env.str('DATABASE')

