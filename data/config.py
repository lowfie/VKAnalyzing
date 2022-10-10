import environs

env = environs.Env()
env.read_env()

# vk_api token
VK_TOKEN = env.str('VK_TOKEN')

# telegram_api token
BOT_TOKEN = env.str('BOT_TOKEN')

# postgres connection
USER_POSTGRES = env.str('USER_POSTGRES')
PASSWORD_POSTGRES = env.str('PASSWORD_POSTGRES')
HOST_POSTGRES = env.str('HOST_POSTGRES')
PORT_POSTGRES = env.str('PORT_POSTGRES')
DATABASE_POSTGRES = env.str('DATABASE_POSTGRES')

