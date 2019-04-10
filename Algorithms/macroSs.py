#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import math
import numpy as np
import random
import copy
GS=2
#GF=B8
class Show:
    
    def showDynFix(self,resultList):
        marker_list=['x','-','.','_']
        label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        
        fig,ax = plt.subplots(1,2)

        for i in range(len(resultList)):
            for j in range(len(resultList[i])):
                ax[i].plot(resultList[i][j],marker_list[j],label=label_list[j])
        
            ax[i].set_title("GS=2, GF=2^8, Dyn vs Fix Byte")
            ax[i].grid(True)
            ax[i].legend()
            ax[i].set_xlabel("smaller packets")
        # plt.ylim(-1,4500,200)
        
        plt.show() 

    def showParameter(self,resultList):
        marker_list=['_','.','','x']
        title_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        label_list = ["Dynamic","Fix"]
        fig,ax = plt.subplots(1,4)
        for i in range(len(resultList[0])):
            for j in range(len(resultList)):
                ax[i].plot(resultList[j][i],marker_list[j],label=label_list[j])
            ax[i].set_title(title_list[i])
            ax[i].grid(True)
            ax[i].legend()
            ax[i].set_xlabel("small packets")

        plt.show()


def gotFixBigGS2GF8(L1):
    # L1 = random.randint(50, 1400)
    Quotient = []
    for n in range(1,L1+1):
        if L1 % n == 0 :
            Quotient.append(n)
    print (Quotient)
    
    cumulate_oh = 0

    Cumulate_list = [cumulate_oh]
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    for L2 in range(1,L1+1):
        Temp_L1_list.append(L1)

        for item in Quotient:
            if L2 <= item:
                MacroSs = item
                Overhead = item-L2
                Operation=L1+2*MacroSs
                cumulate_oh += Overhead
                break
        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Cumulate_list.append(cumulate_oh)
    
    marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size","Cumulate_OH"]
    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list,Cumulate_list]
    
    for j in range(len(resultList)):
        plt.plot(resultList[j],label=label_list[j])

    strTitle = "GS=2, GF=2^8, Bigest Fix Byte"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("smaller packets")
    # plt.yscale('log')
    plt.savefig('./MacroFig/'+strTitle+'.png')
    plt.show()

def gotFixSmallGS2GF8(L1):
    Quotient = []
    for n in range(1,L1+1):
        if L1 % n == 0 :
            Quotient.append(n)
    print (Quotient)
    
    cumulate_oh = 0
    Cumulate_list = [cumulate_oh]
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    for L2 in range(1,L1+1):
        Q = L1 // L2
        R = L1 % L2


        MacroSs = L2
        Overhead = L2-R
        Operation= 2*L2+ (L1 + (L2 - R))
        temp_L1 = L1 + (L2 - R)
        cumulate_oh += Overhead

        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(temp_L1)
        Cumulate_list.append(cumulate_oh)

    marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size","Cumulate_OH"]
    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list,Cumulate_list]
    
    for j in range(len(resultList)):
        plt.plot(resultList[j],label=label_list[j])

    strTitle = "GS=2, GF=2^8, Smallest Fix Byte"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("smaller packets")
    plt.yscale('log')
    plt.savefig('./MacroFig/'+strTitle+".png")
    plt.show()

# ===========================    
def gotFixBigGS4GF8():
    import random

    runNum = 100
    intervel = 100
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []

    for i in range(runNum):
        input_List = [random.randint(1+intervel*j, intervel+ j*intervel) for j in range(4)]
        
        input_List.sort()
        #print "input:",input_List
        largest = max(input_List)
        smallest = min(input_List)

        
        Quotient = []
        for n in range(1,largest+1):
            if largest % n == 0 :
                Quotient.append(n)

        # print (Quotient)
        Overhead = 0
        Operation = 0
        MSs_list =[]
        for L2 in input_List[:-1]:
            
            for n in Quotient:
                if L2 <= n:
                    MacroSs = n
                    Overhead += n-L2
                    Operation += 2*n + largest
                    break
            MSs_list.append(MacroSs)
        print "MSs_list",MSs_list
        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(min(MSs_list))
        Temp_L1_list.append(largest)
    
    marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list]
    
    for j in range(len(resultList)):
        plt.plot(resultList[j],label=label_list[j])

    strTitle = "GS=4, GF=2^8, Largest(301,400) FixByte "+str(runNum)+"times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("random times")
    xtitle=list(np.array(range(runNum)))

    plt.xticks(xtitle)
    plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show()

def gotFixSmallGS4GF8():
    import random

    runNum = 100
    intervel = 100
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []

    for i in range(runNum):
        input_List = [random.randint(1+intervel*j, intervel+ j*intervel) for j in range(4)]
        
        input_List.sort()
        #print "input:",input_List
        smallest = min(input_List)
        largest = max(input_List)

        Quotient = []
        for n in range(1,largest+1):
            if largest % n == 0 :
                Quotient.append(n)
        # print (Quotient)
        
        MacroSs = smallest
        Overhead = 0
        Operation = 0
        for L2 in input_List[1:]:
            
            Q = L2 // smallest
            R = L2 % smallest

            Overhead += smallest - R
            Operation += L2 + (smallest - R)

        R = largest % smallest
        Temp_L1 = largest + (smallest - R)  

        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(Temp_L1)
    
    marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list]
    
    for j in range(len(resultList)):
        plt.plot(resultList[j],label=label_list[j])

    strTitle = "GS=4, GF=2^8, Small(1,100) FixByte "+str(runNum)+"times" 
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("random times")
    xtitle=list(np.array(range(runNum)))

    plt.xticks(xtitle)
    plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show()

