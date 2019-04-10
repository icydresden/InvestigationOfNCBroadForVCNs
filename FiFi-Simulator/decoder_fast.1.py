#!/usr/bin/env python2
# -*- coding:utf-8 -*-

"""
Encoder is a generator to create coded packet
For example, two orginal packet, Encoder will 
give two handled orignal packet and one coded 
packet
"""
import random
import copy
from fifi_simple_api import B,B4,B8,B16
import numpy as np
import json
from encoder_fast import encodertest_SW,encodertest_BBased
import matplotlib.pyplot as plt
import numpy as np
import math


class DecoderCoeffMatrixFactory:
    """
    CoeffRandom crate random coefficience matrix
    """

    # def __init__(self, field, sizes_of_pack, generation_size):
    def __init__(self, field):
        """
        Get the variables associated with the class

        :type field: fifi-byte8(B8)
        :param field: 

        """

        self.field = field
        

    def buildUnEqSizeData(self,coeff_list, sizes_list,buffer_index):
        """
        Generate random coefficient for packets of unequal size
        example [1,2,4,1]
        _                                                   _
        | alpha beta    0   gamma    0      0     0   delta |
        |   0     0   beta    0    gamma    0     0     0   |
        |   0     0     0     0      0    gamma   0     0   |
        |   0     0     0     0      0      0   gamma   0   -
        -
        """
        generation_size = len(sizes_list)
        index_notInBuffer = []
        sum_size = 0
        max_size = 0
        for i in range(generation_size):
            if i not in buffer_index:
                index_notInBuffer.append(i)
                sum_size += sizes_list[i]
                if sizes_list[i] > max_size:
                    max_size = sizes_list[i]


        M = [[self.field(0) for i in range(sum_size) ]
                                for j in range(max_size)]

        next_start = 0
        for index in index_notInBuffer:

            for j in range(sizes_list[index]):
                k = j + next_start
                M[j][k] = coeff_list[index]

            next_start += sizes_list[index]
        # print "M\n",M

        return M

    def buildEqSizeData(self,coeff_list, sizes_list,buffer_index):
        """
        Generate random coefficient for packets of unequal size
        example [1,2,4,1]

        |-----length_unit---|
        _                                                                                       _
        | alpha   0    0    0  beta  0    0   0  gamma  0     0     0   delta   0    0     0    |
        |   0  alpha   0    0    0  beta  0   0    0  gamma   0     0     0   delta  0     0    |
        |   0     0  alpha  0    0   0  beta  0    0    0   gamma   0     0     0   delta  0    |
        |   0     0    0  alpha  0   0    0  beta  0    0     0   gamma   0     0    0    delta -
        -
        """
        generation_size= len(sizes_list)
        index_notInBuffer = []
        sum_size = 0
        max_size = 0
        for i in range(len(sizes_list)):
            if i not in buffer_index:
                index_notInBuffer.append(i)
                sum_size += sizes_list[i]
                if sizes_list[i] > max_size:
                    max_size = sizes_list[i]

        M = [[self.field(0) for i in range(generation_size*max_size)]
                                for j in range(max_size)]

        next_start = 0
        for index in index_notInBuffer:

                for j in range(max_size):
                    k = j + next_start
                    M[j][k] = coeff_list[index]

                next_start += max_size

        return M

