# marathon-protobuf #
Simple tool for managing protobufs used by Marathon and stored in ZooKeeper
Currently only use is to migrate and check `unreachableStrategy` attribute of Marathon apps.

## Usage ##
```
git clone https://github.com/nihn/marathon-protobuf
cd marathon-protobuf && pip install .
maraproto unreachable-strategy check --only-resident
maraproto unreachable-strategy fix (--dry-run)
```
