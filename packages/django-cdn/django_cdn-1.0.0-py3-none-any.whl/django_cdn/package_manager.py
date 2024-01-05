import json
import os

from django.conf import settings


class PackageManager:

    @classmethod
    def get_installed_packages_path(cls):
        default = settings.BASE_DIR / 'cdn_packages.json'
        return str(getattr(settings, 'CDN_PACKAGES_INFO_PATH', default))

    @classmethod
    def get_installed_packages(cls):
        file_path = cls.get_installed_packages_path()
        data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        return data

    @classmethod
    def write_installed_packages(cls, installed_packages):
        file_path = cls.get_installed_packages_path()
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w') as file:
            json.dump(installed_packages, file, indent=4)

    @classmethod
    def get_static_path(cls):
        try:
            default = settings.STATICFILES_DIRS[0]
        except IndexError:
            default = None
        result = str(getattr(settings, 'CDN_BUILD_STATIC_PATH', default))
        if result is None:
            raise Exception('Settings.py: CDN_BUILD_STATIC_PATH not set and not STATICFILES_DIRS found.')
        if not result.startswith(str(settings.BASE_DIR)):
            raise Exception('Settings.py: CDN_BUILD_STATIC_PATH need to be inside BASE_DIR.')
        return result + '/lib'
