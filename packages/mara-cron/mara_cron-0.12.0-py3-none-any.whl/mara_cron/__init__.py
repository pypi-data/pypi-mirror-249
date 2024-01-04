"""Make the functionalities of this package auto-discoverable by mara-app"""
__version__ = '0.12.0'


def MARA_CONFIG_MODULES():
    from . import config
    return [config]


def MARA_FLASK_BLUEPRINTS():
    from . import ui, views
    return [views.blueprint]


def MARA_ACL_RESOURCES():
    from . import views
    return {'Cron': views.acl_resource}


def MARA_CLICK_COMMANDS():
    from . import cli
    return [
        cli.mara_cron,
        cli._enable,
        cli._disable,
        cli._schedule_job,
        cli._list_crontab,
        cli._write_crontab,
        cli._clear_crontab
    ]


def MARA_NAVIGATION_ENTRIES():
    from . import views
    return {'Cron Nav Entries Configs': views.package_cronjobs_navigation_entry()}
