# DataEngr-Twitter
3 versions of the producer scripts: combination with or without filters, runnig forever or fixed time (see comments at beginning of the code)
Problems being faced: When I run producer (no filter+fixed time) it pull. Then I ran the consumer and it also wrote to MongoDb. But I
found blank records. E.g. out of total of 10k odd mongo docs inserted, there were about 1k with blanks. Dunno why its happening.

Consumer is still the same standard one.

Some examples of simple mongo data access to see how the data can be accessed.

Queries.txt has 5 simple queries that are currently coded in native MongoDB shell execution. Need to figure out how to run this via a python program.

PROBLEM FOUND with the way the first 24 hours was read. Simply reading first 316569 messages (discarding the first two as header and blank info) has inserted 316567 docs into mongo. But the dates are outside the PUTime of gte=2018-06-01 00:00:00 and lt=2018-06-02 00:00:00. Only 316188 docs meet this condition. Will need to change consumer to check the date range before proceeding to insert.
> db.TestNYTFullJuneButOnly24hrsCol1.count()
316567
> db.TestNYTFullJuneButOnly24hrsCol1.find({},{_id:0, tpep_pickup_datetime: 1, tpep_dropoff_datetime: 1}).sort({tpep_pickup_datetime: 1}).limit(5)
{ "tpep_pickup_datetime" : "2008-12-31 13:51:38", "tpep_dropoff_datetime" : "2008-12-31 14:21:38" }
{ "tpep_pickup_datetime" : "2009-01-01 17:22:13", "tpep_dropoff_datetime" : "2009-01-01 18:05:13" }
{ "tpep_pickup_datetime" : "2018-05-31 06:08:31", "tpep_dropoff_datetime" : "2018-05-31 06:18:15" }
{ "tpep_pickup_datetime" : "2018-05-31 06:33:15", "tpep_dropoff_datetime" : "2018-05-31 06:35:36" }
{ "tpep_pickup_datetime" : "2018-05-31 06:40:08", "tpep_dropoff_datetime" : "2018-05-31 06:45:04" }
> db.TestNYTFullJuneButOnly24hrsCol1.find({},{_id:0, tpep_pickup_datetime: 1, tpep_dropoff_datetime: 1}).sort({tpep_pickup_datetime: -1}).limit(5)
{ "tpep_pickup_datetime" : "2018-06-02 23:49:30", "tpep_dropoff_datetime" : "2018-06-03 00:00:35" }
{ "tpep_pickup_datetime" : "2018-06-02 23:42:15", "tpep_dropoff_datetime" : "2018-06-02 23:55:21" }
{ "tpep_pickup_datetime" : "2018-06-02 23:39:02", "tpep_dropoff_datetime" : "2018-06-03 00:05:32" }
{ "tpep_pickup_datetime" : "2018-06-02 23:24:21", "tpep_dropoff_datetime" : "2018-06-02 23:38:11" }
{ "tpep_pickup_datetime" : "2018-06-02 23:16:16", "tpep_dropoff_datetime" : "2018-06-02 23:21:04" }
> db.TestNYTFullJuneButOnly24hrsCol1.find( {"tpep_pickup_datetime": {$gte: "2018-06-01 00:00:00", $lt: "2018-06-02 00:00:00"}} ).count()
316188
> db.TestNYTFullJuneButOnly24hrsCol1.find().count()
316567