# ==========================
class MacrosymbolSize():
    def __init__(self):
        self.tempDataList = None

    def getMultiplePacket2_3mix(self,small,big):
        # dynamic, small, big
        Quo = big // small
        Rem = big % small

        Quotient = []
        for n in range(1,big+1):
            if big % n == 0:
                Quotient.append(n)
        
        for n in Quotient:
            if small <= n:
                Overhead_temp = n - small
                MacroSs = n
                break

        if Overhead_temp <= Quo*Rem and Overhead_temp <= small - Rem:
            # execuate big fix Al
            largest = big 
            # MacroSs = n
            
            
        elif Quo*Rem > small - Rem:
            # excuate small fix Al
            largest = big + (small - Rem)
            MacroSs = small 
            
        else:
            # excuate dynamic fix Al
            largest = big + (Quo-1)*Rem
            MacroSs = small + Rem 
            
        
        return MacroSs, largest, [Quo,Rem]

    def algorithm_mix(self,small,big):
        # dynamic and small fix
        Quo = big // small
        Rem = big % small
        
        # Quotient = []
        # for n in range(1,big+1):
        #     if big % n == 0:
        #         Quotient.append(n)
        
        # for n in Quotient:
        #     if small <= n:
        #         Overhead_temp = n - small
        #         MacroSs = n
        #         break

        # if Overhead_temp <= Quo*Rem and Overhead_temp <= small - Rem:
        #     # execuate big fix Al
        #     Temp_biggest = big
            
        # elif small - Rem <= Quo*Rem :
        if small - Rem <= Quo*Rem :
            # excuate small fix Al
            Temp_biggest = big + (small - Rem)
            MacroSs = small 
           
        else:
            # excuate dynamic fix Al
            Temp_biggest = big + (Quo-1)*Rem
            MacroSs = small + Rem 
            
        
        return MacroSs,Temp_biggest,[Quo,Rem]

    def algorithm_Small_Dynamicv1_v2(self,small,big):
        # dynamic and small fix
        Quo = big // small
        Rem = big % small
        
        Overhead_temp= big

        if Quo >= Rem:
            Temp_biggest = big + (Quo - Rem)
            MacroSs = small + 1
            Overhead_temp = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            MacroSs = small + (Rem // Quo +1)
            Temp_biggest = big + (Rem // Quo +1)*Quo - Rem


        if Overhead_temp <= Quo*Rem and Overhead_temp <= small - Rem:
            # execuate big fix Al
            MacroSs = small + 1
            Temp_biggest = big + (Quo - Rem)
            
        elif small - Rem <= Quo*Rem :
        
            # excuate small fix Al
            Temp_biggest = big + (small - Rem)
            MacroSs = small 
           
        else:
            # excuate dynamic fix Al
            Temp_biggest = big + (Quo-1)*Rem
            MacroSs = small + Rem 
            
        
        return MacroSs,Temp_biggest,[Quo,Rem]

    def algorithm_mix_v3(self,small,big):
        # dynamic and small fix
        Quo = big // small
        Rem = big % small

        MacroSs = small
        Temp_biggest = big

        if Quo >= Rem:
             
            Temp_biggest = big + (Quo -Rem)
            MacroSs = small + 1
            # Overhead_temp = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            # temp = Quo - Rem % Quo
            # Temp_biggest = big + (temp)
            # MacroSs = small + (Rem + temp) // Quo

            MacroSs = small + (Rem // Quo +1)
            Temp_biggest = big + (Rem // Quo +1)*Quo - Rem
            

        return MacroSs,Temp_biggest,[Quo,Rem]

    def algorithm_small_fix(self,small,big):
        # dynamic and small fix
        Quo = big // small
        Rem = big % small

        MacroSs = small
        Temp_biggest = big + (small - Rem)

        return MacroSs,Temp_biggest,[Quo,Rem]



    '''
    def gotGS4GF8_SmallvsMix(self):
        runNum = 150
        GS= 4
        OvOp_list = []
        for i in range(runNum):
            loopNum = 90
            tempDataList = [[random.randint(10,600) for _ in range(GS)] for _ in range(loopNum)]
            
            
            loopNum = len(tempDataList)
            # intervel = 500

            Result_list=[[] for _ in range(16)]

            for i in range(loopNum):
                # L1 = random.randint(10,1400)
                # L2 = random.randint(10,1400)
                tempDataList[i].sort()
                #copy_tempDataList = list(tempDataList[i])
                copy_tempDataList = copy.copy(tempDataList[i])

                # =====================
                # Algorithm  1 mix
                # ======================
                small = tempDataList[i][0]
                big =  tempDataList[i][1]
                
                QuoRem_list = [[0,0]]
                # Overhead, Operation, MacroSs, Temp_biggest 
                tempDataList[i][0], tempDataList[i][1], Quo_Rem = self.getMultiplePacket2(small,big)

                QuoRem_list.append(Quo_Rem)
                
                for j in range(2,GS):
                    small = tempDataList[i][0]
                    big = tempDataList[i][j]

                    tempDataList[i][0], tempDataList[i][j], Quo_Rem= self.getMultiplePacket2(small,big)
                    QuoRem_list.append(Quo_Rem)

                    if tempDataList[i][0] > small:
                        for k in range(1,j):
                            tempDataList[i][k] += QuoRem_list[k][0]*Quo_Rem[1]

                    elif tempDataList[i][0] == small:
                            tempDataList[i][j] += tempDataList[i][0] - Quo_Rem[1]
                    else:
                        print "Macro Size should not be smaller"
                        return -1

                Overhead = 0
                Operation = 0
                
                # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_tempDataList[i][j]
                for j in range(GS):
                    Overhead += tempDataList[i][j] - copy_tempDataList[j]
                    if j< GS -1:
                        Operation += 2* tempDataList[i][j]
                    else:
                        Operation += tempDataList[i][j]
                      
                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]
                    
                Result_list[0].append(Overhead)
                Result_list[1].append(Operation)
                Result_list[2].append(MacroSs)
                Result_list[3].append(Temp_L1)
            
                # =====================
                # Algorithm 2 small fix Al2
                # ======================
                tempDataList[i] = list(copy_tempDataList)
                
                Overhead = 0
                Operation = 2*small
                small = tempDataList[i][0]
                for j in range(1,GS):
                    big = tempDataList[i][j]

                    # Quo = big // small
                    Rem = big % small

                    Overhead += small - Rem
                    tempDataList[i][j] += small - Rem
                    if j< GS -1:
                        Operation += 2* tempDataList[i][j]
                    else:
                        Operation += tempDataList[i][j]

                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]
                    
                Result_list[4].append(Overhead)
                Result_list[5].append(Operation)
                Result_list[6].append(MacroSs)
                Result_list[7].append(Temp_L1)
                
                # =====================
                # Algorithm 3 convertional 
                # ======================
                tempDataList[i] = list(copy_tempDataList)

                Overhead = 0
                Operation = tempDataList[i][-1]*((GS-1)*2+1)
                
                for j in range(GS-1):
                    Overhead += tempDataList[i][GS-1] - tempDataList[i][j]
                    
                    # if j< GS -2:
                    #     Operation += 2* tempDataList[i][-1]
                    # else:
                    #     Operation += tempDataList[i][-1]
                      
                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]
                      
                Result_list[8].append(Overhead)
                Result_list[9].append(Operation)
                Result_list[10].append(MacroSs)
                Result_list[11].append(Temp_L1)
               

            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[8],mean_list[4],mean_list[0]])


            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        
        keysParament_list = ["Operation Conv.3","Operation Al.2","Operation Al.1",\
                         "Overhead Conv.3","Overhead Al.2","Overhead Al.1"]
        
        t = np.arange(runNum)
        for i in range(len(OvOp_list)):
            plt.plot(t,OvOp_list[i],label=keysParament_list[i])
        
        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        plt.plot(t,[np.mean(mean_list[3])]*len(t),label="Al.1 Mean"+str(format(np.mean(mean_list[3]),'.2f')))
        
        strTitle = "GS=2, GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
        plt.title(strTitle)
        plt.grid(True)
        plt.legend()
        plt.xlabel("run times")
        # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.show() 

    def gotGS4GF8_SmallvsMix2vsMix(self):
        runNum = 150
        GS= 4
        OvOp_list = []
        for i in range(runNum):
            loopNum = 90
            tempDataList = [[random.randint(100,600) for _ in range(GS)] for _ in range(loopNum)]
            
            
            loopNum = len(tempDataList)
            # intervel = 500

            Result_list=[[] for _ in range(16)]

            for i in range(loopNum):
                # L1 = random.randint(10,1400)
                # L2 = random.randint(10,1400)
                tempDataList[i].sort()
                #copy_tempDataList = list(tempDataList[i])
                copy_tempDataList = copy.copy(tempDataList[i])

                # =====================
                # Algorithm 1 mix
                # ======================
                small = tempDataList[i][0]
                big =  tempDataList[i][1]
                
                QuoRem_list = [[0,0]]
                # Overhead, Operation, MacroSs, Temp_biggest 
                tempDataList[i][0], tempDataList[i][1], Quo_Rem = self.getMultiplePacket2_v3(small,big)

                QuoRem_list.append(Quo_Rem)
                
                for j in range(2,GS):
                    small = tempDataList[i][0]
                    big = tempDataList[i][j]

                    tempDataList[i][0], tempDataList[i][j], Quo_Rem= self.getMultiplePacket2_v3(small,big)
                    QuoRem_list.append(Quo_Rem)

                    if tempDataList[i][0] > small:
                        for k in range(1,j):
                            tempDataList[i][k] += QuoRem_list[k][0]*Quo_Rem[1]

                    elif tempDataList[i][0] == small:
                            tempDataList[i][j] += tempDataList[i][0] - Quo_Rem[1]
                    else:
                        print "Macro Size should not be smaller"
                        return -1

                Overhead = 0
                Operation = 0
                
                # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_tempDataList[i][j]
                for j in range(GS):
                    Overhead += tempDataList[i][j] - copy_tempDataList[j]
                    if j< GS -1:
                        Operation += 2* tempDataList[i][j]
                    else:
                        Operation += tempDataList[i][j]
                      
                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]
                    
                Result_list[0].append(Overhead)
                Result_list[1].append(Operation)
                Result_list[2].append(MacroSs)
                Result_list[3].append(Temp_L1)
            
                # =====================
                # Algorithm 2 small fix Al2
                # ======================
                tempDataList[i] = list(copy_tempDataList)
                
                Overhead = 0
                Operation = 2*small
                small = tempDataList[i][0]
                for j in range(1,GS):
                    big = tempDataList[i][j]

                    # Quo = big // small
                    Rem = big % small

                    Overhead += small - Rem
                    tempDataList[i][j] += small - Rem
                    if j< GS -1:
                        Operation += 2* tempDataList[i][j]
                    else:
                        Operation += tempDataList[i][j]

                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]
                    
                Result_list[4].append(Overhead)
                Result_list[5].append(Operation)
                Result_list[6].append(MacroSs)
                Result_list[7].append(Temp_L1)

                # =====================
                # Algorithm 3 mix_v2
                # =====================
                small = tempDataList[i][0]
                big =  tempDataList[i][1]
                
                QuoRem_list = [[0,0]]
                # Overhead, Operation, MacroSs, Temp_biggest 
                tempDataList[i][0], tempDataList[i][1], Quo_Rem = self.getMultiplePacket2_v2(small,big)

                QuoRem_list.append(Quo_Rem)
                
                for j in range(2,GS):
                    small = tempDataList[i][0]
                    big = tempDataList[i][j]

                    tempDataList[i][0], tempDataList[i][j], Quo_Rem= self.getMultiplePacket2_v2(small,big)
                    QuoRem_list.append(Quo_Rem)

                    if tempDataList[i][0] > small:
                        for k in range(1,j):
                            tempDataList[i][k] += QuoRem_list[k][0]*Quo_Rem[1]

                    elif tempDataList[i][0] == small:
                            tempDataList[i][j] += tempDataList[i][0] - Quo_Rem[1]
                    else:
                        print "Macro Size should not be smaller"
                        return -1

                Overhead = 0
                Operation = 0
                
                # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_tempDataList[i][j]
                for j in range(GS):
                    Overhead += tempDataList[i][j] - copy_tempDataList[j]
                    if j< GS -1:
                        Operation += 2* tempDataList[i][j]
                    else:
                        Operation += tempDataList[i][j]
                      
                MacroSs = tempDataList[i][0]
                Temp_L1 = tempDataList[i][-1]

                Result_list[8].append(Overhead)
                Result_list[9].append(Operation)
                Result_list[10].append(MacroSs)
                Result_list[11].append(Temp_L1)
               

            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[8],mean_list[4],mean_list[0]])


            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        
        keysParament_list = ["Operation Al.3","Operation Al.2","Operation Al.1",\
                         "Overhead Al.3","Overhead Al.2","Overhead Al.1"]
        
        t = np.arange(runNum)
        for i in range(len(OvOp_list)):
            plt.plot(t,OvOp_list[i],label=keysParament_list[i])
        
        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        plt.plot(t,[np.mean(mean_list[3])]*len(t),label="Al.1 Mean"+str(format(np.mean(mean_list[3]),'.2f')))
        
        strTitle = "GS=2, GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
        plt.title(strTitle)
        plt.grid(True)
        plt.legend()
        plt.xlabel("run times")
        # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.show() 
    '''

    def gotGS4GF8_SmallvsMix2vsMix_PacketLimited(self):
        runNum = 150
        GS= 4
        OvOp_list = []
        for i in range(runNum):
            loopNum = 90
            tempDataList = [[random.randint(100,600) for _ in range(GS)] for _ in range(loopNum)]
            
            
            loopNum = len(tempDataList)
            # intervel = 500

            Result_list=[[] for _ in range(24)]

            for i in range(loopNum):
                # L1 = random.randint(10,1400)
                # L2 = random.randint(10,1400)
                tempDataList[i].sort()
                #copy_tempDataList = list(tempDataList[i])
                copy_tempDataList = copy.copy(tempDataList[i])

                # =====================
                # Algorithm 0 small fix Al2
                # ======================
                small = copy_tempDataList[0]
                big =  copy_tempDataList[1]

                # tempDataList[i] = list(copy_tempDataList)
                # copy_tempDataList = copy.copy(tempDataList[i])
                
                Overhead = 0
                Operation = 2*small
                small = copy_tempDataList[0]
                for j in range(1,GS):
                    big = copy_tempDataList[j]

                    # Quo = big // small
                    Rem = big % small

                    Overhead += small - Rem
                    copy_tempDataList[j] += small - Rem
                    if j< GS -1:
                        Operation += 2* copy_tempDataList[j]
                    else:
                        Operation += copy_tempDataList[j]
                
                MacroSs = copy_tempDataList[0]
                LargestItem = copy_tempDataList[-1]
                    
                Result_list[0].append(Overhead)
                Result_list[1].append(Operation)
                Result_list[2].append(MacroSs)
                Result_list[3].append(LargestItem)

                # =====================
                # Algorithm 1 mix
                # ======================
                # Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(tempDataList[i],self.algorithm_mix)
                    
                # Result_list[4].append(Overhead)
                # Result_list[5].append(Operation)
                # Result_list[6].append(MacroSs)
                # Result_list[7].append(LargestItem)

                # =====================
                # Algorithm 2 mix_v2
                # =====================
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(tempDataList[i],self.algorithm_mix_v2)

                Result_list[8].append(Overhead)
                Result_list[9].append(Operation)
                Result_list[10].append(MacroSs)
                Result_list[11].append(LargestItem)

                # =====================
                # Algorithm 3 mix_v3
                # =====================
                # Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(tempDataList[i],self.algorithm_mix_v3)

                # Result_list[12].append(Overhead)
                # Result_list[13].append(Operation)
                # Result_list[14].append(MacroSs)
                # Result_list[15].append(LargestItem)
               
                # ================
                # Algaric 4 think together
                # ================
                copy_tempDataList = copy.copy(tempDataList[i])

                tempDataList[i].sort()
                copy_DataList = list(tempDataList[i])

                Q = [ copy_DataList[n] / copy_DataList[0] for n in range(GS)]
                R = [ copy_DataList[n] % copy_DataList[0] for n in range(GS)] 

                # Q_R = [R[n]/Q[n] for n in range(GS)]
                # (value,flag_j) = max((v,flag_j) for flag_j,v in enumerate(Q_R)) 
                value = max([R[n]/Q[n] for n in range(GS)])

                if value == 0 :
                    add_macross = 0
                elif 0 < value and value < 1:
                    add_macross = 1
                elif 1 <= value :
                    add_macross = value + 1
                    
                else:
                    print "something muss be wrong, Remanation should not be nagativ"
                    return -1

                Overhead = add_macross
                MacroSs  = copy_tempDataList[0] +add_macross
                Operation = 0
                for n in range(GS):
                    Overhead += Q[n]*add_macross - R[n]
                    if n < GS -1:
                        Operation += 2*(copy_DataList[n] + (Q[n]*add_macross - R[n]))
                    else:
                        Operation += copy_DataList[n] + (Q[n]*add_macross - R[n])
                        LargestItem= copy_DataList[n] + (Q[n]*add_macross - R[n])

                Result_list[16].append(Overhead)
                Result_list[17].append(Operation)
                Result_list[18].append(MacroSs)
                Result_list[19].append(LargestItem)
               

                # ================
                # Algaric 5 fix two edges
                # ================
                copy_tempDataList = copy.copy(tempDataList[i])

                smallest = copy_tempDataList[0]
                biggest = copy_tempDataList[3]

                # Quo = biggest // smallest
                # Rem = biggest % smallest

                # Overhead_temp = big

                copy_tempDataList[0],copy_tempDataList[3],_ = self.algorithm_mix_v2(smallest,biggest)
                Overhead = copy_tempDataList[0] - tempDataList[i][0]
                Overhead += copy_tempDataList[GS-1] - tempDataList[i][GS-1]

                Operation = 2*copy_tempDataList[0]
                for n in range(1,GS-1):
                    smallest = copy_tempDataList[0]
                    biggest = copy_tempDataList[n]
                    _,copy_tempDataList[n],_ = self.algorithm_small_fix(smallest,biggest)
                    Overhead += copy_tempDataList[n] - tempDataList[i][n]
                    Operation += 2*copy_tempDataList[n]

                Operation += copy_tempDataList[GS-1]

                Result_list[20].append(Overhead)
                Result_list[21].append(Operation)
                Result_list[22].append(MacroSs)
                Result_list[23].append(LargestItem)


            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[21],mean_list[17],mean_list[13],mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[20],mean_list[16],mean_list[12],mean_list[8],mean_list[4],mean_list[0]])


            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        
        keysParament_list = ["Operation twoEdge Fix","Operation Mix4","Operation Mix3","Operation Mix2","Operation Mix1","Operation SmallFix",\
                         "Overhead twoEdge Fix","Overhead Mix4","Overhead Mix3","Overhead Mix2","Overhead Mix1","Overhead SmallFix"]
        
        t = np.arange(runNum)
        for i in range(len(OvOp_list)):
            plt.plot(t,OvOp_list[i],label=keysParament_list[i])
        
        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        plt.plot(t,[np.mean(mean_list[3])]*len(t),label="LargPacketSize Mean"+str(format(np.mean(mean_list[3]),'.2f')))
        
        strTitle = "GS=4, GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
        plt.title(strTitle)
        plt.grid(True)
        plt.legend()
        plt.xlabel("run times")
        # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.show() 


    def gotPerformance(self,tempDataList,algorithm):
        # =====================
        # Algorithm 1 mix
        # ======================
        copy_tempDataList = list(tempDataList)

        small = copy_tempDataList[0]
        big =  copy_tempDataList[1]
        
        QuoRem_list = [[0,0]]
        # Overhead, Operation, MacroSs, Temp_biggest 
        copy_tempDataList[0], copy_tempDataList[1], Quo_Rem = algorithm(small,big)

        QuoRem_list.append(Quo_Rem)
        
        for j in range(2,GS):
            small = copy_tempDataList[0]
            big = copy_tempDataList[j]

            copy_tempDataList[0], copy_tempDataList[j], Quo_Rem= algorithm(small,big)
            QuoRem_list.append(Quo_Rem)

            if copy_tempDataList[0] > small:
                for k in range(1,j):
                    copy_tempDataList[k] += QuoRem_list[k][0]*Quo_Rem[1]

            elif copy_tempDataList[0] == small:
                    copy_tempDataList[j] += copy_tempDataList[0] - Quo_Rem[1]
            else:
                print "Macro Size should not be smaller"
                return -1

        Overhead = 0
        Operation = 0
        
        # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_tempDataList[i][j]
        for j in range(GS):
            Overhead += copy_tempDataList[j] - tempDataList[j]
            if j< GS -1:
                Operation += 2* copy_tempDataList[j]
            else:
                Operation += copy_tempDataList[j]
                
        MacroSs = copy_tempDataList[0]
        Temp_L1 = copy_tempDataList[-1]

        
        return Overhead,Operation,MacroSs,Temp_L1

    def gotPerformance_onece(self,tempDataList,algorithm):
        # =====================
        # Algorithm 1 mix
        # ======================
        tempDataList.sort()
        

        copy_tempDataList = list(tempDataList)
        print copy_tempDataList

        small = copy_tempDataList[0]
        big =  copy_tempDataList[1]
        
        QuoRem_list = [[0,0]]
        # Overhead, Operation, MacroSs, Temp_biggest 
        copy_tempDataList[0], copy_tempDataList[1], Quo_Rem = algorithm(small,big)

        QuoRem_list.append(Quo_Rem)
        
        for j in range(2,GS):
            small = copy_tempDataList[0]
            big = copy_tempDataList[j]

            copy_tempDataList[0], copy_tempDataList[j], Quo_Rem= algorithm(small,big)
            QuoRem_list.append(Quo_Rem)

            if copy_tempDataList[0] > small:
                for k in range(1,j):
                    copy_tempDataList[k] += QuoRem_list[k][0]*(copy_tempDataList[0] - small)

            elif copy_tempDataList[0] == small:
                    # copy_tempDataList[j] += copy_tempDataList[0] - Quo_Rem[1]
                    pass
            else:
                print "Macro Size should not be smaller"
                return -1

        Overhead = 0
        Operation = 0
        
        # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_tempDataList[i][j]
        for j in range(GS):
            Overhead += copy_tempDataList[j] - tempDataList[j]
            if j< GS -1:
                Operation += 2* copy_tempDataList[j]
            else:
                Operation += copy_tempDataList[j]
                
        MacroSs = copy_tempDataList[0]
        Temp_L1 = copy_tempDataList[-1]

        
        return copy_tempDataList, [Overhead,Operation,MacroSs,Temp_L1]

def gotDynGS2GF8_Ac1(tempL1L2):
    # runNum = 50
    runNum = len(tempL1L2)
    # intervel = 500
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    
    for i in range(runNum):
        # L1 = random.randint(10,1400)
        # L2 = random.randint(10,1400)
        
        L1 = tempL1L2[i][0]
        L2 = tempL1L2[i][1]
        
        if L2 > L2:
            L1, L2 = L2, L1

        
        Quo =L1//L2
        Rem =L1%L2

        Temp_L1 = L1 + (Quo-1)*Rem
        MacroSs = L2 + Rem 
        Overhead = Quo * Rem
        Operation= 2*(L2 + Rem) + (L1 + (Quo-1)*Rem)
        

        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(Temp_L1)

    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list]
    
    mean_list=[np.mean(item) for item in resultList]
    std_list = [np.std(item) for item in resultList]

        # marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]

    t = np.arange(len(mean_list))
    for i in range(len(mean_list)):
        plt.bar(t[i],mean_list[i],yerr=std_list[i])
        
    
    for x,y,yerr in zip(t,mean_list,std_list):  
         plt.text(x, y, '%.0f   $ \pm $%.0f' % (y,yerr) , ha='center', va= 'bottom',fontsize=12)  
    
   
    strTitle = "GS=2, GF=2^8, Dyn Algorith (1) " + str(runNum)+" times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("smaller packets")
    plt.xticks(t,label_list)
    # plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show() 

def gotDynGS2GF8_Ac2(tempL1L2):
    # runNum = 50
    runNum = len(tempL1L2)
    # intervel = 500
    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    
    for i in range(runNum):
        #L1 = random.randint(10,1400)
        #L2 = random.randint(10,1400)
        
        L1 = tempL1L2[i][0]
        L2 = tempL1L2[i][1]
        
        if L2 > L2:
            L1, L2 = L2, L1

        
        Quo =L1//L2
        Rem =L1%L2

        Temp_L1 = L1 + (L2 - Rem)
        MacroSs = L2 
        Overhead = L2 - Rem
        Operation= 2*L2 + (L1 + (L2 - Rem))
        

        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(Temp_L1)

    resultList = [Overhead_list,Operation_list,MacroSs_list,Temp_L1_list]
        
    mean_list=[np.mean(item) for item in resultList]
    std_list = [np.std(item) for item in resultList]

        # marker_list=['x','-','.','_']
    label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]

    t = np.arange(len(mean_list))
    for i in range(len(mean_list)):
        plt.bar(t[i],mean_list[i],yerr=std_list[i])
    
    for x,y,yerr in zip(t,mean_list,std_list):  
        plt.text(x, y, '%.0f   $ \pm $%.0f' % (y,yerr) , ha='center', va= 'bottom',fontsize=12)  
    
    
    strTitle = "GS=2, GF=2^8, Dyn Algorith (2) " + str(runNum)+" times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("smaller packets")
    plt.xticks(t,label_list)
    # plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show()  

