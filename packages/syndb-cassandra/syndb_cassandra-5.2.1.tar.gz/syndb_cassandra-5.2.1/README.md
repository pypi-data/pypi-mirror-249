# SynapseDB: Cassandra init

The following scripts initialize the tables used by SynapseDB on the designated Cassandra through CQLSH

### Setup port-forwarding from K8-nautilus:
```shell
kubectl port-forward -n syndb svc/syndb-cluster-client 9042:9042
```
