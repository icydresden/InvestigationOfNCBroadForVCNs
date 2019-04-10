#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import random
import os
import array
# from timeit import timeit
import numpy as np

from fifi_simple_api import B,B4,B8,B16
import json



"""
Encoder is a generator to create coded packet
For example, two orginal packet, Encoder will 
give two handled orignal packet and one coded 
packet
"""
class RandomGenerator:
    def __init__(self,field,rand):
        self.rand = rand
        self.field = field
    
    def databuild(self,sizes_list):
        # data_matrix = [os.urandom(size)  for size in sizes_list]
        data_matrix = [[self.field(self.rand.randint(1,len(self.field.range)-1))  for _ in range(size) ] for size in sizes_list]
        # data_matrix = [[self.field(1)  for _ in range(size) ] for size in sizes_list]
        return data_matrix

    def databuild_zeropad_fixMaxLength(self,sizes_list,PacketmaxSize):
        data_matrix = []
        for size in sizes_list:
            data = [self.field(self.rand.randint(1,len(self.field.range)-1))  for _ in range(size) ]
            data = data + [self.field(0) for _ in range(PacketmaxSize-size)]
            data_matrix.append(data)
        return data_matrix
    
    # def databuild_withzeropadding_maxDataLength(self,sizes_list):
    #     data_matrix = []
    #     for size in sizes_list:
    #         data = os.urandom(size)
    #         data = data + chr(0)*(maxlength-size)
    #         data_matrix.append(data)
    #     return data_matrix

    def coeffbuild(self,generation_size):
        coeff_list = [self.field(self.rand.randint(1,len(self.field.range)-1)) for _ in range(generation_size)]
        return coeff_list

    def databuild_MS(self,sizes_list):
        dataMatrix = [[self.field(self.rand.randint(1,1500)) for _ in range(size)] for size in sizes_list]
        return dataMatrix