def gotDynGS2GF8_Ac1vsAc2vsAc3():
    runNum = 150

    OvOp_list = []
    for i in range(runNum):
        loopNum = 90
        tempL1L2 = [[random.randint(10,1400),random.randint(10,1400)] for _ in range(loopNum)]

        loopNum = len(tempL1L2)
        # intervel = 500

        Result_list=[[] for _ in range(16)]

        for i in range(loopNum):
            # L1 = random.randint(10,1400)
            # L2 = random.randint(10,1400)

            L1 = tempL1L2[i][0]
            L2 = tempL1L2[i][1]

            if L2 > L2:
                L1, L2 = L2, L1

            # ================
            # Algaric 1 
            # ================
            Quo =L1//L2
            Rem =L1%L2

            Temp_L1 = L1 + (Quo-1)*Rem
            MacroSs = L2 + Rem 
            Overhead = Quo * Rem
            Operation= 2*(L2 + Rem) + (L1 + (Quo-1)*Rem)


            Result_list[0].append(Overhead)
            Result_list[1].append(Operation)
            Result_list[2].append(MacroSs)
            Result_list[3].append(Temp_L1)

            # ================
            # Algaric 2 small fix
            # ================
            #Quo =L1//L2
            #Rem =L1%L2

            Temp_L1 = L1 + (L2 - Rem)
            MacroSs = L2 
            Overhead = L2 - Rem
            Operation= 2*L2 + (L1 + (L2 - Rem))


            Result_list[4].append(Overhead)
            Result_list[5].append(Operation)
            Result_list[6].append(MacroSs)
            Result_list[7].append(Temp_L1)
            
            # ================
            # Algaric 3 big fix
            # ================
            
            Quotient = []
            for n in range(1,L1+1):
                if L1%n == 0:
                    Quotient.append(n)
            
            for n in Quotient:
                if L2 <= n:
                    Temp_L1 = L1 
                    MacroSs = n 
                    Overhead = n - L2
                    Operation= 2*n + L1
                    break


            Result_list[8].append(Overhead)
            Result_list[9].append(Operation)
            Result_list[10].append(MacroSs)
            Result_list[11].append(Temp_L1)


        mean_list=[np.mean(item) for item in Result_list]
        std_list = [np.std(item) for item in Result_list]
        # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
        OvOp_list.append([mean_list[9],mean_list[1],mean_list[5],\
                            mean_list[8],mean_list[4],mean_list[0]])

        
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=np.array(OvOp_list).T
       # marker_list=['x','-','.','_']
        
    #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
    #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    
    keysParament_list = ["Operation Ac3","Operation Ac1","Operation Ac2", \
                         "Overhead Ac3","Overhead Ac2","Overhead Ac1"]
    
    t = np.arange(runNum)
    for i in range(len(OvOp_list)):
        plt.plot(t,OvOp_list[i],label=keysParament_list[i])
    
    
    strTitle = "GS=2, GF=2^8, Dyn Algorith 1vs2vs3 " + str(runNum)+" times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("run times")
    # plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show() 