class UnpackenPacket:
    def __init__(self,field,generation_size,num_packets):
        self.field = field
        # generation_size is usually 4
        self.generation_size = generation_size
        # set biger buffer
        self.data_buffer = { i:[] for i in range(num_packets) }
        self.decoded_flag = { i:False for i in range(num_packets ) }
        
        self.rank_buffer = {i:0 for i in range(num_packets//generation_size)}
        self.coded_data_buffer=[[] for _ in range(num_packets//generation_size)]
        self.coded_coeff_buffer=[[] for _ in range(num_packets//generation_size)]

        self.rank_buffer_zp = {i:0 for i in range(num_packets// (generation_size//2) +1 )}
        self.coded_data_buffer_zp=[[] for _ in range(num_packets// (generation_size//2))]
        self.coded_coeff_buffer_zp=[[] for _ in range(num_packets// (generation_size//2))]

        # self.index = 0
        self.buffer_index = []
        self.index_notInBuffer= []
        self.flag = []
        # generate coeff matrix
        self.DecoeffFactory=DecoderCoeffMatrixFactory(field)
        self.step = generation_size / 2

    def reset(self,field,generation_size,num_packets):
        self.generation_size = generation_size
        # set biger buffer
        self.data_buffer = { i:[] for i in range(num_packets) }
        self.decoded_flag = { i:False for i in range(num_packets ) }
        # self.index = 0
        self.buffer_index = []
        self.index_notInBuffer= []
        self.flag = []
        

    def unpacken(self,packet,checkString="BBased"):
        Type = packet[0]
        ID = packet[1]
        
        blockNum = ID//self.generation_size

        if checkString == "SW":
            checkFull = self.checkFull_SW
            # blockNum = ID // (self.generation_size//2)
            # self.rank_buffer_zp[blockNum] += 1
        else:
            checkFull = self.checkFull_BBased
            
            # self.rank_buffer[blockNum] += 1

        print "index ",ID,"generataion:",self.generation_size,"\n"
        if Type == 0x01: 
            self.data_buffer[ID] = packet[2]
            self.decoded_flag[ID] = True

            self.rank_buffer[blockNum] += 1
            if checkFull(ID):   
                             
                print "all elements are received !\n"
            
        elif Type == 0x11:
            
            if checkFull(ID):
                
                print "No need Decode Process, all data are there ! self.decoded_flag\n",self.decoded_flag
            else:
                if checkString == "BBased" and self.rank_buffer[blockNum] > self.generation_size:
                    print "enough packets, but still not get all ? what happened?"
                    return -1
                if checkString == "SW" and self.rank_buffer_zp[blockNum] > self.generation_size:
                    print "enough packets, but still not get all ? what happened?"
                    return -1
                    
                self.rank_buffer[blockNum] += 1

                checkFull(ID)
                
                print "Start Decoder ......\n"
                self.generation_size = packet[2]

                coeff_list = [item for item in packet[3:3+self.generation_size]]
                sizes_list = packet[3+self.generation_size : 3+2*self.generation_size]

                # coded_data = packet[3+2*self.generation_size:]
                
                coded_data = packet[3+2*self.generation_size]
                # print "coded_data :",type(coded_data[0])

                ##  add coded data in a buffer, wait for a decode process
                print "blockNum:",blockNum,"self.coded_data_buffer",self.coded_data_buffer

                if checkString == "BBased":
                    self.coded_coeff_buffer[blockNum].append(coeff_list)
                    self.coded_data_buffer[blockNum].append(coded_data)
                    
                    # print "fist Deocder Prozess sizes_list",sizes_list
                    ## decode data
                    # self.decoderProcess(ID, coded_data, coeff_list, sizes_list)
                    self.decoderProcess(ID, self.coded_coeff_buffer[blockNum], self.coded_data_buffer[blockNum], sizes_list)
                    print " self.decoded_flag\n", self.decoded_flag
                elif checkString == "SW":
                    self.coded_coeff_buffer_zp[blockNum].append(coeff_list)
                    self.coded_data_buffer_zp[blockNum].append(coded_data)
                    
                    # print "fist Deocder Prozess sizes_list",sizes_list
                    ## decode data
                    # self.decoderProcess(ID, coded_data, coeff_list, sizes_list)
                    self.decoderProcess(ID, self.coded_coeff_buffer_zp[blockNum], self.coded_data_buffer_zp[blockNum], sizes_list)
                    print " self.decoded_flag\n", self.decoded_flag
                else:
                    print "Unknown type packet"
                
        else:
            print "Unknown type packet"
            return -1


    def checkFull_SW(self,ID):
        
        # generation_size = self.generation_size
        if ID < self.step:
            
            start = ( ID / self.step) * self.step
        else:
            
            start = ( ID / self.step) * self.step - self.step

        self.buffer_index=[]
        temp = [[] for i in range(self.generation_size)]
        for i in range(self.generation_size):
            temp[i]=self.decoded_flag[start + i]
            if self.decoded_flag[start + i] == True:
                self.buffer_index.append(i)
            print "data %d %s: " % (start+i , str(self.data_buffer[start+i]))

        return all(temp)
    
    def checkFull_BBased(self,ID):
        # generation_size = self.generation_size
        start = ( ID // self.generation_size) * self.generation_size 

        self.buffer_index=[]
        temp = [[] for i in range(self.generation_size)]
        for i in range(self.generation_size):
            temp[i]=self.decoded_flag[start + i]
            if self.decoded_flag[start + i] == True:
                self.buffer_index.append(i)
            print "data %d %s: " % (start+i , str(self.data_buffer[start+i]))

        return all(temp)

    def decoderProcess(self,ID, coeff_list_m, coded_data_m, sizes_list):

        ## coded_data is a coded data matrix

        # coeff_matrix, data_list

        coeff_matrix_list=[]
        sum_of_sizes=[]
        coded_data_list =[]

        for coeff_list in coeff_list_m:
            coeff_matrix_list.append(self.DecoeffFactory.buildUnEqSizeData(coeff_list,sizes_list,self.buffer_index))
        # coded_data = [self.field(d) for d in coded_data]

        
        max_size = 0
        sum_of_sizes= 0
        
        self.index_notInBuffer = []
        print "buffer_index",self.buffer_index
        for i in range(self.generation_size):
            
            if i in self.buffer_index:
                index = ID - self.generation_size +1 + i
                print "self.data_buffer[",index,"] : \n",self.data_buffer[index]
                for j in range(len(self.data_buffer[index])):
                    
                    # print "i:", i,",j",j,",", "data_buffer:",type(self.data_buffer[index][j])
                    
                    item = self.data_buffer[index][j]
                    # print "item type:",type(item)
                    for coded_data,coeff_list in zip(coded_data_m,coeff_list_m):
                        coded_data[j] +=  coeff_list[i]*item
            else:
                self.index_notInBuffer.append(i)
                if sizes_list[i] > max_size:
                    max_size = sizes_list[i]
                sum_of_sizes += sizes_list[i]
        
        # print "self.buffer_index",self.buffer_index
        # print "index_notInBuffer",index_notInBuffer
        for coded_data in coded_data_m:
            coded_data_list.append(coded_data[0:max_size])
        
        self.flag = {i:0 for i in range(sum_of_sizes)}

        # self.decoded_CoeffMatrix = [[self.field(0) for i in range(sum_of_sizes)] for j in range(len(coeff_matrix))]
        # self.decoded_DataMatrix = [self.field(0) for i in range(sum_of_sizes)]

        self.decoded_CoeffMatrix = [[] for j in range(sum_of_sizes)]
        self.decoded_DataMatrix = [None for i in range(sum_of_sizes)]

        # decode random coeff matrix
        for coeff_matrix,coded_data in zip(coeff_matrix_list,coded_data_list):

            for i in range(max_size):  
                self.line_decoder(coeff_matrix[i],coded_data[i])

        # print "decoded_coeff matrix\n",np.array(self.decoded_CoeffMatrix)
        # print "decoded_coded data\n", np.array(self.decoded_DataMatrix)

        # to get triangular matrix
        for i in range(sum_of_sizes-1,-1,-1):
            # for j in range(sum_of_sizes):

            index = self.findLastNoneZero(self.decoded_CoeffMatrix[i])
            if index == -1 or index != i:
                continue

            for j in range(i-1,-1,-1):

                if len(self.decoded_CoeffMatrix[j]) >0 and self.decoded_CoeffMatrix[j][i]!=self.field(0):
                    self.decoded_DataMatrix[j] +=  self.decoded_CoeffMatrix[j][i]*self.decoded_DataMatrix[i]
                    self.decoded_CoeffMatrix[j][i] = self.field(0)
                    
            
        # print "dex coeff matrix\n",np.array(self.decoded_CoeffMatrix)
        # print "dex coded data\n", np.array(self.decoded_DataMatrix)

        base = 0
        print "index_notInBuffer",self.index_notInBuffer
        succeed_flag=[]
        
        for f,i in enumerate (self.index_notInBuffer):
            succeed_flag.append(True) 
            index = ID-(self.generation_size-1)+i
            temp = [None for _ in range(sizes_list[i])]
            
            for j in range(sizes_list[i]):
                k = j + base
                if k == self.findLastNoneZero(self.decoded_CoeffMatrix[k]):
                    temp[j]  = self.decoded_DataMatrix[k]
                else:
                    succeed_flag[f]=False
                    # self.rank_buffer[ID//self.generation_size] -= 1
                
            base += sizes_list[i]
            if succeed_flag[f]:
                self.data_buffer[index] = temp
                # succeed_flag should be True when there is no error
                self.decoded_flag[index] = succeed_flag[f]
                print "=Got new Packet===================================="
                # print "decoded Matrix\n",self.decoded_flag

        # if len(succeed_flag) !=0 and all(succeed_flag):
        #     self.rank_buffer[ID//self.generation_size] = 0
            
        # else:
        #     self.rank_buffer[ID//self.generation_size] -= 1
        # # one test function() 

    def line_decoder(self,new_line, new_data):
    
         
        # find the first None Zero element, return index
        index = next((i for i,value in enumerate(new_line) if value != self.field(0)), -1 )
        # print "index: ", index
        data_decoded_temp = copy.deepcopy(new_data)
        # while index>=0 and (self.rank <= len(self.coeff_Matrix[0])):
        while index>=0 :  
            # print "Rank :",self.rank
            # print "flag [",index,"]\n", self.flag

            if self.flag[index] == 0:
                line_temp = [new_line[i]/new_line[index] for i in range(len(new_line))]
                # print "line_temp ))\n",line_temp
                data_decoded_temp = data_decoded_temp/new_line[index]

                self.decoded_CoeffMatrix[index] = line_temp
                self.decoded_DataMatrix[index] = data_decoded_temp

                self.flag[index] = 1
                # print "flag [",index,"]\n", self.flag
                index = -1
            else:
                line_temp = [new_line[i]/new_line[index] for i in range(len(new_line))]
                data_decoded_temp = data_decoded_temp/new_line[index]
                
                line_flag = self.decoded_CoeffMatrix[index]
                new_line = [line_temp[i]+line_flag[i] for i in range(len(new_line))]
                
                if line_temp.count(self.field(0)) > line_flag.count(self.field(0)):
                    self.decoded_CoeffMatrix[index] = line_temp
                    self.decoded_DataMatrix[index], data_decoded_temp = data_decoded_temp, self.decoded_DataMatrix[index]


                data_decoded_temp = data_decoded_temp + self.decoded_DataMatrix[index]
                
                # print "new_line", new_line
                index = self.findFirstNoneZero(new_line)

        # return self.isdecoded()

    def findLastNoneZero(self,new_line):
        
        for index in range(len(new_line)-1,-1,-1):
            if new_line[index] != self.field(0):
                
                return index
        return -1

    def findFirstNoneZero(self,new_line):
        
        # option 1
        # for index in range(len(new_line)):
        #     if new_line[index] != self.field(0):
        #         return index
        
        # return -1

        # option 2
        return next((i for i,value in enumerate(new_line) if value != self.field(0)), -1 )
        
    def showDecodedMatrix(self):
        for row in self.decoded_CoeffMatrix:
            print row


if __name__=="__main__":
    import time
    
    num_packets = 12800
    maxSize_packet = 1500
    fixPacketmaxSize = 50
    generation_size = 8

    field_group = [B,B4,B8,B16]
    field = B8

    GS = [2,4,8,16,32,64]
    GS = [2,4,8,16]
    
    error_native = []
    error_zeropp = []
    codedRatePacket = 1
    for i in range(10):
        error_native.append([])
        error_zeropp.append([])
        for generation_size in GS:
            t0 = time.time()
            list_packets=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=0)
            deltaT = time.time() - t0

            error_native[i].append(deltaT)
            print "time of BlockBased:",deltaT
            # list_packets_zp=encodertest_BBased(field,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
            if generation_size == 2:
                error_zeropp[i].append(0)
            else:
                t0 = time.time()
                list_packets_zp=encodertest_BBased(field,codedRatePacket,generation_size,num_packets,maxSize_packet,fixPacketmaxSize=maxSize_packet)
                deltaT = time.time() - t0

                error_zeropp[i].append(deltaT)
                print "time of SlidingWindow:",deltaT
        
    error_rate=[error_native,error_zeropp]
    
    fileName = "BB_Coding Time: NumP:"+ str(num_packets)+"_maxSize_"+str(maxSize_packet)+"_FixSize_"+str(fixPacketmaxSize)
    with open('./json/'+ fileName + '.json','w') as outfile:
        json.dump(error_rate,outfile)

    # # t = np.arange(len(error_rate))
    # markter = ['o','<','*','>','.','+','x']
    # for i in range(len(GS)):
        
    #     # temp_d = [error_rate[i][0][j] for j in range(len(error_rate)) ]
    #     temp_d = [error_rate[i][0]]
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
    

    