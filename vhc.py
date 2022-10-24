#!/usr/bin/env python3
import os
import pathlib
import pwd
import stat
import string
import subprocess

vh_templates = str(pathlib.Path.cwd()) + '/templates'
vh_workspace = str(pathlib.Path.cwd()) + '/out/'


def read_templates():
    domain_name = input('Your domain name:')
    create_index(domain_name)
    create_vh(domain_name)
    run_script(domain_name)


def create_index(domain_name):
    f = open(vh_templates + '/index')
    index = f.read()
    index_location = '/var/www/{0}/public_html'.format(domain_name)
    pathlib.Path(index_location).mkdir(parents=True, exist_ok=True)
    write_out(string.Template(index).substitute(domainName=domain_name), index_location + '/index.html')
    f.close()


def create_vh(domain_name):
    proxy_ip = input('Proxy address:')
    port = input('Proxy port:')
    f = open(vh_templates + '/vh')
    index = f.read()
    f.close()
    domain_conf = '/etc/apache2/sites-available/' + domain_name + '.conf'
    write_out(string.Template(index).substitute(domainName=domain_name, proxyPort=port, proxyAddress=proxy_ip),
              domain_conf)


def write_out(content, file_name):
    f1 = open(file_name, 'w')
    f1.write(content)
    print('Created file: ' + file_name)
    f1.close()


def run_script(domain_name):
    uid = pwd.getpwnam("rishi").pw_uid
    print('uid: ' + str(uid))
    os.chown('/var/www/' + domain_name + '/public_html', uid, -1)
    os.chmod('/var/www', stat.S_IROTH)
    enable_site = 'sudo a2ensite ' + domain_name + '.conf'
    print('enable_site: ' + enable_site)
    subprocess.Popen(enable_site, shell=True, stdout=subprocess.PIPE)
    subprocess.run('/etc/init.d/apache2 restart', shell=True, stdout=subprocess.PIPE)


read_templates()

exit(0)
