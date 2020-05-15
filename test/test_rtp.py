#!/usr/bin/env python
import sys
import os
sys.path.append(os.getcwd())
import rtp
import argparse

if __name__ == '__main__':
    def briefInfo(pack):
        str = ""
        str += "timestamp = %d " % (pack.header.timestamp)
        str += "number = %d " % (pack.header.number)
        str += "payloadType = %s " % (pack.header.flag.type)
        typeStr = "type = %s " % (pack.nalu.indicator.type)
        if pack.nalu.indicator.type == rtp.NaluH264TypeWithFU.FU_A:
            typeStr = "type = %s:%s " % (pack.nalu.indicator.type, pack.nalu.payload.header.type)
            str += "isSegmented = %d " % (pack.nalu.payload.header.isSegmented)
            str += "isLastSegment = %d " % (pack.nalu.payload.header.isLastSegment)
        elif pack.nalu.indicator.type == rtp.NaluH264TypeWithFU.STAP_A:
            typeStr = "type = %s:[%s] " % (
            pack.nalu.indicator.type, "".join("%s," % s.header.type for s in pack.nalu.payload.packets)[:-1])
        return str + typeStr

    parser = argparse.ArgumentParser(description="rtp parser and dump tool")
    parser.add_argument("rtpfile", nargs="+", help="""support rtpdump file or packet dump files:
            RtpDump file:   full pathname of rtpdump file.
            paket dumpe files:  multiple files of rtp packet dumped. such as: /tmp/rtp*.dat
        """)
    args = parser.parse_args()
    rtpfile = args.rtpfile

    for f in rtpfile:
        _, ext = os.path.splitext(f)
        if ext == ".rtpdump":
            print("[RTPDUMP] " + f)
            rtpdump = rtp.RtpDumpFile.parse_file(f)
            for p in rtpdump.packets:
                package = rtp.RTP.parse(bytearray(p.data))
                print("%s : " % briefInfo(package) + "size = %d" % (p.length - 8))
        else:
            package = rtp.RTP.parse_file(f)
            print("%s : " % (os.path.basename(f)) +
                  briefInfo(package) + "size = %d" % (os.stat(f).st_size))
