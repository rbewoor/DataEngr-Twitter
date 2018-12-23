# DataEngr-Twitter
3 versions of the producer scripts: combination with or without filters, runnig forever or fixed time (see comments at beginning of the code)
Problems being faced: When I run producer (no filter+fixed time) it pull. Then I ran the consumer and it also wrote to MongoDb. But I
found blank records. E.g. out of total of 10k odd mongo docs inserted, there were about 1k with blanks. Dunno why its happening.

Consumer is still the same standard one.

Some examples of simple mongo data access to see how the data can be accessed.

Queries.txt has 5 simple queries that are currently coded in native MongoDB shell execution. Need to figure out how to run this via a python program.
