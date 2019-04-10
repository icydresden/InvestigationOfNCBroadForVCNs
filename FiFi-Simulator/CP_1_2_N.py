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

num_packets = 128
maxSize_packet = 50
fixPacketmaxSize = 0
generation_size = 8 #8
numCP=1
fileName = "CP_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet) \
                +"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size) \
                +"_NumCP"+str(numCP)

y=np.linspace(0.3,1,10)
errorFactor=[0.001]+list(np.linspace(0.01,0.3,7))+list(1-1/pow(10,y))
# errorFactor=np.linspace(0.01,1,10)

# errorFactor = [0.001, 0.01] + list(np.linspace(0.01,0.1,6)) + list(np.linspace(0.1,1,15))
codedRatePacket = 1
# field = B8
field_group=[B,B4,B8,B16]

def run():
    
    field = B8
    error_rate = []
    
    for codedRatePacket in range(1,numCP+1):

        error_BB = []
        error_BB_zp = []

        error_SW = []
        error_SW_zp = []

        BB_list_packets=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        BB_list_packets_zp=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

        SW_list_packets=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        SW_list_packets_zp=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

        for error in errorFactor:    
            seed = random.randint(1,2555)
            rand = random.Random(seed)

            Decoder=UnpackenPacket(field,generation_size,num_packets)
            Decoder_zp = UnpackenPacket(field,generation_size,num_packets)

            # print list_packets,'\n',list_packets_zp
            # for packet,packet_zp in zip(list_packets,list_packets_zp):
            for packet in BB_list_packets:    
                if rand.random() >error:
                    Decoder.unpacken(packet,checkString="BBased")
            temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            error_BB.append(temp_datum)

            for packet_zp in BB_list_packets_zp:
                if rand.random() > error:    
                    Decoder_zp.unpacken(packet_zp,checkString="BBased")
                

            

            temp_datum = Decoder_zp.decoded_flag.values().count(True)/float(num_packets)
            error_BB_zp.append(temp_datum)

            # # =============================================================================
            # list_packets=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
            # list_packets_zp=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

            Decoder=UnpackenPacket(field,generation_size,num_packets)
            Decoder_zp = UnpackenPacket(field,generation_size,num_packets)

            # print list_packets,'\n',list_packets_zp
            #for packet,packet_zp in zip(list_packets,list_packets_zp):
            for packet in SW_list_packets:    
                if random.random() >error:
                    Decoder.unpacken(packet,checkString="SW")
            for packet_zp in SW_list_packets_zp:
                if random.random() >error:
                    Decoder_zp.unpacken(packet_zp,checkString="SW")
                

            temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            error_SW.append(temp_datum)

            temp_datum = Decoder_zp.decoded_flag.values().count(True)/float(num_packets)
            error_SW_zp.append(temp_datum)

        error_rate.append([error_BB,error_BB_zp,error_SW,error_SW_zp])


    
    with open('./CodeRate/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)
    print error_rate

def run_seprate():
    
    
    error_rate = []
    # for i in range(3):
    for field in field_group:

        error_BB = []
        error_BB_zp = []

        error_SW = []
        error_SW_zp = []

        BB_list_packets=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        BB_list_packets_zp=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

        # SW_list_packets=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
        # SW_list_packets_zp=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

        for error in errorFactor:    
            #seed = random.randint(1,2555)
            #rand = random.Random(seed)

            Decoder=UnpackenPacket(field,generation_size,num_packets)
            Decoder_zp = UnpackenPacket(field,generation_size,num_packets)

            # print list_packets,'\n',list_packets_zp
            # for packet,packet_zp in zip(list_packets,list_packets_zp):
            for packet,packet_zp in zip(BB_list_packets,BB_list_packets_zp):    
                if random.random() >error:
                    Decoder.unpacken(packet,checkString="BBased")

                if random.random() > error:    
                    Decoder_zp.unpacken(packet_zp,checkString="BBased")
                
            temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            error_BB.append(temp_datum)

            # for packet_zp in BB_list_packets_zp:
            #     if random.random() > error:    
            #         Decoder_zp.unpacken(packet_zp,checkString="BBased")
                
            temp_datum = Decoder_zp.decoded_flag.values().count(True)/float(num_packets)
            error_BB_zp.append(temp_datum)

            # # # =============================================================================
            # # list_packets=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
            # # list_packets_zp=encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)

            # Decoder=UnpackenPacket(field,generation_size,num_packets)
            # Decoder_zp = UnpackenPacket(field,generation_size,num_packets)

            # # print list_packets,'\n',list_packets_zp
            # #for packet,packet_zp in zip(list_packets,list_packets_zp):
            # for packet in SW_list_packets:    
            #     if random.random() >error:
            #         Decoder.unpacken(packet,checkString="SW")
            # for packet_zp in SW_list_packets_zp:
            #     if random.random() >error:
            #         Decoder_zp.unpacken(packet_zp,checkString="SW")
                

            # temp_datum = Decoder.decoded_flag.values().count(True) / float(num_packets)
            # error_SW.append(temp_datum)

            # temp_datum = Decoder_zp.decoded_flag.values().count(True)/float(num_packets)
            # error_SW_zp.append(temp_datum)

        error_rate.append([error_BB,error_BB_zp,error_SW,error_SW_zp])


    
    with open('./CodeRate/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)
    print error_rate

def show_error():
   

    #fileName = "CP_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./CodeRate/'+ fileName + '.json','r') as outfile:
        error_rate= json.load(outfile)

    
    error_BB = [item[0] for item in error_rate]
    error_BB_zp = [item[1] for item in error_rate]

    error_SW = [item[2] for item in error_rate]
    error_SW_zp = [item[3] for item in error_rate]    

    error_M = [error_BB,error_BB_zp,error_SW,error_SW_zp]
    title_List=['error_BB','error_BB_zerop','error_SW','error_SW_zerop']
    fig,ax = plt.subplots(2,1)
    
    markter = ['.',',','_','x','p','4','|']
    print "error_M:",error_M
    for i in range(2):
        # if len(error_M[i]) !=0:
            for j in range(numCP):
                
                ax[i].plot(errorFactor,error_M[i][j],label="CP="+str(1+j),marker=markter[j])
                # ax[i].plot(errorFactor,error_M[i][j],label="CodedP="+str(1+j))
                ax[i].set_xscale('log')
                ax[i].set_xlabel("error")
                
                ax[i].set_title(title_List[i])
                ax[i].grid(True)
            ax[i].plot(errorFactor,1-np.array(errorFactor),color="r",marker=">",label="Reference")
            ax[i].legend()
    ax[0].set_ylabel("Reliability")

    plt.subplots_adjust(vspace=0.3)
    plt.savefig('./CodeRate/average_'+ fileName + '_error.png')
    
    plt.show()

def show2_CP():

    #fileName = "CP_"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)+"GenS"+str(generation_size)
    with open('./CodeRate/'+ fileName + '.json','r') as outfile:
        error_rate= json.load(outfile)

    
    error_BB = [item[0] for item in error_rate]
    error_BB_zp = [item[1] for item in error_rate]

    error_SW = [item[2] for item in error_rate]
    error_SW_zp = [item[3] for item in error_rate]    

    error_M = [error_BB,error_BB_zp,error_SW,error_SW_zp]
    title_List=['error_BB','error_BB_zerop','error_SW','error_SW_zerop']
    
    fig,ax = plt.subplots(1,4)
    
    markter = ['.',',','_','x','p','4','|']
    for i in range(numCP):
        # if len(error_M[i]) !=0:
            for j in range(4):
                ax[i].plot(errorFactor,error_M[j][i],label=title_List[j],marker=markter[j])
                # ax[i].plot(errorFactor,error_M[i][j],label="CodedP="+str(1+j))
                ax[i].set_xscale('log')
                ax[i].set_xlabel("error")
                ax[i].legend()
                ax[i].set_title("Coded Packet ="+str(1+i))
                ax[i].grid(True)
    ax[0].set_ylabel("Reliability")

    
    plt.savefig('./CodeRate/'+ fileName + '_CP.png')
    plt.show()

def show_macro():
    with open('./CodeRate/'+ fileName + '.json','r') as outfile:
        error_rate= json.load(outfile)

    
    error_BB = [item[0] for item in error_rate]
    error_BB_zp = [item[1] for item in error_rate]

    error_SW = [item[2] for item in error_rate]
    error_SW_zp = [item[3] for item in error_rate]    

    error_M = [error_BB,error_BB_zp,error_SW,error_SW_zp]
    title_List=['error_BB','error_BB_zerop','error_SW','error_SW_zerop']
    
    fig,ax = plt.subplots(1,4)
    
    markter = ['.',',','_','x','p','4','|']
    for i in range(numCP):
        # if len(error_M[i]) !=0:
            for j in range(4):
                ax[i].plot(errorFactor,error_M[j][i],label=title_List[j],marker=markter[j])
                # ax[i].plot(errorFactor,error_M[i][j],label="CodedP="+str(1+j))
                ax[i].set_xscale('log')
                ax[i].set_xlabel("error")
                ax[i].legend()
                ax[i].set_title("Coded Packet ="+str(1+i))
                ax[i].grid(True)
    ax[0].set_ylabel("Reliability")

    
    plt.savefig('./CodeRate/'+ fileName + '_CP.png')
    plt.show()

if __name__ == "__main__":

    # run()
    run_seprate()
    # show_error()
    # show2_CP()
    
    
    # t = [g/float(g+1) for g in GS]
    # for i in range(len(error_rate)):
        
    #     plt.plot(t,error_rate[i][0],marker='*',label='SBlock '+ str(field_group[i]))
    #     plt.plot(t,error_rate[i][1],marker='x',label="SBlock_zp "+ str(field_group[i]))

    
    # # t = np.arange(len(error_rate))
    # markter = ['o','<','*','>','.','+','x']
    # for i in range(len(GS)):
        
    #     # temp_d = [error_rate[i][0][j] for j in range(len(error_rate)) ]
    #     temp_d = error_rate[i][0]
    #     t=np.linspace(0,1,len(temp_d))
    #     plt.plot(t,temp_d,marker=markter[i],label='BB GS:'+str(GS[i]))
    #     # plt.yscale('log')
    #     # temp_d = [error_rate[i][1][j] for j in range(len(error_rate)) ]
    #     temp_d = error_rate[i][1]
    #     t=np.linspace(0,1,len(temp_d))
    #     plt.plot(t,temp_d,marker=markter[i+2],label='BB-ZP GS:'+str(GS[i]))

    
    # plt.legend()
    
    # plt.ylim((-0.1,0.99))
    # # plt.xlim((0.3,1))
    # plt.title("channel loss 5%"+fileName)
    # plt.xlabel("codede rate")
    # plt.ylabel("loss rate")
    
    # plt.savefig('./json/'+fileName+".png")
    # plt.show()
