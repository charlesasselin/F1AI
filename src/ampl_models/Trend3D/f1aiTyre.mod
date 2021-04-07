set tyres;
set laps;
set stints;
param tyreLifeSpan;
param totalLaps;
param pitTime;
param usage{c in tyres, s in stints};
param avg{c in tyres};
param coeff{c in tyres};
var time {c in tyres, s in stints};
var compound {c in tyres, s in stints, l in laps} binary;
var pit {c in tyres, l in laps} binary;

minimize z: sum{c in tyres, s in stints, l in laps} time[c,s] * compound[c,s,l] + sum{c in tyres, l in laps} pitTime * pit[c,l];

subject to ApproxTime{c in tyres, s in stints}: time[c,s] = usage[c,s]*coeff[c]+avg[c];
subject to GottaLap {l in laps}: sum{c in tyres, s in stints} compound[c,s,l] = 1;
subject to StartRace: sum{c in tyres} compound[c,1,1] = 1;
subject to UniqueLap {c in tyres, s in stints}: sum{l in laps} compound[c,s,l] <= 1;
subject to PitStop{c in tyres, l in laps, b in 1..totalLaps-1}: pit[c,b] >= sum{s in stints} compound[c,s,b] - sum{s in stints} compound[c,s,b+1];
subject to PitRestrictions: sum{c in tyres, l in laps} pit[c,l] >= 1;
subject to TrackEvolution {c in tyres, a in 1..tyreLifeSpan-1, b in 1..totalLaps-1}: compound[c,a+1,b+1] <= 999 * compound[c,a,b];
