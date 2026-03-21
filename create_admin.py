import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Services'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'vedants201011@gmail.com', '7aDm1n4@8')
    print('Superuser created')
else:
    print('Superuser already exists')
