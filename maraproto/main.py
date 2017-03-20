from click import group
from click import option, pass_context

from kazoo.client import KazooClient

from maraproto.unreachable_strategy import unreachable_strategy


@group()
@option('--zk-addr', default='localhost')
@option('--zk-creds', help='Credentials string in form <username>:<password>')
@pass_context
def main(ctx, zk_addr, zk_creds):
    zk_client = KazooClient(zk_addr)
    zk_client.start()

    if zk_creds:
        zk_client.add_auth('digest', zk_creds)
    ctx.obj = zk_client


main.add_command(unreachable_strategy)

if __name__ == '__main__':
    main()
