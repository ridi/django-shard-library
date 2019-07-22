Changelog
=========
0.1.3 (Jul 22nd 2019)
-------------------
- Add a logic for source database of shard static

0.1.2 (Apr 19th 2019)
-------------------
- Support django 2.2

0.1.1 (Aug 21st 2018)
-------------------
- Change the way which register database config.
    - Add new feature which extend `options` and `conn_max_age` each shard.

0.1.0 (July 10th 2018)
-------------------
- Add fresh manger mode.

0.0.17 (Jun 28th 2018)
-------------------
- Fix bug for execute_query_command and service.

0.0.16 (Jun 27th 2018)
-------------------
- Add query executor django command.

0.0.15 (Jun 11st 2018)
-------------------
- Add conn_max_age parameter.

0.0.14 (Jun 4th 2018)
-------------------
- Refac logic for transmitting
    - Remove static_transmit_service.
    - Initialize transmitter interface
- Remove config about lock

0.0.13 (Jun 1st 2018)
-------------------
- Fix bug that loop is run more than expectation.

0.0.12 (Jun 1st 2018)
-------------------
- Change con_hash algorithm to blake2b
- Change to transmit datetime field from the source.
    - for example last_modified, created

0.0.11 (May 31st 2018)
-------------------
- Change definition for shard_static from sync to transmit
- Change con_hash algorithm from sha256 to md5
- Increase DEFAULT_REPLICA_COUNT to 512

0.0.10 (May 24th 2018)
-------------------
- The shard logic is made to use of consistent hash.
- Remove transaction in sync_static_service.
- Separate update_or_create to update and bulk_create in sync_static_service.
- No coercion in setting the lock class.

0.0.9 (May 15th 2018)
-------------------
- Fix bug for sync logic

0.0.8 (May 15th 2018)
-------------------
- Fix bug

0.0.7 (May 15th 2018)
-------------------
- Repurpose config.SHARD_SYNC_MAX_ITEMS
- Change run_sync_with_lock arguments to the same with run_sync
- Improve sync logic

0.0.6 (May 2nd 2018)
------------------
- Fix incorrect structure for StaticSyncStatus
- Remove ALL_SHARD_GROUP and logic for it

0.0.5 (Apr 17th 2018)
------------------
- Add new feature for shard static
- Change dependency version

0.0.4 (Mar 30th 2018)
------------------
- Test Travis Deploy

0.0.3 (Mar 23th 2018)
------------------
- Change logic for calculate shard_key
- Support raw, bulk_create in `ShardManager`

0.0.2 (Mar 23th 2018)
------------------
- Change config structure
  - Support db_options


0.0.1 (Mar 7th 2018)
------------------

### Register New Package
- Addition of initial functions related to sharding
    - shardmodel, read-replica routing, etc...