def gotDynGS2GF8_Ac1vsAc2vsAc3_Bar():
    runNum = 50
    OvOp_list = []
    for i in range(runNum):
        loopNum = 90
        tempL1L2 = [[random.randint(10,1400),random.randint(10,1400)] for _ in range(loopNum)]

        loopNum = len(tempL1L2)
        # intervel = 500

        Result_list=[[] for _ in range(16)]

        for i in range(loopNum):
            # L1 = random.randint(10,1400)
            # L2 = random.randint(10,1400)

            L1 = tempL1L2[i][0]
            L2 = tempL1L2[i][1]

            if L2 > L2:
                L1, L2 = L2, L1

            # ================
            # Algaric 1 
            # ================
            Quo =L1//L2
            Rem =L1%L2

            Temp_L1 = L1 + (Quo-1)*Rem
            MacroSs = L2 + Rem 
            Overhead = Quo * Rem
            Operation= 2*(L2 + Rem) + (L1 + (Quo-1)*Rem)


            Result_list[0].append(Overhead)
            Result_list[1].append(Operation)
            Result_list[2].append(MacroSs)
            Result_list[3].append(Temp_L1)

            # ================
            # Algaric 2 small fix
            # ================
            #Quo =L1//L2
            #Rem =L1%L2

            Temp_L1 = L1 + (L2 - Rem)
            MacroSs = L2 
            Overhead = L2 - Rem
            Operation= 2*L2 + (L1 + (L2 - Rem))


            Result_list[4].append(Overhead)
            Result_list[5].append(Operation)
            Result_list[6].append(MacroSs)
            Result_list[7].append(Temp_L1)
            
            # ================
            # Algaric 3 big fix
            # ================
            
            Quotient = []
            for n in range(1,L1+1):
                if L1%n == 0:
                    Quotient.append(n)
            
            for n in Quotient:
                if L2 <= n:
                    Temp_L1 = L1 
                    MacroSs = n 
                    Overhead = n - L2
                    Operation= 2*n + L1
                    break


            Result_list[8].append(Overhead)
            Result_list[9].append(Operation)
            Result_list[10].append(MacroSs)
            Result_list[11].append(Temp_L1)


        mean_list=[np.mean(item) for item in Result_list]
        std_list = [np.std(item) for item in Result_list]
        # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
        OvOp_list.append([mean_list[1],mean_list[5],mean_list[9],mean_list[4],mean_list[0],mean_list[8]])
        
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=list(np.array(OvOp_list).T)
    
    mean_runTimes = [np.mean(item) for item in OvOp_list]
    std_runTimes = [np.mean(item) for item in OvOp_list]
    
    
       # marker_list=['x','-','.','_']
        
    #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
    #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    
    keysParament_list = ["Operation Ac1","Operation Ac2","Operation Ac3", \
                         "Overhead Ac2","Overhead Ac1","Overhead Ac3"]
    
    t = np.arange(len(keysParament_list))
    for i in range(len(keysParament_list)):
        plt.bar(t[i],mean_runTimes[i],yerr=std_runTimes[i])
    
    plt.xticks(t,keysParament_list)
    strTitle = "GS=2, GF=2^8, Dyn Algorith 1vs2vs3" + str(runNum)+" times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("run times")
    # plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show() 

