###############################################################################
# Helpers
###############################################################################
db = {}
def ccoreDump(msg):
    # dump a CommuniCore message to stdout and remember the last value we saw
    # in an in memory database
    global db
    print "path: %s %s %s from: %s" % ( msg.path, type(msg.data), msg.data, msg.source )
    db[msg.path]=msg.data

###############################################################################
# CCore
###############################################################################

# Uses DEFAULT CONFIGURATION on DEFAULT INTERFACE (see ../Readme)

import CCore
tcore = CCore.CCore(pubsub="osc-udp:") # use default bidirectional multicast
tcore.subscribe("default", ccoreDump)	# catch all 
