rs.initiate({_id: "cfgrs", configsvr: true, members:[{ _id: 0, host: "cfgsvr1:27017" }]}) // cfgsrv 
rs.initiate({_id: "shard1rs",members: [{ _id : 0, host : "shard1svr1:27017" },{ _id : 1, host : "shard1svr2:27017" },{ _id : 2, host : "shard1svr3:27017" }]})
rs.initiate({_id: "shard2rs",members: [{ _id : 0, host : "shard2svr1:27017" },{ _id : 1, host : "shard2svr2:27017" },{ _id : 2, host : "shard2svr3:27017" }]})

// access to mongo_router
// mongosh <url mongo_router>
sh.status()
sh.addShard("shard1rs/shard1svr1:27017,shard1svr2:27017,shard1svr3:27017")
sh.addShard("shard2rs/shard2svr1:27017,shard2svr2:27017,shard2svr3:27017")
sh.enableSharding("BIGDATA")
sh.shardCollection("BIGDATA.movie", { id: 'hashed' })
sh.shardCollection("BIGDATA.actor", { id: 'hashed' })

// use movie
// db.movie.deleteMany({})

// use actor
// db.actor.deleteMany({})

/* read the explan plan in compass
https://www.mongodb.com/docs/upcoming/reference/explain-results/?utm_source=compass&utm_medium=product#mongodb-data-explain.executionStats
Stages are descriptive of the operation. For example:

COLLSCAN for a collection scan

IXSCAN for scanning index keys

FETCH for retrieving documents

GROUP for grouping documents

SHARD_MERGE for merging results from shards

SHARDING_FILTER for filtering out orphan documents from shards

BATCHED_DELETE for multiple document deletions that are batched together internally (starting in MongoDB 6.1)
*/