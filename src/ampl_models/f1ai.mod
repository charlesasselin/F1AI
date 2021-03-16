set tyres;
set laps;
param time {c in tyres, l in laps};
var compound {c in tyres, l in laps} binary;

minimize z: sum{c in tyres, l in laps} time[c,l] * compound[c,l];

subject to CompoundLimits: sum{c in tyres, l in laps} compound[c,l] >= 3;
subject to GottaLap {l in laps}: sum{c in tyres} compound[c,l] = 1;
