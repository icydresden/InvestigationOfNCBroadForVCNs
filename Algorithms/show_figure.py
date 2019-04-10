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

def test1():
    
    fileName = "packets_200_maxSize_10_FixSize_0GenS64"
    with open('./json/'+ fileName + '.json','r') as infile:
        error_rate=json.load(infile)

    print error_rate
    # fig = plt.figure()
    
    GS = [2,4,8,16,32,64]
    x = [item/float(item+1) for item in GS]
    plt.plot(x,error_rate[0],marker='*',label="SBlock")
    plt.plot(x[1:],error_rate[1],marker='x',label="CRLNC")
    plt.legend()
    plt.ylim((0,1.2))
    # plt.xlim((0.3,1))
    plt.title("channel loss 5%"+fileName)
    plt.xlabel("codede rate")
    plt.ylabel("packet loss")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()

def test2():
    fileName =["packets_12000_maxSize_10_FixSize_0GenS64",
               "packets_2000_maxSize_10_FixSize_0GenS64",
               "packets_2000_maxSize_40_FixSize_0GenS64",
               "packets_800_maxSize_40_FixSize_0GenS64",
               "packets_800_maxSize_20_FixSize_0GenS64",
               "packets_200_maxSize_10_FixSize_0GenS64"] 

    error_rate = []
    for fN in fileName:
        
        with open('./json/'+ fN + '.json','r') as infile:
            error_rate.append(json.load(infile))

        # print error_rate
    # fig = plt.figure()
    
    plt.figure()

    GS = [2,4,8,16,32,64]
    x = [item/float(item+1) for item in GS]
    for i in range(len(error_rate)):
        plt.subplot(2,3,i+1)
        plt.plot(x,error_rate[i][0],marker='*',label="SBlock")
        plt.plot(x[1:],error_rate[i][1],marker='x',label="CRLNC")
        plt.legend()
        plt.ylim((0,1.2))
    # plt.xlim((0.3,1))
        plt.title(fileName[i],fontsize=9)
        if i >2:
            plt.xlabel("codede rate")
        if i ==0:
            plt.ylabel("packet get rate")
        if i ==3:
            plt.ylabel("packet get rate")
    
    plt.savefig('./json/'+"zusammen"+".png")
    plt.show()

def test3():
    num_packets = 100
    maxSize_packet = 10
    fixPacketmaxSize = 0
    generation_size = 4

    
    errorSize = 10
    errorFactor = 0.05
    error_rate = []

    numberOfFigure = 4
    # num_ps = num_packets
    field = [B,B4,B8,B16]
    for i in range(numberOfFigure):
        # list_packets=encodertest_CRLNC(field[i],num_packets ,maxSize_packet,fixPacketmaxSize)
        list_packets=encodertest_SBlock(field[i],num_packets ,maxSize_packet,fixPacketmaxSize)
        print list_packets
        error_rate.append([])
        for j in range(0,errorSize):
            print "%%%%%%%"*15," runs", i
            Decoder=UnpackenPacket(field[i],generation_size,num_packets)
            error = 0.1*i
            # error = 0.1
            for packet in list_packets:
                possibility = rand.random()
                if possibility >error:
                    # print "\n data: x",Decoder.unpacken(packet)
                    # print possibility, "?",error
                    Decoder.unpacken(packet)
                else:
                    # print possibility, "?",error
                    pass
            error_rate[i].append(Decoder.decoded_flag.values().count(True) / float(num_packets))

    print error_rate

    fileName = "packets_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)

    print list_packets
    num_ps = num_packets

    # plt.title(fileName)
    # gs = gridspec.GridSpec(numberOfFigure,1)
    fig,axs = plt.subplots(numberOfFigure,1)
    plt.tight_layout(pad=0.4,w_pad=0.5,h_pad=1.0)
    for i in range(numberOfFigure):
        
        fileN_temp = "sended packets: "+str(field[i])
        x = np.linspace(0,errorSize*errorFactor,len(error_rate[i]))
        axs[i].plot(x,error_rate[i],x,1-x,'r')
        axs[i].set_title(fileN_temp,fontsize=9)
    # fig = plt.figure()
    # plt.plot(error_rate)
    # plt.axis([0,errorSize,1,100])
    
    plt.xlabel("errors")
    # plt.ylabel("received rate")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()

