from django.apps import AppConfig
from api.utils import pinecone_utils


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
  
    def ready(self):
       pinecone_utils.init_pinecone()