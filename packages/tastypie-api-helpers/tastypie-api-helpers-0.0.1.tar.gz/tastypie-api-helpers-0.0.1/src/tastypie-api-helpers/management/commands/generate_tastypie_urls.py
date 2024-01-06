
from django.core.management.base import BaseCommand
from django.conf import settings
import importlib
import inspect
import ast
import json
import os

class Command(BaseCommand):
    help = 'This commands reads the registerd Tastypie API and generates the url file'
    
    def handle(self, *args, **kwargs):
        
        urls_module = importlib.import_module(settings.ROOT_URLCONF)
        urls_file_path = inspect.getsourcefile(urls_module)
        
        with open(urls_file_path, 'r') as urls_file:
            urls_file_content = urls_file.read()
            
        tree = ast.parse(urls_file_content)
        
        api_object_name = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Name) and
                        isinstance(node.value, ast.Call) and
                        hasattr(node.value.func, 'id') and
                        node.value.func.id == 'Api'
                    ):
                        api_object_name = target.id
                        break
        
        if not api_object_name:
            raise Exception('Api object not found')
        
        api_object = getattr(urls_module, api_object_name)
        res = []
        base_url = '/api/'
        
        for resource_name, resource in api_object._registry.items():
            api_name = api_object.api_name
            resource_url = f"{base_url}{api_name}/{resource._meta.resource_name}/"
            for url in resource.urls:
                api_path = resource_url + '/'.join(url.pattern.regex.pattern.split('/')[1:]).strip(' $')
                select_flag = True
                if api_path.endswith('/(?P<pk>.*?)/') \
                or api_path.endswith('(?P<pk_list>.*?)/') \
                or api_path.endswith('/schema/') \
                or api_path.endswith('/set/'):
                    select_flag = False
                res.append({'api_path': api_path, 'selected': select_flag})

        django_root_path = settings.BASE_DIR
        api_output_file_name = 'apidoc_url_import_file.json'
        
        file_path = os.path.join(django_root_path, api_output_file_name)
        
        with open(file_path, 'w') as api_output_file:
            json.dump(res, api_output_file)