def test4():
    num_packets = 5000
    maxSize_packet = 1800
    fixPacketmaxSize = 0
    generation_size = 4

    
    errorSize = 10
    errorFactor = 0.05
    error_rate = []

    numberOfFigure = 4
    # num_ps = num_packets
    error_CRLNC = []
    error_SBlock = []
    list_packets_CRLNC = []
    list_packets_SBlock = []

    field = [B,B4,B8,B16]
    for i in range(numberOfFigure):
        list_packets_CRLNC.append(encodertest_CRLNC(field[i],num_packets ,maxSize_packet,fixPacketmaxSize))
        list_packets_SBlock.append(encodertest_SBlock(field[i],num_packets ,maxSize_packet,fixPacketmaxSize))

        error_CRLNC.append([])
        error_SBlock.append([])

        # for j in range(0,errorSize):
        print "%%%%%%%"*15," runs", i
        Decoder_CRLNC=UnpackenPacket(field[i],generation_size,num_packets)
        Decoder_SBlock=UnpackenPacket(field[i],generation_size,num_packets)
        error = 0.5
        # error = 0.1
        for packet in list_packets_CRLNC:
            possibility = rand.random()
            if possibility >error:
                # print "\n data: x",Decoder.unpacken(packet)
                print possibility, "?",error
                Decoder_CRLNC.unpacken(packet)
            else:
                print possibility, "?",error
                pass
        error_CRLNC[i].append(Decoder_CRLNC.decoded_flag.values().count(True) / float(num_packets))

        for packet in list_packets_SBlock:
            possibility = rand.random()
            if possibility >error:
                # print "\n data: x",Decoder.unpacken(packet)
                # print possibility, "?",error
                Decoder_SBlock.unpacken(packet)
            else:
                # print possibility, "?",error
                pass
        error_SBlock[i].append(Decoder_SBlock.decoded_flag.values().count(True) / float(num_packets))


    for i in range(numberOfFigure):
        error_rate.append([])
        # for j in range(numberOfFigure):
        error_rate[i].append(error_CRLNC[i])
        error_rate[i].append(error_SBlock[i])

    fileName = "error_"+ str(error)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)

    x = np.linspace(0,1,len(error_rate[0]))
    plt.plot(x,error_rate[0],'b',x,error_rate[1],'g')
    
    
    plt.xlabel("Coded Rate")
    plt.ylabel("packets loss")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()

def test5():
    num_packets = 100
    maxSize_packet = 10
    fixPacketmaxSize = 0
    generation_size = 4

    
    errorSize = 10
    errorFactor = 0.05
    error_rate = []

    numberOfFigure = 4
    # num_ps = num_packets
    field = [B,B4,B8,B16]
    for i in range(numberOfFigure):
        # list_packets=encodertest_CRLNC(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        list_packets=encodertest_SBlock(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        print list_packets
        error_rate.append([])
        
        print "%%%%%%%"*15," runs", i
        Decoder=UnpackenPacket(field[i],generation_size,num_packets)
        error = 0.5
        # error = 0.1
        for packet in list_packets:
            possibility = rand.random()
            if possibility >error:
                # print "\n data: x",Decoder.unpacken(packet)
                # print possibility, "?",error
                Decoder.unpacken(packet)
            else:
                # print possibility, "?",error
                pass
        error_rate[i].append(Decoder.decoded_flag.values().count(True) / float(num_packets))

   

    error_rate1=[]
    for i in range(numberOfFigure):
        # list_packets=encodertest_CRLNC(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        list_packets=encodertest_CRLNC(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        print list_packets
        error_rate1.append([])
        
        print "%%%%%%%"*15," runs", i
        Decoder=UnpackenPacket(field[i],generation_size,num_packets)
        error = 0.2
        # error = 0.1
        for packet in list_packets:
            possibility = rand.random()
            if possibility >error:
                # print "\n data: x",Decoder.unpacken(packet)
                # print possibility, "?",error
                Decoder.unpacken(packet,"CRLNC")
            else:
                # print possibility, "?",error
                pass
        error_rate1[i].append(Decoder.decoded_flag.values().count(True) / float(num_packets))
    

    fileName = "packets_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)

    print error_rate
    print error_rate1

    t=[0.6, 0.8]
    plt.plot(t,[error_rate[0],error_rate1[0]],marker='x',label='B')
    plt.plot(t,[error_rate[1],error_rate1[1]],marker='o',label='B4')
    plt.plot(t,[error_rate[2],error_rate1[2]],marker='<',label='B8')
    plt.plot(t,[error_rate[3],error_rate1[3]],marker='>',label='B16')
    plt.legend()
    
    
    plt.axis([0,1.0,0,1.0])
    plt.title("test")
    plt.xlabel("codede rate")
    plt.ylabel("loss rate")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()
      
