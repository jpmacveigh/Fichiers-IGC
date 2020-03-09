def deltaCap(capBefore,capAfter):
    assert 0.<=capBefore<= 360. and 0.<=capAfter<=360.,(capBefore,capAfter)
    rep=(capAfter-capBefore)%360.
    if rep >=180. : rep=rep-360.
    return (rep)
"""
capBefore=140.
capAfter=320.
print ("de: "+str(capBefore)+" vers: "+str(capAfter)+" rotation de: "+str(deltaCap(capBefore,capAfter)))

"""