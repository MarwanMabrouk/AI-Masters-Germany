USERNAME = "doadmin"
PASSWORD = "Rj5M6X7e219DvQ43"
DB_NAME = "data"
CONNECTION_STRING = 'mongodb+srv://{username}:{password}@{host}/{dbname}?{options}'.\
    format(username=USERNAME,
           password=PASSWORD,
           host='ai-masters-8e63c445.mongo.ondigitalocean.com',
           dbname=DB_NAME,
           options='tls=true&authSource=admin&replicaSet=ai-masters')