def test6():
    num_packets = 100
    maxSize_packet = 10
    fixPacketmaxSize = 0
    generation_size = 4

    
    errorSize = 10
    errorFactor = 0.05
    

    numberOfFigure = 4

    Packetmaxlength = 0
    GS = [2,4,8,16,32,64]
    # field = B8
    error_rate = []
    field_group = [B,B4,B8,B16]
    for field in field_group:
        
        error_SBlock = []
        for generation_size in GS:
            list_packets=encodertest_SBlock(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
            # list_packets=encodertest_CRLNC(B8,generation_size,num_packets = 10,maxSize_packet=18,fixPacketmaxSize=0)
            print list_packets
            
            Decoder=UnpackenPacket(field,generation_size,num_packets)
            error = errorFactor
            # error = 0.1
            for packet in list_packets:
                possibility = rand.random()
                if possibility >error:
                    # print "\n data: x",Decoder.unpacken(packet)
                    # print possibility, "?",error
                    Decoder.unpacken(packet,checkString="SBlock")
                else:
                    # print possibility, "?",error
                    pass
            # temp_datum = math.log10(Decoder.decoded_flag.values().count(True) / float(num_packets))
            temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            error_SBlock.append(temp_datum)

            # print "error_rate:",error_CRLNC

        # GS = [4,8,16,32,64]

        error_CRLNC=[]
        for generation_size in GS[1:]:
            # list_packets=encodertest_CRLNC(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
            list_packets=encodertest_CRLNC(field,generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
            print list_packets
            # error_rate1.append([])
            
            print "%%%%%%%"*15," runs"
            Decoder=UnpackenPacket(field,generation_size,num_packets)
            error = 0.05
            # error = 0.1
            for packet in list_packets:
                possibility = rand.random()
                if possibility >error:
                    # print "\n data: x",Decoder.unpacken(packet)
                    # print possibility, "?",error
                    Decoder.unpacken(packet,"CRLNC")
                else:
                    # print possibility, "?",error
                    pass
            error_CRLNC.append(Decoder.decoded_flag.values().count(True) / float(num_packets))
    
        error_rate.append([error_SBlock, error_CRLNC])

    fileName = "B-B16 packets_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)
    # print error_rate1
   
    GS = [2,4,8,16,32,64]
    t = [g/float(g+1) for g in GS]
    for i in range(len(error_rate)):
        
        plt.plot(t,error_rate[i][0],marker='*',label='SBlock '+ str(field_group[i]))
        plt.plot(t[1:],error_rate[i][1],marker='x',label="CRLNC "+ str(field_group[i]))
    # plt.plot(t,[error_rate[1],error_rate1[1]],marker='o',label='B4')
    # plt.plot(t,[error_rate[2],error_rate1[2]],marker='<',label='B8')
    # plt.plot(t,[error_rate[3],error_rate1[3]],marker='>',label='B16')
    
    plt.legend()
    
    plt.ylim((0,1))
    # plt.xlim((0.3,1))
    plt.title("channel loss 5%"+fileName)
    plt.xlabel("codede rate")
    plt.ylabel("packet get rate")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()
    
def test7():
    num_packets = 200
    maxSize_packet = 100
    fixPacketmaxSize = 50

    GS = [2,4,8,16,32,64]
    GS = [4,8,16]

    generation_size = 8
    
    errorSize = 9
    errorFactor = 0.1

    numberOfFigure = 4

    Packetmaxlength = 0
    
    error_rate = []
    field_group = [B,B4,B8,B16]
    field = B8
    
    Decoder=UnpackenPacket(field,generation_size,num_packets)
    Decoder_zp = UnpackenPacket(field,generation_size,num_packets)
    
    
    error_SBlock = []
    error_SBlock_zp = []
    for i in range(1,errorSize):    
        error = errorFactor * i
        list_packets=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        # list_packets_zp=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
        list_packets_zp=encodertest_SW(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)

        # list_packets=encodertest_CRLNC(B8,generation_size,num_packets = 10,maxSize_packet=18,fixPacketmaxSize=0)
        # print list_packets,'\n',list_packets_zp

        # error = 0.1
        for packet,packet_zp in zip(list_packets,list_packets_zp):
        # for packet in list_packets:    
            possibility = rand.random()
            if possibility >error:
                # print "\n data: x",Decoder.unpacken(packet)
                # print possibility, "?",error
                Decoder.unpacken(packet,checkString="BBased")
                Decoder_zp.unpacken(packet_zp,checkString="SW")
            else:
                # print possibility, "?",error
                pass

        # temp_datum = math.log10(Decoder.decoded_flag.values().count(True) / float(num_packets))
        temp_datum = Decoder.decoded_flag.values().count(False) / float(num_packets)
        error_SBlock.append(temp_datum)
        Decoder.reset()

        temp_datum = Decoder_zp.decoded_flag.values().count(False)/float(num_packets)
        error_SBlock_zp.append(temp_datum)
        Decoder_zp.reset()
        # print "**"*15
        # print "error_SBlock:",error_SBlock
        error_rate.append([error_SBlock,error_SBlock_zp])
        # error_rate.append([error_SBlock])

    # print "error_rate:",error_rate

        # GS = [4,8,16,32,64]

        # error_CRLNC=[]
        # for generation_size in GS[1:]:
        #     # list_packets=encodertest_CRLNC(field[i],generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        #     list_packets=encodertest_CRLNC(field,generation_size,num_packets ,maxSize_packet,fixPacketmaxSize)
        #     print list_packets
        #     # error_rate1.append([])
            
        #     print "%%%%%%%"*15," runs"
        #     Decoder=UnpackenPacket(field,generation_size,num_packets)
        #     error = 0.05
        #     # error = 0.1
        #     for packet in list_packets:
        #         possibility = rand.random()
        #         if possibility >error:
        #             # print "\n data: x",Decoder.unpacken(packet)
        #             # print possibility, "?",error
        #             Decoder.unpacken(packet,"CRLNC")
        #         else:
        #             # print possibility, "?",error
        #             pass
        #     error_CRLNC.append(Decoder.decoded_flag.values().count(True) / float(num_packets))
    
        # error_rate.append([error_SBlock, error_CRLNC])

    

    fileName = "B-B16 packets_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)
    print error_rate
   
    # t = [g/float(g+1) for g in GS]
    # for i in range(len(error_rate)):
        
    #     plt.plot(t,error_rate[i][0],marker='*',label='SBlock '+ str(field_group[i]))
    #     plt.plot(t,error_rate[i][1],marker='x',label="SBlock_zp "+ str(field_group[i]))

    
    # t = np.arange(len(error_rate))
    markter = ['o','<','*','>','.','+','x']
    for i in range(len(GS)):
        
        # temp_d = [error_rate[i][0][j] for j in range(len(error_rate)) ]
        temp_d = error_rate[i][0]
        t=np.linspace(0,1,len(temp_d))
        plt.plot(t,temp_d,marker=markter[i],label='BB GS:'+str(GS[i]))
        # plt.yscale('log')
        # temp_d = [error_rate[i][1][j] for j in range(len(error_rate)) ]
        temp_d = error_rate[i][1]
        t=np.linspace(0,1,len(temp_d))
        plt.plot(t,temp_d,marker=markter[i+2],label='BB-ZP GS:'+str(GS[i]))

    
    plt.legend()
    
    plt.ylim((-0.1,0.99))
    # plt.xlim((0.3,1))
    plt.title("channel loss 5%"+fileName)
    plt.xlabel("codede rate")
    plt.ylabel("loss rate")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()

def test8():
    num_packets = 1000
    maxSize_packet = 50
    fixPacketmaxSize = 50
    generation_size = 8

    fileName = "B-B16 packets_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./json/'+ fileName + '.json','r') as outfile:
        error_rate=json.load(outfile)
    print error_rate
   
    GS = [2,4,8,16,32,64]
    # t = [g/float(g+1) for g in GS]
    # for i in range(len(error_rate)):
        
    #     plt.plot(t,error_rate[i][0],marker='*',label='SBlock '+ str(field_group[i]))
    #     plt.plot(t,error_rate[i][1],marker='x',label="SBlock_zp "+ str(field_group[i]))

    # t=np.linspace(0,1,len(error_rate))
    t = np.arange(len(error_rate))
    markter = ['o','<','>','*','.','+','x']
    k = 0
    for i in range(len(GS[0:4])):
        
        temp_d = [error_rate[j][0][i] for j in range(len(error_rate)) ]

        plt.plot(temp_d,marker=markter[k % len(markter)],label='SB GS:'+str(GS[i]))
        k += 1
        plt.yscale('log')
        temp_d = [error_rate[j][1][i] for j in range(len(error_rate)) ]
        plt.plot(temp_d,marker=markter[k % len(markter)],label='SB-ZP GS:'+str(GS[i]))
        # plt.yscale('log')
        k += 1
    plt.legend()
    
    # plt.ylim((0,1.1))
    # plt.xlim((0.3,1))
    plt.title("channel loss 5%"+fileName)
    plt.xlabel("codede rate")
    plt.ylabel("loss rate")
    
    plt.savefig('./json/'+fileName+".png")
    plt.show()
     

def lossRate():
    
    seed = random.randint(1,255)
    rand = random.Random(seed)
    
    num_packets = 40 #200 # 20000
    maxSize_packet = 50  # 1500
    fixPacketmaxSize = 0
    generation_size = 8

    # field_group = [B,B4,B8,B16]
    field = B8

    GS = [2,4,8,16,32,64]
    # GS = [2,4,8,16]
    GS = [8]

    codedRatePacket = 2
    error = np.linspace(0.01,1,10)
    # error=[0.001,0.01,0.1,0.2,0.4]
    error_result=[]
    for codedRatePacket in range(1,5):
        error_BB = []
        # list_packets=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize)
        list_packets=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize)
        print "list_packets:",list_packets
        # result = []
        for i in range(len(error)):        
              
            # error_SBlock_zp = []
            # for codedRatePacket in range(1,generation_size+1):
            
            Decoder = UnpackenPacket(field,generation_size,num_packets)
            for packet in list_packets:
                tempRandom = rand.random()
                
                if tempRandom > error[i]:
                    #print "tempRandom"
                    # Decoder.unpacken(packet,checkString="BBased")
                    Decoder.unpacken(packet,checkString="SW")


            temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            error_BB.append(temp_datum)

            # Decoder.reset()
        # result.append(error_BB)
        error_result.append(error_BB)
            # temp_datum = Decoder_zp.decoded_flag.values().count(False)/float(num_packets)
            # error_SBlock_zp.append(temp_datum)
            # Decoder_zp.reset()



            # t0 = time.time()
            # # list_packets_zp=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            # encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            # deltaT = time.time() - t0
            # encoder_zeropp[i].append(deltaT)
            # print "time of SlidingWindow:",deltaT
            # # BB_Coding Time: BlockBasedZero 3816.53170896:15000_maxSize_1500_FixSize_50
            
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
            

    # error_rate=[encoder_native,decoder_native,encoder_zeropp,decoder_zeropp]
    
    fileName = "CodeRateWithError"
    with open('./CodeRate/'+ fileName + '.json','w') as outfile:
        json.dump(error_result,outfile)
    
    print error_result

def showBB():
    from mpl_toolkits.mplot3d import Axes3D

    GS = [2,4,8,16]
    

    fileName = "CodeRateWithError"
    with open('./CodeRate/'+ fileName + '.json','r') as outfile:
        error_result=json.load(outfile)

    fig = plt.figure()
    ax = []
    for i in range(len(GS)):
        ax.append(fig.add_subplot(221+i, projection = '3d'))



    for i in range(len(GS)):

        yticks = np.arange(0.1,1,0.1)
        for j,error in enumerate(yticks):

            # for j,error in enumerate(yticks):
                ys = error_result[j][i]
                xs = np.arange(1,len(ys)+1)

                ax[i].bar(xs,ys,zs=error,zdir='y',alpha=0.8)


                ax[i].set_xlabel('M <= N')
                ax[i].set_ylabel('error')
                ax[i].set_zlabel('Z')

                ax[i].set_yticks(yticks)
    plt.savefig('./CodeRate/'+ fileName + '.png')
    plt.show()

def showBB1():
    from mpl_toolkits.mplot3d import Axes3D

    GS = [2,4,8,16]
    GS = [8]

    fileName = "CodeRateWithError"
    with open('./CodeRate/'+ fileName + '.json','r') as outfile:
        error_result=json.load(outfile)
    print error_result
    for i in range(len(error_result)):
        plt.plot(error_result[i],label="CP="+str(1+i))
    plt.legend()
    plt.xscale('log')

    plt.savefig('./CodeRate/'+ fileName + '.png')
    plt.show()     

if __name__=="__main__":
    
    lossRate()
    showBB1()
