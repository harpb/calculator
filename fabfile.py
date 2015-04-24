import pprint
from fabfile_settings import environments
from fabric.api import *

if env.key_filename == None:
    env.key_filename = ["~/.ssh/id_rsa"]

for env_name, env_settings in environments.iteritems():
    env_settings['pyenv_path'] = env_settings['repo_dir'] + '/pyenv'
    env_settings['webapp_path'] = env_settings['repo_dir'] + '/webapp'
    env_settings['static_path'] = env_settings['webapp_path'] + '/static'
    env_settings['js_apps'] = ['.']
    env_settings['server_script'] = env_settings['webapp_path'] + '/gevent_wsgi_server.py'

#===============================================================================
# ENVIRONMENTS
#===============================================================================
def local():
    env.settings = environments['local']
    env.hosts = env.settings['servers']

def prod():
    env.settings = environments['prod']
    env.hosts = env.settings['servers']
    if 'user' in env.settings:
        env.user = env.settings['user']

#===============================================================================
# HELPERS
#===============================================================================
def run_in_background(cmd, server_env):
#    run("nohup export SERVER_ENVIRONMENT=PROD %s >& /dev/null < /dev/null &" % cmd, shell=False, pty=False)
# #        run("export -p", shell=False, pty=False)
    run('bash -c export SERVER_ENVIRONMENT=%s' % server_env['type'])
    run('export SERVER_ENVIRONMENT=%s' % server_env['type'])
    run('declare -x SERVER_ENVIRONMENT=%s' % server_env['type'])
    with prefix('export SERVER_ENVIRONMENT=%s' % server_env['type']):
        full_cmd = "export DJANGO_SETTINGS_MODULE=webapp.settings; export SERVER_ENVIRONMENT=%s; nohup %s >& /dev/null < /dev/null &" % (
                server_env['type'], cmd)
        run(full_cmd, shell = False, pty = False)

def django_manage(cmd, background = False, server_env = None):
    if not server_env:
        server_env = env.settings
    full_cmd = '%s/bin/python %s/manage.py %s' % (
            server_env['pyenv_path'], server_env['webapp_path'], cmd)
    if background:
        run_in_background(full_cmd)
    else:
        with prefix("export SERVER_ENVIRONMENT=%s" % server_env['type']):
            run(full_cmd)

#===============================================================================
# ACTIONS
#===============================================================================
def start_server(server_env = None):
    if not server_env:
        server_env = env.settings
    sudo('service nginx start')
    
    for port in server_env['ports']:
        cmd = '%s/bin/python %s %d' % (server_env['pyenv_path'], server_env['server_script'], port)
        run_in_background(cmd, server_env)

def stop_django(server_env = None):
    if not server_env:
        server_env = env.settings
    try:
        run('pkill -f %r' % server_env['server_script'])
    except:
        pass

def stop_server(server_env = None):
    if not server_env:
        server_env = env.settings
    sudo('service nginx stop')
    stop_django(server_env)

def restart_server():
    try:
        stop_server()
    except:
        pass
    start_server()

def pull_changes():
    # PULL changes
    with cd(env.settings["repo_dir"]):
        run("git status")
        run("git pull")
#===============================================================================
# Virtualenv
#===============================================================================
def pip(command):
    with cd(env.settings["repo_dir"]):
        run("./pyenv/bin/pip {}".format(command))
        
def build_wheels():
    pull_changes()
    pip('wheel --wheel-dir=/tmp/wheelhouse -r requirements.txt MySQL-python gevent')
        
def build_pyenv():
    run('apt-get update')
    run('apt-get -y upgrade')
    run('apt-get -y dist-upgrade')
    run('apt-get install libmysqlclient-dev')
    run('easy_install -U distribute')
    
    pull_changes()
#    run('pip install lxml')
    run("rm -rf ./pyenv/build")
    pip('install --use-wheel --no-index --find-links=/tmp/wheelhouse MySQL-python gevent')
    pip('install --use-wheel --no-index --find-links=/tmp/wheelhouse -r requirements.txt --upgrade --exists-action=s')
        
#===============================================================================
# Deployment
#===============================================================================
def django_sync():
    # UPDATE static files
    django_manage('collectstatic -l --noinput')
    django_manage('migrate')

def npm_install():
    with cd(env.settings["static_path"]):
        for app in env.settings["js_apps"]:
            with cd(app):
                run("npm install")
                run("bower install --allow-root")

def refresh():
    pull_changes()
    django_sync()
    restart_server()
