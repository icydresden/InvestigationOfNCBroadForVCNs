# set number of nodes
set opt(nn) 191

# set activity file
set opt(af) $opt(config-path)
append opt(af) /hangzhou2activitysumo25ms.tcl

# set mobility file
set opt(mf) $opt(config-path)
append opt(mf) /hangzhou2mobilitysumo25ms.tcl

# set start/stop time
set opt(start) 100.0
set opt(stop) 929.0

# set floor size
set opt(x) 4428.95
set opt(y) 4862.48
set opt(min-x) 5.17
set opt(min-y) 4.3

