from click import group, option, pass_context, Tuple
from kazoo.client import KazooClient

from maraproto.unreachable_strategy import unreachable_strategy
from maraproto.consistency import consistency


@group()
@option('--zk-addr', default='localhost')
@option('--zk-creds', type=Tuple([str, str]))
@pass_context
def main(ctx, zk_addr, zk_creds):
    zk_client = KazooClient(zk_addr)
    zk_client.start()

    if zk_creds:
        zk_client.add_auth('digest', ':'.join(zk_creds))
    ctx.obj = zk_client


main.add_command(unreachable_strategy)
main.add_command(consistency)

if __name__ == '__main__':
    main()