def GS2GF8_SmallBigDynamicAlgorithm():
    runNum = 150

    OvOp_list = []
    for i in range(runNum):
        loopNum = 90
        dataList = [[random.randint(400,500),random.randint(400,500)] for _ in range(loopNum)]

        loopNum = len(dataList)
        # intervel = 500

        Result_list=[[] for _ in range(24)]

        for i in range(loopNum):
            # L1 = random.randint(10,1400)
            # L2 = random.randint(10,1400)

            dataList[i].sort()

            smaller = dataList[i][0]
            larger = dataList[i][1]

            Quo =larger//smaller
            Rem =larger%smaller
            
            # ================
            # Algorithm 1 small fix
            # ================
            #Quo =larger//smaller
            #Rem =larger%smaller

            Temp_L1 = larger + (smaller - Rem)
            MacroSs = smaller 
            Overhead = smaller - Rem
            Operation= 2*smaller + (larger + (smaller - Rem))

            Result_list[0].append(Overhead)
            Result_list[1].append(Operation)
            Result_list[2].append(MacroSs)
            Result_list[3].append(Temp_L1)

            # ================
            # Algorithm 2 big fix
            # ================

            Quotient = []
            for n in range(1,larger+1):
                if larger%n == 0:
                    Quotient.append(n)
            
            for n in Quotient:
                if smaller <= n:
                    Temp_L1 = larger 
                    MacroSs = n 
                    Overhead_temp= n - smaller
                    Overhead = n - smaller
                    Operation= 2*n + larger
                    break

            Result_list[4].append(Overhead)
            Result_list[5].append(Operation)
            Result_list[6].append(MacroSs)
            Result_list[7].append(Temp_L1)
            
            
            # ================
            # Algorithm 3 dynamic v1
            # ================
            Temp_L1 = larger + (Quo-1)*Rem
            MacroSs = smaller + Rem 
            Overhead = Quo * Rem
            Operation= 2*(smaller + Rem) + (larger + (Quo-1)*Rem)
            
            Result_list[8].append(Overhead)
            Result_list[9].append(Operation)
            Result_list[10].append(MacroSs)
            Result_list[11].append(Temp_L1)
            
            # ================
            # Algaric 4 mix dynamic v2
            # ================

            if Quo >= Rem:
                Temp_L1 = larger + (Quo -Rem)
                MacroSs = smaller + 1
                Overhead = (Quo -Rem) + 1
                # Operation= 2*(smaller +1) + larger + (Quo - Rem)
            else:
                MacroSs = smaller + (Rem // Quo +1)
                Temp_L1 = larger + (Rem // Quo +1)*Quo - Rem

            Operation= 2*MacroSs + Temp_L1

            Result_list[12].append(Overhead)
            Result_list[13].append(Operation)
            Result_list[14].append(MacroSs)
            Result_list[15].append(Temp_L1)
            # ================
            # Algorithm 4 mix dynamic and small fix
            # ================
                
            if Quo*Rem > smaller - Rem:
                # excuate small fix Al
                Temp_L1 = larger + (smaller - Rem)
                MacroSs = smaller 
                Overhead = smaller - Rem
                Operation= 2*smaller + (larger + (smaller - Rem))
            else:
                # excuate dynamic fix Al
                Temp_L1 = larger + (Quo-1)*Rem
                MacroSs = smaller + Rem 
                Overhead = Quo * Rem
                Operation= 2*(smaller + Rem) + (larger + (Quo-1)*Rem)

            Result_list[16].append(Overhead)
            Result_list[17].append(Operation)
            Result_list[18].append(MacroSs)
            Result_list[19].append(Temp_L1)
            

            # ================
            # Algorithm 5 mix dynamic,small,big fix
            # ================
            
            Overhead_temp3 = 2*larger

            for n in Quotient:
                if smaller <= n:
                    Overhead_temp3 = n - smaller
                    MacroSs = n
                    break

            Overhead_temp6 = 2*larger
            if Quo >= Rem:
                Temp_L1 = larger + (Quo -Rem)
                MacroSs = smaller + 1
                Overhead_temp6 = (Quo -Rem) + 1
                # Operation= 2*(smaller +1) + larger + (Quo - Rem)
            else:
                for n in range(1,Quo+1):
                    if (Rem + n ) % Quo ==0:
                        Temp_L1 = larger + n
                        MacroSs = smaller + ( Rem + n )// Quo
                        Overhead_temp6 = ( Rem + n )// Quo + n
                        break


            if Overhead_temp3 <= Quo*Rem and Overhead_temp3 <= smaller - Rem and Overhead_temp3 <= Overhead_temp6 :
                # execuate big fix Al
                Temp_L1 = larger
                
                Overhead = Overhead_temp3
                # Operation= 2*n + larger
                
            elif smaller - Rem <= Quo*Rem and smaller - Rem <=  Overhead_temp6 :
                # excuate small fix Al
                Temp_L1 = larger + (smaller - Rem)
                MacroSs = smaller 
                Overhead = smaller - Rem
                # Operation= 2*smaller + (larger + (smaller - Rem))
            elif Quo*Rem <= Overhead_temp6:
                # excuate dynamic fix Al
                Temp_L1 = larger + (Quo-1)*Rem
                MacroSs = smaller + Rem 
                Overhead = Quo * Rem
            else:
                pass
            
            Operation= 2*MacroSs + Temp_L1


            Result_list[20].append(Overhead)
            Result_list[21].append(Operation)
            Result_list[22].append(MacroSs)
            Result_list[23].append(Temp_L1)

            

        mean_list=[np.mean(item) for item in Result_list]
        std_list = [np.std(item) for item in Result_list]
        # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
        OvOp_list.append([mean_list[9],mean_list[1],mean_list[5],mean_list[13],mean_list[17],mean_list[21],\
                            mean_list[8],mean_list[4],mean_list[0],mean_list[12],mean_list[16],mean_list[20]])

        
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=np.array(OvOp_list).T
       # marker_list=['x','-','.','_']
        
    #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
    #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    
    keysParament_list = ["Operation DynamicV1","OPeration SmallFix","Operation BigFix", "Operation DynamicV2", "Operation mix1","Operation mix2",\
                         "Small DynamicV1","Ohead SmallFix","Small BigFix","Small DynamicV2","Small mix1","Small mix2"]
    
    t = np.arange(runNum)
    for i in range(len(OvOp_list)):
        plt.plot(t,OvOp_list[i],label=keysParament_list[i])
    
    
    strTitle = "GS=2, GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
    plt.title(strTitle)
    plt.grid(True)
    plt.legend()
    plt.xlabel("run times")
    # plt.savefig('./MacroFig'+strTitle+'.png')
    plt.show() 


def thinkTogetherGS4():
    runNum = 150
    GS= 4
    OvOp_list = []
    for i in range(runNum):
        loopNum = 90
        tempDataList = [[random.randint(100,600) for _ in range(GS)] for _ in range(loopNum)]
        
        
        loopNum = len(tempDataList)
        # intervel = 500

        Result_list=[[] for _ in range(16)]

        for i in range(loopNum):
            tempDataList[i].sort()
            copy_DataList = list(tempDataList[i])

            Q = [ copy_DataList[n] / copy_DataList[0] for n in range(GS)]
            R = [ copy_DataList[n] % copy_DataList[0] for n in range(GS)] 

            Q_R = [R[n]/Q[n] for n in range(GS)]
            (value,flag_j) = max((v,flag_j) for flag_j,v in enumerate(Q_R)) 

            if value == 0 :
                add_macross = 0
            elif 0 < value and value < 1:
                add_macross = 1
            elif 1 <= value :
                add_macross = value + 1
                
            else:
                print "something muss be wrong, Remanation should not be nagativ"
                return -1

            Overhead = add_macross
            for n in range(GS):
                Overhead += Q[n]*add_macross - R[n]

            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[13],mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[12],mean_list[8],mean_list[4],mean_list[0]])


            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        
        keysParament_list = ["Operation Mix3","Operation Special","Operation Mix1","Operation Al.0",\
                         "Overhead Mix3","Overhead Special","Overhead Mix1","Overhead Al.0"]
        
        t = np.arange(runNum)
        for i in range(len(OvOp_list)):
            plt.plot(t,OvOp_list[i],label=keysParament_list[i])
        
        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        plt.plot(t,[np.mean(mean_list[3])]*len(t),label="Al.1 Mean"+str(format(np.mean(mean_list[3]),'.2f')))
        
        strTitle = "GS=4, GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
        plt.title(strTitle)
        plt.grid(True)
        plt.legend()
        plt.xlabel("run times")
        # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.show() 


