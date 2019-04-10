#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import random
import copy
from fifi_simple_api import B,B4,B8,B16
import numpy as np
import json
from encoder_fast import encodertest_SW,encodertest_BBased
from decoder_fast import UnpackenPacket
import matplotlib.pyplot as plt
import numpy as np
import gc
import time


def timeGain():
    
    seed = 2
    rand = random.Random(seed)
    
    num_packets = 500 #200 # 20000
    maxSize_packet = 1500  # 1500
    fixPacketmaxSize = 50
    # generation_size = 8

    # field_group = [B,B4,B8,B16]
    field = B8

    # GS = [2,4,8,16,32,64]
    GS = [2,4,8,16,32,64]
    # GS = [2]
    
    encoder_native = []
    encoder_zeropp = []

    decoder_native = []
    decoder_zeropp = []

    codedRatePacket = 1
    error = 0.5
    
    for i,generation_size in enumerate(GS):
        encoder_native.append([])
        encoder_zeropp.append([])
        
        decoder_native.append([])
        decoder_zeropp.append([])
        
        # if generation_size == 2:
        #     encoder_native[i].append(0)
        # else:
        #     for _ in range(10):

        #         t0 = time.time()
        #         #list_packets=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        #         encodertest_SW(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        #         deltaT = time.time() - t0
        #         encoder_native[i].append(deltaT)
        #         print "time of BlockBased:",deltaT
        #         ## BB_Coding Time: BlockBased 2380.42835307:15000_maxSize_1500_FixSize_50

        for _ in range(10):

            t0 = time.time()
            encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
            deltaT = time.time() - t0
            encoder_native[i].append(deltaT)
            print "time of BlockBased:",deltaT
            ## BB_Coding Time: BlockBased 2380.42835307:15000_maxSize_1500_FixSize_50


            # list_packets_zp=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            
            # Decoder = UnpackenPacket(field,generation_size,num_packets)
            # t0 = time.time()
            # for packet in list_packets:
            #     if rand.random() >error:
            #         Decoder.unpacken(packet,checkString="BBased")

            # deltaT = time.time() - t0
            # decoder_native[i].append(deltaT)
            # gc.collect()

            t0 = time.time()
            # list_packets_zp=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            deltaT = time.time() - t0
            encoder_zeropp[i].append(deltaT)
            print "time of SlidingWindow:",deltaT
            # BB_Coding Time: BlockBasedZero 3816.53170896:15000_maxSize_1500_FixSize_50
            
            #Decoder_zp = UnpackenPacket(field,generation_size,num_packets)
            #t0 = time.time()
            #for packet_zp in list_packets_zp:
            #    if rand.random() >error:
            #        Decoder_zp.unpacken(packet_zp,checkString="BBased")
            #deltaT = time.time() - t0
            #decoder_zeropp.append(deltaT)
        
            #gc.collect()
            # Decoder.reset()
            # Decoder_zp.reset()
            

    error_rate=[encoder_native,decoder_native,encoder_zeropp,decoder_zeropp]
    
    fileName = "20times BB packets:"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"_AddPacket_"+str(codedRatePacket)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)
    


def BBShow():
    GS = [2,4,8,16,32,64]
    num_packets = 500#200# 12800 # 20000
    maxSize_packet = 1500  # 1500
    fixPacketmaxSize = 50
    time1 = 2380.42835307
    time2 = 3816.53170896 
    codedRatePacket=1
    fileName1 = "BB_Coding Time: BlockBased "+str(time1)+":"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)
    fileName2 = "BB_Coding Time: BlockBasedZero "+str(time2)+":"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)


    fileName = "20times BB packets:"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"_AddPacket_"+str(codedRatePacket)
    with open("./json/"+fileName+".json","r") as outfile:
        result = json.load(outfile)

    print result

    BBnative = result[0] 
    BBzeropp = result[2]
    # mean = [np.mean(BBnative4[i]) for i in range(len(BBnative4))]
    # mean_std = [np.std(BBnative4[i]) for i in range(len(BBnative4))]

    # ==========================================================
    #with open('./json/'+ fileName1 + '.json','r') as outfile:
     #   BBnative=json.load(outfile)[0]

    #with open('./json/'+ fileName2 + '.json','r') as outfile:
    #    BBzeropp=json.load(outfile)[2]
    
   # BBnative[1]=BBnative4

    #fileName = "BB native packets "+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)
    #with open("./json/"+fileName+".json","w") as infile:
    #    json.dump(BBnative,infile)

    itemNum = len(BBnative)
    Mean_BBnative = [np.mean(BBnative[i]) for i in range(itemNum)]
    Deviation_BBnative = [np.std(BBnative[i]) for i in range(itemNum)]

    itemNum = len(BBzeropp)
    Mean_BBzeropp = [np.mean(BBzeropp[i]) for i in range(itemNum)]
    Deviation_BBzeropp = [np.std(BBzeropp[i]) for i in range(itemNum)]
    
    

    print BBnative
    print BBzeropp
    
    ind = np.arange(len(GS))
    width = 0.35

    fig, ax = plt.subplots(2,1)
    p1 = ax[0].bar(ind - width/2,Mean_BBnative,width,yerr=Deviation_BBnative,label="Native Packets")
    p2 = ax[0].bar(ind + width/2,Mean_BBzeropp,width,yerr=Deviation_BBzeropp,label="Zeropadding Packets")

    ax[0].set_title("Encoder Time Gain: "+str(num_packets)+" pakcets, "+str(maxSize_packet)+" bytes, GaloisField 8, Random 30 times")
    ax[0].set_xticks(ind)
    ax[0].set_xticklabels([ "GS "+str(GS[i]) for i in range(len(GS))])
    # ax[0].set_xticklabels(('GS 2','GS 4','GS 8','GS 16'))
    ax[0].set_ylabel("Run times (sec)")
    ax[0].set_yticks(np.arange(0,2,0.5))
    ax[0].legend()

    ax[1].plot(ind,Mean_BBnative,color='IndianRed',marker='*',label="Native Packets")
    ax[1].plot(ind,Mean_BBzeropp,color='SkyBlue',marker='x',label="Zeropadding Packets")
    ax[1].set_xticks(ind)
    ax[0].set_xticklabels([ "GS "+str(GS[i]) for i in range(len(GS))])
    ax[1].set_yticks(np.arange(0,2,0.5))
    ax[1].legend()

    plt.savefig('./json/'+fileName+".png")
    plt.show()

def packets200():
    GS = [2,4,8,16]
    num_packets = 15000 # 20000
    maxSize_packet = 1500  # 1500
    fixPacketmaxSize = 50
    
    fileName = "BB_Coding Time: BBnativ G4:"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)
    
    with open("./json/"+fileName+".json","r") as outfile:
        BBnative = json.load(outfile)[0]

    print BBnative
    mean = [np.mean(BBnative[i]) for i in range(len(BBnative))]
    mean_std = [np.std(BBnative[i]) for i in range(len(BBnative))]

    ind = np.arange(len(GS))
    fig, ax = plt.subplots()
    p1 = ax.bar(ind,mean,width=0.35, yerr=mean_std,label="BBnative packet")
    ax.set_xticks(ind)
    ax.set_xticklabels(('GS2','GS4','GS8','GS16'))
    ax.legend()
    plt.show()
    
    

if __name__=="__main__":
    
    # test3()
    
    # packets200()
    # time.sleep(30)
    BBShow()
    # timeGain()
