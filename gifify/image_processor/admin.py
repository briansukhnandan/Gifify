from django.apps import apps
from django.contrib import admin


for model in apps.get_app_config('image_processor').get_models():
    admin.site.register(model)
