import logging
import os

from datetime import datetime

from click import command, group, option, pass_obj, pass_context, Tuple, echo
from marathon import MarathonClient

from maraproto.utils import apps_nodes_gen, get_service_proto

logging.basicConfig(level=logging.ERROR)


@group()
@option('-m', '--marathon-addr')
@option('-c', '--marathon-creds', type=Tuple([str, str]))
@pass_obj
@pass_context
def consistency(ctx, zk_client, marathon_addr, marathon_creds):
    marathon_addr = marathon_addr or 'http://%s:8080' % zk_client.hosts[0][0]
    marathon_client = MarathonClient(marathon_addr, verify=False)

    if marathon_creds:
        marathon_client.auth = marathon_creds
    ctx.obj = zk_client, marathon_client


@command()
@pass_obj
def check(obj):
    zk_client, marathon_client = obj
    all_apps = {app.id: app for app in marathon_client.list_apps()}
    total = len(all_apps)
    invalid = 0

    for app in apps_nodes_gen(zk_client):
        zk_versions = [get_service_proto(zk_client, os.path.join(app, child))
                       for child in zk_client.get_children(app)]
        zk_app = max(zk_versions, key=get_version_time)

        try:
            marathon_app = all_apps.pop(zk_app.id)
        except KeyError:
            logging.error('%s was deleted in Marathon but is still '
                          'present in ZK', zk_app.id)
            continue

        marathon_version = get_version_time(marathon_app)
        zk_version = get_version_time(zk_app)

        if marathon_version != zk_version:
            log_inconsistency(zk_app.id, marathon_version, zk_version)
            invalid += 1
        else:
            logging.info('Both version of %s are %s', zk_app.id, zk_version)

    for missing_app in all_apps:
        logging.error('App %s is present in Marathon but not in ZK', missing_app)

    echo('Summary:\n'
         'Total: {total}\n'
         'Invalid: {invalid}'.format(**locals()))


def get_version_time(obj):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(obj.version, date_format)


def log_inconsistency(app_id, marathon_version, zk_version):
    logging.info('%s != %s', marathon_version, zk_version)
    is_zk_older = zk_version < marathon_version
    desc = 'older' if is_zk_older else 'newer'
    value = marathon_version - zk_version if is_zk_older else \
        zk_version - marathon_version
    logging.error('App %(app_id)s has different version on ZK and Marathon '
                  '(ZK\'s is %(value)s %(desc)s than Marathon\'s)', locals())

consistency.add_command(check)
