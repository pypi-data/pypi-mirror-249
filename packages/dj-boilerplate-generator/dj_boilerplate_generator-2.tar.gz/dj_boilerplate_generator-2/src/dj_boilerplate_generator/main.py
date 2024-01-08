import os
import subprocess
import shutil
import inspect
import snippets


class DjangoProjectCreator:
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_path = os.path.join(os.getcwd(), self.project_name)

    def create_project(self):
        while True:
            if self.validate_name(self.project_name):
                try:
                    subprocess.check_output(f"django-admin startproject {self.project_name}", shell=True)
                    print(f"Basic structure of {self.project_name} (Django project) created successfully.")
                    break
                except Exception as err:
                    print(f"Error creating project: {err}")
                    exit(1)
            else:
                print("Invalid project name. Valid examples: [myaproject, my_aproject, myaproject12, my_aproject1]")
                self.project_name = input("Please enter a valid project name: ")

    def create_app(self,app_name):
        while True:
            app_path = os.path.join(self.project_path, app_name)

            if self.validate_name(app_name):
                try:    
                    subprocess.run(f"cd {self.project_path} && py manage.py startapp {app_name}", shell=True)

                    # templates_path = os.path.join(app_path, 'templates')
                    # os.makedirs(templates_path, exist_ok=True)

                    self.copy_template(os.path.join(app_path))  # Copy modified index.html

                    self.update_settings(app_name)
                    self.update_urls(app_name)
                    self.add_view(app_name,snippets)

                    print(f"Basic structure of {app_name} (Django application) created successfully.")
                    break

                except Exception as error:
                    print(f"Error while creating app {error}")
            else:
                print("Invalid app name. Valid examples: [myapp, my_app, myapp12, my_app1]")
                app_name = input("Please enter a valid app name: ")


    def add_view(self, app_name, view_function):
        app_location = os.path.join(self.project_path, app_name, 'views.py')
        with open(app_location, "a+") as file_object:
            source_code = inspect.getsource(view_function)
            file_object.write(f"\n{source_code}")

    def update_settings(self, app_name):
        settings_location = os.path.join(self.project_path, self.project_name, 'settings.py')

        with open(settings_location, "r") as open_settings:
            read_settings = open_settings.read()
            settings_app_init = 'django.contrib.staticfiles\','
            if settings_app_init in read_settings:
                add_app = read_settings.replace(settings_app_init, settings_app_init + f'\n    \'{app_name}\',')

                with open(settings_location, 'w') as file:
                    file.write(add_app)

    def update_urls(self, app_name):
        urls_location = os.path.join(self.project_path, self.project_name, 'urls.py')

        with open(urls_location, 'r') as open_urls:
            read_urls = open_urls.read()
            dj_url_init = """urlpatterns = [
    path('admin/', admin.site.urls),
]"""
            if dj_url_init in read_urls:
                add_url = read_urls.replace(
                    dj_url_init,
                    f"""from django.conf.urls import url\nfrom {app_name} import views\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    url('', views.index_view)\n]""")

                with open(urls_location, 'w') as url_file:
                    url_file.write(add_url)

    def validate_name(self, name):
        return (
            len(name) >= 2
            and all(c.isalnum() or c == '_' or c.isspace() for c in name)
            and not name[0].isdigit()
            and '-' not in name
        )

    def copy_template(self, destination):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # template_path = os.path.join(current_dir, template_name)
        # destination_path = os.path.join(destination, template_name)
        # shutil.copyfile(template_path, destination_path)

        static_path = os.path.join("static")
        destination_path = os.path.join(destination, "static")
        shutil.copytree(static_path, destination_path)

        static_path = os.path.join("templates")
        destination_path = os.path.join(destination, "templates")
        shutil.copytree(static_path, destination_path)


if __name__ == "__main__":
    project_name = input('Enter project name:')
    django_project_creator = DjangoProjectCreator(project_name)
    django_project_creator.create_project()

    app_name = input("Enter application name:")
    django_project_creator.create_app(app_name)