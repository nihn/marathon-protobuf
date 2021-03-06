import os

from click import group, command, option, pass_obj, echo
from maraproto.utils import (
    apps_nodes_gen,
    get_service_proto,
)


def unreachable_strategy_defined(service_proto):
    strategy = service_proto.unreachableStrategy
    return (strategy.HasField('expungeAfterSeconds') and
            strategy.HasField('inactiveAfterSeconds'))


def disable_unreachable_strategy(service_proto):
    strategy = service_proto.unreachableStrategy
    strategy.ClearField('expungeAfterSeconds')
    strategy.ClearField('inactiveAfterSeconds')


def is_resident(service_proto):
    return service_proto.residency.taskLostBehavior == \
           service_proto.residency.WAIT_FOREVER


@group('unreachable-strategy')
def unreachable_strategy():
    pass


@command()
@option('--only-resident', is_flag=True, help='Only check resident tasks')
@pass_obj
def check(zk_client, only_resident):

    for app in apps_nodes_gen(zk_client):
        result = []

        for version in zk_client.get_children(app):
            service = get_service_proto(
                zk_client, os.path.join(app, version))

            if only_resident and not is_resident(service):
                continue

            result.append('unreachableStrategy set for %s/%s: %s' % (
                app, version, unreachable_strategy_defined(service)))
        if result:
            echo("\n======%s======\n%s" % (app,  '\n'.join(result)))


@command()
@option('--dry-run', is_flag=True)
@pass_obj
def fix(zk_client, dry_run):
    migrated = 0

    for app in apps_nodes_gen(zk_client):
        result = []

        for version in zk_client.get_children(app):
            version_path = os.path.join(app, version)
            service = get_service_proto(zk_client, version_path)

            if not is_resident(service) or not \
                    unreachable_strategy_defined(service):
                continue

            disable_unreachable_strategy(service)

            if not dry_run:
                zk_client.set(version_path, service.SerializeToString())

            result.append('unreachableStrategy for version %s changed to '
                          '"disabled"' % version)
        if result:
            echo("\n======%s======\n%s" % (app,  '\n'.join(result)))
            migrated += len(result)

    echo("Fixing done, %d protobufs migrated" % migrated)


unreachable_strategy.add_command(check)
unreachable_strategy.add_command(fix)
