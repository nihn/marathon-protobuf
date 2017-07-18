# marathon-protobuf #
Simple tool for working with protobufs used by Marathon and stored in ZooKeeper

# commands #

## unreachable-strategy ##
Used to check and migrate `unreachableStrategy` attribute of Marathon apps.

## consistency ##
Used to check consistency between apps in Marathon and those stored in ZooKeeper.

## Usage ##
```
git clone https://github.com/nihn/marathon-protobuf
cd marathon-protobuf && pip install .
maraproto unreachable-strategy check --only-resident
maraproto unreachable-strategy fix (--dry-run)
maraproto consistency check
```
