import environs

env = environs.Env()
env.read_env()

# vk_api token
VK_TOKEN = env.str("VK_TOKEN")

# telegram_api token
BOT_TOKEN = env.str("BOT_TOKEN")

# postgres connection
USER_POSTGRES = env.str("USER_POSTGRES")
PASSWORD_POSTGRES = env.str("PASSWORD_POSTGRES")
HOST_POSTGRES = env.str("HOST_POSTGRES")
PORT_POSTGRES = env.str("PORT_POSTGRES")
DATABASE_POSTGRES = env.str("DATABASE_POSTGRES")

# redis connection
PREFIX_REDIS = env.str("PREFIX_REDIS")
PASSWORD_REDIS = env.str("PASSWORD_REDIS") if env.str("PASSWORD_REDIS") else None
HOST_REDIS = env.str("HOST_REDIS")
PORT_REDIS = env.str("PORT_REDIS")
DATABASE_REDIS = env.str("DATABASE_REDIS")
