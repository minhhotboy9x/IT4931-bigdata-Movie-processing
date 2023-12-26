rs.initiate({_id: "cfgrs", configsvr: true, members:[{ _id: 0, host: "cfgsvr1:27017" }]}) // cfgsrv 
rs.initiate({_id: "shard1rs",members: [{ _id : 0, host : "shard1svr1:27017" },{ _id : 1, host : "shard1svr2:27017" },{ _id : 2, host : "shard1svr3:27017" }]})
rs.initiate({_id: "shard2rs",members: [{ _id : 0, host : "shard2svr1:27017" },{ _id : 1, host : "shard2svr2:27017" },{ _id : 2, host : "shard2svr3:27017" }]})
sh.addShard("shard1rs/shard1svr1:27017,shard1svr2:27017,shard1svr3:27017")
sh.addShard("shard2rs/shard2svr1:27017,shard2svr2:27017,shard2svr3:27017")