def GS2GF8(L1):
    Quotient = []
    for n in range(1,L1+1):
        if L1 % n == 0 :
            Quotient.append(n)
    print (Quotient)
    
    result = []

    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    # Dynamic
    for L2 in range(1,L1+1):
        Quo =L1//L2
        Rem =L1%L2
       
        Overhead = Quo * Rem
        Operation= 2*(L2 + Rem) + (L1 + (Quo-1)*Rem)
        MacroSs = L2 + Rem 
        Temp_L1 = L1 + (Quo-1)*Rem

        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(Temp_L1)

    result.append([Overhead_list,Operation_list,MacroSs_list,Temp_L1_list])

    Overhead_list=[]
    Operation_list=[]
    MacroSs_list = []
    Temp_L1_list = []
    # Fix
    for L2 in range(1,L1+1):   
        

        for item in Quotient:
            if L2 <= item:
                MacroSs = item
                Overhead = item-L2
                Operation=L1+2*MacroSs
                break
        Overhead_list.append(Overhead)
        Operation_list.append(Operation)
        MacroSs_list.append(MacroSs)
        Temp_L1_list.append(L1)

    result.append([Overhead_list,Operation_list,MacroSs_list,Temp_L1_list])

    return result


def showDiffer(Differ):
    Differitem = sorted(list(set(Differ)))
    R = [Differ.count(item) for item in Differitem]
    #print ("set(Differ)",(Differ))
    #t = np.arrange
    #print ("np.linspace(1,len(R),1)",np.linspace(1,len(R),1))
    plt.bar(np.arange(len(R)),R)
    xtitle=[str(i) for i in Differitem]
    #print xtitle
    plt.xticks(np.arange(len(R)),xtitle)
    plt.plot(R, color='r')
    plt.show()

