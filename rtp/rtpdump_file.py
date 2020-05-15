#!/usr/bin/env python

from construct import *

###############################################################################
# rtpdump file parser.
#   Reference: http://web4.cs.columbia.edu/irt/software/rtptools/
###############################################################################
RtpDumpHeader = Struct(
    "tv_sec" / Int32ub,
    "tv_usec" / Int32ub,
    "source" / Int32ub,
    "port" / Int16ub,
    "padding" / Int16ub,
)
RtpDumpPacket = Struct(
    "length" / Int16ub,
    "plen" / Int16ub,
    "time_offset" / Int32ub,
    "data" / Array(this.length - 8, Byte),
)
RtpDumpFile = Struct(
    "start_line" / NullTerminated(Byte, term=b"\x0a"),
    "header" / RtpDumpHeader,
    "packets" / GreedyRange(RtpDumpPacket),
)