class EncoderFactory:
    """
    Encoder generate packet matrix associated with input packet 
    """
    # def __init__(self, field,coeff_factory, data_factory, sizes_list):
    def __init__(self, field, rand):
        """
        Get the variables associated with the class

        :type factory: fifi-byte8(B8)encodertest_SBlock
        :param factory: 

        :type sizes_list: array
        :param sizes_list: 
        """
        self.rand = rand
        self.field=field
        self.data_buffer = None
        self.sizes_buffer = []
        self.ID = 0

        
    def buildCodedData_SW_Macro(self,codedRatePacket,generation_size,packets_sizes_list,fixPacketmaxSize):

        """
        Associate different genertion size and packet sizes list make packets list
        which include native packets and coded packet

        :type packets_sizes_list: list
        :param packets_sizes_list: 

        """
      
        maxSize=max(packets_sizes_list)
        # if len(self.data_buffer) == 0 :
        if self.data_buffer is None:
            coeff_list=[]
            for i in range(codedRatePacket):
                coeff_list.append( RandomGenerator(self.field,self.rand).coeffbuild(len(packets_sizes_list)))

            # coeff_list = RandomGenerator(self.field,self.rand).coeffbuild(len(packets_sizes_list))

            if fixPacketmaxSize > maxSize:
                data_m = RandomGenerator(self.field,self.rand).databuild_zeropad_fixMaxLength(packets_sizes_list,fixPacketmaxSize) # fix length, fixPacketmaxSize
            else:
                data_m = RandomGenerator(self.field,self.rand).databuild(packets_sizes_list) # random length

            self.data_buffer = data_m
            self.sizes_buffer = packets_sizes_list
        else:
            coeff_list=[]
            for i in range(codedRatePacket):
                coeff_list.append( RandomGenerator(self.field,self.rand).coeffbuild(generation_size))
            
            # coeff_list = RandomGenerator(self.field,self.rand).coeffbuild(generation_size)

            if fixPacketmaxSize >= maxSize:
                data_m = RandomGenerator(self.field,self.rand).databuild_zeropad_fixMaxLength(packets_sizes_list,fixPacketmaxSize) # fix length, fixPacketmaxSize
            else:
                data_m = RandomGenerator(self.field,self.rand).databuild(packets_sizes_list) # random length

            self.data_buffer.extend(data_m)
            data_m, self.data_buffer = self.data_buffer, data_m

            self.sizes_buffer.extend(packets_sizes_list)
            packets_sizes_list, self.sizes_buffer = self.sizes_buffer, packets_sizes_list
            # print  "packets_sizes_list ->",packets_sizes_list

        print "fixPacketMaxLength", fixPacketmaxSize ," vs ", maxSize
        # for item in data_m:
        #     print len(item),'|',item
    
        packets = []
        for i in range(len(self.data_buffer)):
            
            packet_original=[0x01] + [self.ID] + [self.data_buffer[i]]
            packets.append(packet_original)

            self.ID += 1

        coded_list = []
        for i in range(len(coeff_list)):
            coded_list.append([])
            for j in range(len(data_m)):
                # print "type(data_m)[j]:",type(data_m[j][0])
                temp_list = [coeff_list[i][j]*item for item in data_m[j]]

                if len(coded_list[i]) < len(temp_list):
                    coded_list[i], temp_list = temp_list, coded_list[i]

                # for j in range(len(temp_list)):
                #     coded_list[i][j] +=  temp_list[j]
                for k in range(len(temp_list)):
                    coded_list[i][k] +=  temp_list[k]

        
        # for cp in codedRatePacket:
        #     coded_list = []
        #     for i in range(len(data_m)):
        #         # print "len(data_m)[i]:",len(data_m[i])
        #         temp_list = [coeff_list[i]*item for item in data_m[i]]

        #         if len(coded_list) < len(temp_list):
        #             coded_list, temp_list = temp_list, coded_list

        #         for j in range(len(temp_list)):
        #             coded_list[j] +=  temp_list[j]

        for i in range(len(coeff_list)):
            if fixPacketmaxSize >= maxSize:
            # print  "result\n",result
                zeropad_sizes_list=[]
                for _ in range(len(data_m)):
                    zeropad_sizes_list.append(fixPacketmaxSize)

                packet_coded_head = [0x11] + [self.ID-1] + [len(data_m)] + coeff_list[i] + zeropad_sizes_list

            else:
                packet_coded_head = [0x11] + [self.ID-1] + [len(data_m)] + coeff_list[i] + packets_sizes_list
                
            
            packet_coded = packet_coded_head + [coded_list[i]]

            packets.append(packet_coded)

        return packets

    def buildCodedData_BBased_Macro(self,codedRatePacket,generation_size,packets_sizes_list,fixPacketmaxSize):
    
        """
        Associate different genertion size and packet sizes list make packets list
        which include native packets and coded packet

        :type packets_sizes_list: list
        :param packets_sizes_list: 

        """
      
        maxSize=max(packets_sizes_list)
        coeff_list=[]
        # if len(self.data_buffer) == 0 :
        # codedRatePacket = 1
        for i in range(codedRatePacket):
            coeff_list.append( RandomGenerator(self.field,self.rand).coeffbuild(len(packets_sizes_list)))

        if fixPacketmaxSize >= maxSize:
            data_m = RandomGenerator(self.field,self.rand).databuild_zeropad_fixMaxLength(packets_sizes_list,fixPacketmaxSize) # fix length, fixPacketmaxSize
        else:
            data_m = RandomGenerator(self.field,self.rand).databuild(packets_sizes_list) # random length

        self.data_buffer = data_m
       

        # print "fixPacketMaxLength", fixPacketmaxSize ," vs ", maxSize
        # for item in data_m:
        #     print len(item),'|',item
    
        packets = []
        for i in range(len(self.data_buffer)):
            
            packet_original=[0x01] + [self.ID] + [self.data_buffer[i]]
            packets.append(packet_original)

            self.ID += 1

        coded_list = []
        for i in range(len(coeff_list)):
            coded_list.append([])
            for j in range(len(data_m)):
                # print "type(data_m)[j]:",type(data_m[j][0])
                temp_list = [coeff_list[i][j]*item for item in data_m[j]]

                if len(coded_list[i]) < len(temp_list):
                    coded_list[i], temp_list = temp_list, coded_list[i]

                # for j in range(len(temp_list)):
                #     coded_list[i][j] +=  temp_list[j]
                for k in range(len(temp_list)):
                    coded_list[i][k] +=  temp_list[k]

        for i in range(len(coeff_list)):
            if fixPacketmaxSize >= maxSize:
            # print  "result\n",result
                zeropad_sizes_list=[]
                for _ in range(len(data_m)):
                    zeropad_sizes_list.append(fixPacketmaxSize)

                packet_coded_head = [0x11] + [self.ID-1] + [len(data_m)] + coeff_list[i] + zeropad_sizes_list

            else:
                packet_coded_head = [0x11] + [self.ID-1] + [len(data_m)] + coeff_list[i] + packets_sizes_list
            
        
            packet_coded = packet_coded_head + [coded_list[i]]

            packets.append(packet_coded)

        return packets  

