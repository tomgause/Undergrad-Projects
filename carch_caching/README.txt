RESULTS

Direct Mapped Simulation, small
    hits = 86873
    misses = 18179
    hit rate = 82.695237%

Direct Mapped Simulation, large
    hits = 15418817
    misses = 1204740
    hit rate = 92.752815%

Fully Associative Simulation, small
    hits = 100964
    misses = 4088
    hit rate = 96.108594%

Fully Associative Simulation, large
    hits = 16536483
    misses = 87074
    hit rate = 99.476201%

Set Mapped Simulation, small
    hits = 103009
    misses = 2043
    hit rate = 98.055249%

Set Mapped Simulation, large
    hits =  16599721
    misses = 23836
    hit rate = 99.856613%

INSTRUCTIONS

$ gcc -o directmapped directmapped.c
$ gcc -o fullyassociative fullyassociative.c
$ gcc -o setassociative setassociative.c

$ gcc ./directmapped < small
$ gcc ./directmapped < large
$ gcc ./fullyassociative < small
$ gcc ./fullyassociative < large
$ gcc ./setassociative < small
$ gcc ./setassociative < large
