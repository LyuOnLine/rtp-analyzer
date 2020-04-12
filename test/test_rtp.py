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


    parser = argparse.ArgumentParser(description="pack parser and dump tool")
    parser.add_argument("mp4file", help="mp4 full pathname", nargs="+")
    args = parser.parse_args()
    mp4file = args.mp4file

    for f in mp4file:
        package = rtp.RTP.parse_file(f)
        print("%s : " % (os.path.basename(f)) + briefInfo(package) + "size = %d" % (os.stat(f).st_size))
