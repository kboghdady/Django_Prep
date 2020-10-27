#Create the essintial data into the Djano app
# to run the script python django_prep.py PROJECT APP1 APP2


import sys
import os
from pathlib import Path

apps = sys.argv
apps.pop(0)  # remove the python file name
project_name = apps.pop(0)
print("Project name: {}".format(project_name))
print("all apps: {}".format(apps))
os.system("django-admin startproject {}".format(project_name))
os.chdir("{}".format(project_name))




##########Variables################################
PATH = os.path.abspath(os.getcwd())
project_path = os.path.join(PATH,project_name)
settings_path = os.path.join(project_path,"settings.py")
urls_path = os.path.join(project_path,"urls.py")
####################################################

###### adding lines to the files
def addALine(file, line2Add, lineBefore):
  with open(file, "r") as in_file:
      buf = in_file.readlines()

  with open(file, "w") as out_file:
      for line in buf:
          if line == "{}\n".format(lineBefore):
              line = line + "{}\n".format(line2Add)
          out_file.write(line)

######################################################




addStaticLines = """urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\n
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 """
urls_import = """from django.conf import settings\nfrom django.conf.urls.static import static """

first_view = """def home(request):\n
 \treturn render(request,'rooms/home.html')"""


addALine("{}".format(urls_path),addStaticLines,"]")
addALine("{}".format(urls_path),urls_import,"from django.urls import path")
addALine("{}".format(settings_path),"import os","from pathlib import Path")

# Add STATIC FILE AND MEDIA
addALine("{}".format(settings_path),"MEDIA_ROOT = BASE_DIR","STATIC_URL = '/static/'")
addALine("{}".format(settings_path),"MEDIA_URL = '/media/'","STATIC_URL = '/static/'")
addALine("{}".format(settings_path),"STATIC_ROOT = os.path.join(BASE_DIR,'static')","STATIC_URL = '/static/'")




for app in apps:
  print(app)
  app_path = os.path.join(PATH,app)
  app_view_path = os.path.join(app_path, "views.py")
  admin_path = os.path.join(app_path,"admin.py")

  os.system("django-admin startapp {}".format(app))
  addALine("{}".format(urls_path),"import {}.views".format(app),"from django.urls import path")
  addALine("{}".format(settings_path),"'{}',".format(app),"'django.contrib.staticfiles',")


  #views.py
  addALine("{}".format(app_view_path),first_view,"from django.shortcuts import render")
  addALine("{}".format(app_view_path),"from django.shortcuts import get_object_or_404","from django.shortcuts import render")
  addALine("{}".format(app_view_path),"#from .models import <MODLE>","# Create your views here.")

  #Admin.py
  addALine("{}".format(admin_path),"#from .models import <MODLE>","# Register your models here.")
  addALine("{}".format(admin_path),"#admin.site.register(<MODEL>)","import .models")


  #Create the template folders
  os.mkdir("{}/templates".format(app_path))
  os.mkdir("{}/static".format(app_path))
  os.mkdir("{}/templates/{}".format(app_path,app))
  home_file = open("{}/templates/{}/home.html".format(app_path,app),"w+" )
  home_file.write("{\% load static \%}")
  home_file.close()
