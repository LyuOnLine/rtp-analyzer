#!/usr/bin/env python

from construct import *

################################################################################################
# Rtp header parser
#   Reference: [RFC1889](https://tools.ietf.org/html/rfc1889)
################################################################################################
RTPPayloadType = Enum(BitsInteger(7),
                      PCMU=0,
                      GSM=3,
                      G723=4,
                      DVI4_8000=5,
                      DVI4_16000=6,
                      LPC=7,
                      PCMA=8,
                      G722=9,
                      L16_2chan=10,
                      L16_1chan=11,
                      QCELP=12,
                      CN=13,
                      MPA=14,
                      G728=15,
                      DVI4_11025=16,
                      DVI4_22050=17,
                      G729=18,
                      CelB=25,
                      JPEG=26,
                      nv=28,
                      H261=31,
                      MPV=32,
                      MP2T=33,
                      H263=34,
                      Dynamic_h264=96,
                      )

RTPHeaderExtension = Struct(
    "id" / Int32ub,
    "length" / Int16ub,
    "content" / Bytes(this.length)
)

RTPHeader = Struct(
    "flag" / BitStruct(
        "version" / BitsInteger(2),
        "hasPadding" / Flag,
        "hasExtension" / Flag,
        "csrcNumber" / Nibble,
        "marker" / Flag,
        "type" / RTPPayloadType,
    ),
    "number" / Int16ub,
    "timestamp" / Int32ub,
    "ssrc" / Int32ub,
    "csrc" / If(this.flag.csrcNumber > 0, Array(this.flag.csrcNumber, Int32ub)),
    "extenstion" / If(this.flag.hasExtension, RTPHeaderExtension)
)

################################################################################################
# Rtp payload for h264
#   Reference: [rfc6184](https://datatracker.ietf.org/doc/rfc6184/)
################################################################################################
NaluH264Type = Enum(BitsInteger(5),
                    PFrame=1,
                    PartitionA=2,
                    PartitionB=3,
                    PartitionC=4,
                    IFrame=5,
                    SEI=6,
                    SPS=7,
                    PPS=8,
                    UnitDelimiter=9,
                    EndOfSequnce=10,
                    EndOfStream=11,
                    FilterData=12,
                    SPSExtension=13,
                    PrefixNalUnit=14,
                    SubsetSPS=15,
                    SliceWithoutPartion=19,
                    SliceScalableExtenstion=20,
                    )

NaluH264TypeWithFU = Enum(BitsInteger(5),
                          PFrame=1,
                          PartitionA=2,
                          PartitionB=3,
                          PartitionC=4,
                          IFrame=5,
                          SEI=6,
                          SPS=7,
                          PPS=8,
                          UnitDelimiter=9,
                          EndOfSequnce=10,
                          EndOfStream=11,
                          FilterData=12,
                          SPSExtension=13,
                          PrefixNalUnit=14,
                          SubsetSPS=15,
                          SliceWithoutPartion=19,
                          SliceScalableExtenstion=20,
                          STAP_A=24,
                          STAP_B=25,
                          MTAP16=26,
                          MTAP24=27,
                          FU_A=28,
                          FU_B=29,
                          )

FUIndicator = BitStruct(
    "isSegmented" / Flag,
    "importance" / BitsInteger(2),
    "type" / NaluH264TypeWithFU,
)

##############################################
# NALU for not segmented
##############################################
# todo: pps/sps parser.
Packet = Struct(
    "header" / FUIndicator,
    "data" / GreedyRange(Byte),
)

##############################################
# NALU for aggregated.
##############################################
STAP_A = Struct(
    "packets" / GreedyRange(Prefixed(Int16ub, Packet)),
)

##############################################
# NALU for fragmentated.
##############################################
FUHeader_A = BitStruct(
    "isSegmented" / Flag,
    "isLastSegment" / Flag,
    Padding(1),
    "type" / NaluH264Type,
)
FU_A = Struct(
    "header" / FUHeader_A,
    "data" / GreedyRange(Byte),
)

NALU = Struct(
    "indicator" / FUIndicator,
    "payload" / Switch(this.indicator.type, {
        NaluH264TypeWithFU.FU_A: FU_A,
        NaluH264TypeWithFU.STAP_A: STAP_A,
    })
)

RTP = Struct(
    "header" / RTPHeader,
    "nalu" / NALU,
)
