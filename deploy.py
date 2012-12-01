#!/usr/bin/env python2
from os import getcwd
from os.path import join, dirname, realpath, basename
from fabric.api import env, task, run, cd, sudo
from fabric.contrib.files import upload_template, exists

# DOCSTRINGS

__all__ = ['env', 'configure', 'deploy']


class config:
    pass

def configure(**settings):
    settings.setdefault('toxenv', 'py27')
    config.__dict__.update(settings)


@task
def deploy():
    if exists(get_project_root()):
        pull_repo()
    else:
        setup_project()
        clone_repo()
    tox()
    restart_uwsgi()


def setup_project():
    root = get_project_root()
    run('mkdir %s' % root)
    for tpl in ['nginx.conf', 'supervisord.conf']:
        upload_jinja_template(tpl)


def clone_repo():
    with cd(get_project_root()):
        run('git clone %s' % config.repo)


def pull_repo():
    with cd(get_repo()):
        run('git pull')


def tox():
    with cd(get_repo()):
        run('tox2')


def restart_uwsgi():
    sudo('supervisorctl restart %s' % config.domain)


def get_project_root():
    return join(config.root, config.domain)


def get_virtualenv():
    return join(get_repo(), '.tox', config.toxenv)


def get_repo():
    return join(get_project_root(), config.repo.rstrip('/').split('/')[-1])


def get_project_name():
    return basename(getcwd())


def upload_jinja_template(tpl):
    context = {
        'domain': config.domain,
        'uwsgi_sock': '/tmp/%s.sock' % config.domain,
        'virtualenv': get_virtualenv(),
        'repo': get_repo(),
        'project_name': get_project_name(),
    }
    src = tpl + '.jinja'
    dest = join(get_project_root(), tpl)
    return upload_template(src, dest, context, use_jinja=True,
                           template_dir=join(dirname(realpath(__file__)), 'templates'))