def encodertest_SW(field,codedRatePacket,generation_size,num_packets,maxSize,fixPacketmaxSize=0):
    seed = random.randint(1,2555)
    rand = random.Random(seed)
    print "seed:",seed

    Encoder=EncoderFactory(field,rand)
    # [2,4,8,16,32,64]
    # generation_size = 4
    # SW macro level test
    step = generation_size/2
    # sizes_list = [rand.randint(1,maxSize) for _ in range(step)]
    
    # packets=Encoder.buildCodedData_SW_Macro(generation_size,sizes_list[0:step],fixPacketmaxSize)
    
    # list_packets.extend(packets)

    # start = generation_size - step
    # stop = generation_size + step
    assert(maxSize>=40)
    list_packets = []

    for i in range(0,num_packets/step ):
        sizes_list = [rand.randint(1,maxSize) for _ in range(num_packets)]
        #packets=Encoder.buildCodedData_BBased_Macro(1,generation_size,sizes_list[2*i:2*i+step],fixPacketmaxSize)
        packets=Encoder.buildCodedData_SW_Macro(codedRatePacket,generation_size,sizes_list[2*i:2*i+step],fixPacketmaxSize)
        list_packets.extend(packets)
        print "count: SW",i
    
    return list_packets
    # print list_packets
    # with open("./fifi-example/Structure/result.json","w+") as outfile:
    # with open("./Structure/coded_packet.json","w") as outfile:
    #     json.dump(list_packets,outfile)

    # Systmatic Block macro level test
    # SW packets level test
    # Systmatic Block packets level test

def encodertest_BBased(field,codedRatePacket,generation_size,num_packets ,maxSize,fixPacketmaxSize):
    seed = random.randint(1,2555)
    rand = random.Random(seed)

    print "seed:",seed

    Encoder=EncoderFactory(field,rand)
    # [2,4,8,16,32,64]
    # generation_size = 4
    # SW macro level test
    # list_packets = [[] for _ in range(0,num_packets/generation_size)]
    list_packets=[]
    for i in range(0,num_packets/generation_size ):

        sizes_list = [rand.randint(1,maxSize) for _ in range(generation_size)]
        packets=Encoder.buildCodedData_BBased_Macro(codedRatePacket,generation_size,sizes_list,fixPacketmaxSize)
        list_packets.extend(packets)
        print "count: random.randin(1,2555)",i
    
    return list_packets

def encodertest_REPEAT(field,codedRatePacket,generation_size,num_packets ,maxSize,fixPacketmaxSize):
    seed = random.randint(1,2555)
    rand = random.Random(seed)

    print "seed:",seed

    Encoder=EncoderFactory(field,rand)
    # [2,4,8,16,32,64]
    # generation_size = 4
    # SW macro level test
    # list_packets = [[] for _ in range(0,num_packets/generation_size)]
    list_packets=[]
    for i in range(0,num_packets/generation_size ):

        sizes_list = [rand.randint(1,maxSize) for _ in range(generation_size)]
        packets=Encoder.buildCodedData_BBased_Macro(codedRatePacket,generation_size,sizes_list,fixPacketmaxSize)
        list_packets.extend(packets)
        print "count: random.randin(1,2555)",i
    
    return list_packets

if __name__ == "__main__":

    seed = 2
    rand = random.Random(seed)
    
    num_packets = 50 #200 # 20000
    maxSize_packet = 50  # 1500
    fixPacketmaxSize = 50
    # generation_size = 8
    GS = [2,4,8,16,32,64]
    GS = [2]
    field_group = [B,B4,B8,B16]

    # #codedRatePacket = 1
    # for generation_size in GS:
    #     for codedRatePacket in range(1,generation_size+1):
    #         list_packets = encodertest_BBased(field_group[2],codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize)
            
    #         # print "list_packets",list_packets
    #         fileName = "PStream_nP_"+str(num_packets)+"_maxS_"+str(maxSize_packet)+"_cR_"+str(generation_size)+"_"+str(generation_size+codedRatePacket)
            
    #         with open("./pStream/"+fileName+".json",'w') as outfile:
    #             json.dump(list_packets,outfile)
    
    generation_size = 8
    codedRatePacket = 1
    for i in range(3):
        list_packets = encodertest_SW(field_group[2],codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize)
    print list_packets
    # print "list_packets",list_packets
    