if __name__=="__main__":  

    
    # gotFixSmallGS4GF8()
    # gotFixBigGS4GF8()
    # gotFixSmallGS2GF8(400)
    # gotFixBigGS2GF8(400)
    # gotDynGS2GF8(400)
    
    # gotDynGS2GF8_Ac1vsAc2vsAc3()
    # gotDynGS2GF8_Ac1vsAc2vsAc3_Bar()
    # gotDynGS2GF8_Al1vsAl2vsAl3vsAl4vsAl5()
    # Show().showParameter(GS2GF8(800))
    # Show().showDynFix(GS2GF8(800))
    # Show().showDynFix(GS2GF8(800))
    # MacrosymbolSize().gotGS4GF8_SmallvsMix2vsMix_PacketLimited()

    GS2GF8_SmallBigDynamicAlgorithm()

    # GS = 4
    # runTimes = 4
    # dataM = [[random.randint(10,1400) for _ in range(GS)] for _ in range(runTimes)]
    # for item in dataM:
    #     # print item
    #     # organized_item, result = MacrosymbolSize().gotPerformance_onece(item, MacrosymbolSize().algorithm_mix_v3)
    #     # print organized_item
    #     # print "Overhead: " + str(result[0]) +" | Operation: "+str(result[1]) \
    #     #         +" | MacroSymbol Size: " +str(result[2]) +" | Biggest Item: "+str(result[3])+"\n"

    #     # item.sort()
    #     # small = item[0]
    #     # big = item[1]
    #     # print str(small),"|",str(big)
    #     # small,big,_ = MacrosymbolSize().algorithm_mix_v3(small,big)
    #     # print str(small),"|",str(big)+"\n"

    #     print item
    #     item.sort()
    #     copy_DataList = list(item)
    #     print copy_DataList

    #     Q = [ copy_DataList[n] / copy_DataList[0] for n in range(GS)]
    #     R = [ copy_DataList[n] % copy_DataList[0] for n in range(GS)] 

    #     # Q_R = [R[n]/Q[n] for n in range(GS)]
    #     # (value,flag_j) = max((v,flag_j) for flag_j,v in enumerate(Q_R)) 
    #     value = max([R[n]/Q[n] for n in range(GS)])

    #     if value == 0 :
    #         add_macross = 0
    #     elif 0 < value and value < 1:
    #         add_macross = 1
    #     elif 1 <= value :
    #         add_macross = value + 1
            
    #     else:
    #         print "something muss be wrong, Remanation should not be nagativ"

    #     Overhead = add_macross
    #     MacroSs  = copy_DataList[0] +add_macross
    #     Operation = 0
    #     for n in range(GS):
    #         Overhead += Q[n]*add_macross - R[n]
    #         copy_DataList[n] += Q[n]*add_macross - R[n]

    #         if n < GS -1:
    #             Operation += 2*(copy_DataList[n] + (Q[n]*add_macross - R[n]))
    #         else:
    #             Operation += copy_DataList[n] + (Q[n]*add_macross - R[n])
    #             LargestItem= copy_DataList[n] + (Q[n]*add_macross - R[n])
        
    #     print copy_DataList
    #     print "Overhead: " + str(copy_DataList[0]) +" | Operation: "+str(copy_DataList[1]) \
    #             +" | MacroSymbol Size: " +str(copy_DataList[2]) +" | Biggest Item: "+str(copy_DataList[3])+"\n"
