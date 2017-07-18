import os

from maraproto.proto import marathon_pb2


def apps_nodes_gen(zk_client):
    apps_node = '/marathon/state/apps'

    for apps_sub_node in zk_client.get_children(apps_node):
        apps_sub_node_path = os.path.join(apps_node, apps_sub_node)

        for node in zk_client.get_children(apps_sub_node_path):
            yield os.path.join(apps_sub_node_path, node)


def get_service_proto(zk_client, zk_path):
    service = marathon_pb2.ServiceDefinition()
    service.ParseFromString(zk_client.get(zk_path)[0])
    return service
