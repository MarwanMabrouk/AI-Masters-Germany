
DB_NAME = "data"

try:
    from dotenv import dotenv_values
    config = dotenv_values(".env")
    if config == {}:
        raise Exception("No .envs file found")  
    CONNECTION_STRING = 'mongodb+srv://{username}:{password}@{host}/{dbname}?{options}'.\
        format(username=config['USERNAME'],
            password=config['PASSWORD'],
            host=config['HOST'],
            dbname=DB_NAME,
            options='tls=true&authSource=admin&replicaSet=ai-masters')
    print("Using remote database")
except Exception as e:
    print("No .env file found, using local database instead")
    CONNECTION_STRING = 'mongodb://localhost:27017/' + DB_NAME