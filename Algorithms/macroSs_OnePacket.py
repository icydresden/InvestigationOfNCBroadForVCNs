#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import math
import numpy as np
import random
import copy
import matplotlib.pylab as pl
import json
import pandas as pd

#GS = 4
# ==========================
class MacrosymbolSize():
    def __init__(self):
        self.tempDataList = None
        #self.twoEdge_OH = None

    # mix 1
    def Alg_Small_DynamicV1(self,small,big):
        # dynamic and small fix 
        # mix 1
        Quo = big // small
        Rem = big % small
        
        
        if small - Rem <= Quo*Rem :
            # excuate small fix Al
            Temp_biggest = big + (small - Rem)
            MacroSs = small 
           
        else:
            # excuate dynamic fix Al
            Temp_biggest = big + (Quo-1)*Rem
            MacroSs = small + Rem 
            
        
        return MacroSs,Temp_biggest,[Quo,Rem]

    # mix 2
    def Alg_Small_Dynamicv1_v2(self,small,big):
        # dynamic and small fix
        # mix 2
        Quo = big // small
        Rem = big % small
        
        # print "big / small = "+str(big)+"/"+str(small)
        # print "Rem / Quo = "+ str(Rem)+"/"+str(Quo)
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

    # dynamic v2
    def Alg_DynamicV2(self,small,big):
        # dynamic and small fix
        # print "big / small = "+ str(big)+"/"+str(small)
        Quo = big // small
        Rem = big % small

        assert(Quo > 0)
        # MacroSs = small
        # Temp_biggest = big

        if Quo >= Rem:
             
            Temp_biggest = big + (Quo -Rem)
            MacroSs = small + 1
            # Overhead_temp = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            # temp = Quo - Rem % Quo
            # Temp_biggest = big + (temp)
            # MacroSs = small + (Rem + temp) // Quo
            MacroSs = small + (Rem // Quo) +1
            Temp_biggest = big + (Rem//Quo +1)*Quo - Rem
            

        return MacroSs,Temp_biggest,[Quo,Rem]

    # smallFix
    def Alg_Small_Fix(self,small,big):
        # dynamic and small fix
        Quo = big // small
        Rem = big % small

        MacroSs = small
        Temp_biggest = big + (small - Rem)

        return MacroSs,Temp_biggest,[Quo,Rem]



    def GS4GF8_fullrandom(self):
        runNum = 200 #150
        GS= 2
        OvOp_list = []
        twoEdge_OH = []
        largest_item = []
        for _ in range(runNum):
            
            # tempDataList = [[random.randint(10,1400) for _ in range(GS)] for _ in range(loopTimes)]
            
            
            # loopNum = len(tempDataList)
            # intervel = 500
            loopTimes = 200 # 90
            Result_list=[[] for _ in range(24)]

            for i in range(loopTimes):
                # L1 = random.randint(10,1400)
                # L2 = random.randint(10,1400)
                tempDataList = [random.randint(20,1400) for _ in range(GS)]
                tempDataList.sort()
                
                # =====================
                # Algorithm 0 small fix Al2
                # ======================
                
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_Fix)
                    
                Result_list[0].append(Overhead)
                Result_list[1].append(Operation)
                Result_list[2].append(MacroSs)
                Result_list[3].append(LargestItem)

                # =====================
                # Algorithm 1 Alg_Small_DynamicV1
                # ======================
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_DynamicV1)
                    
                Result_list[4].append(Overhead)
                Result_list[5].append(Operation)
                Result_list[6].append(MacroSs)
                Result_list[7].append(LargestItem)

                # =====================
                # Algorithm 2 Alg_Small_Dynamicv1_v2
                # =====================
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_Dynamicv1_v2)

                Result_list[8].append(Overhead)
                Result_list[9].append(Operation)
                Result_list[10].append(MacroSs)
                Result_list[11].append(LargestItem)

                # =====================
                # Algorithm 3 Alg_DynamicV2
                # =====================
                # tempDataList.sort()
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_DynamicV2)

                Result_list[12].append(Overhead)
                Result_list[13].append(Operation)
                Result_list[14].append(MacroSs)
                Result_list[15].append(LargestItem)
               
                # ================
                # Algorithm 4 think together
                # ================
                # copy_tempDataList = copy.copy(tempDataList)

                tempDataList.sort()
                copy_DataList = list(tempDataList)

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
                MacroSs  = copy_DataList[0] +add_macross
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
                # Algorithm 5 fix two edges
                # ================
                copy_DataList = copy.copy(tempDataList)

                smallest = copy_DataList[0]
                biggest = copy_DataList[-1]

                # Quo = biggest // smallest
                # Rem = biggest % smallest

                # Overhead_temp = big
                
                copy_DataList[0],copy_DataList[-1],_ = self.Alg_Small_Dynamicv1_v2(smallest,biggest)

                Overhead = copy_DataList[0] - tempDataList[0]
                Overhead += copy_DataList[GS-1] - tempDataList[GS-1]

                Operation = 2*copy_DataList[0]
                for n in range(1,GS-1):
                    smallest = copy_DataList[0]
                    biggest = copy_DataList[n]
                    _,copy_DataList[n],_ = self.Alg_Small_Fix(smallest,biggest)
                    Overhead += copy_DataList[n] - tempDataList[n]
                    Operation += 2*copy_DataList[n]

                Operation += copy_DataList[GS-1]

                Result_list[20].append(Overhead)
                Result_list[21].append(Operation)
                Result_list[22].append(MacroSs)
                Result_list[23].append(LargestItem)


            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            

            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[21],mean_list[17],mean_list[13],mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[20],mean_list[16],mean_list[12],mean_list[8],mean_list[4],mean_list[0]])

            twoEdge_OH.append(mean_list[20])
            largest_item.append([mean_list[23]])
            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        fileName= "RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopTimes)
        with open("./twoEdgeFig/"+fileName+".json","w") as output:
            json.dump(twoEdge_OH,output)
        # self.show_plot(OvOp_list,GS,runNum,largest_item)
        print "twoEdge,",np.round(twoEdge_OH)
        self.show_twoEdge_OH(GS,np.round(twoEdge_OH))


    def GS4GF8_FixOnePacket(self):
        runNum = 200 #150
        GS= 4
        OvOp_list = []
        twoEdge_OH = []
        largest_item = []
        for _ in range(runNum):
            
            loopTimes = 200 # 90
            Result_list=[[] for _ in range(24)]

            for i in range(loopTimes):
                # L1 = random.randint(10,1400)
                # L2 = random.randint(10,1400)
                tempDataList = [10] + [random.randint(20,1400) for _ in range(GS-1)]
                tempDataList.sort()
                
                # =====================
                # Algorithm 0 small fix Al2
                # ======================
                
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_Fix)
                    
                Result_list[0].append(Overhead)
                Result_list[1].append(Operation)
                Result_list[2].append(MacroSs)
                Result_list[3].append(LargestItem)

                # =====================
                # Algorithm 1 Alg_Small_DynamicV1
                # ======================
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_DynamicV1)
                    
                Result_list[4].append(Overhead)
                Result_list[5].append(Operation)
                Result_list[6].append(MacroSs)
                Result_list[7].append(LargestItem)

                # =====================
                # Algorithm 2 Alg_Small_Dynamicv1_v2
                # =====================
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_Small_Dynamicv1_v2)

                Result_list[8].append(Overhead)
                Result_list[9].append(Operation)
                Result_list[10].append(MacroSs)
                Result_list[11].append(LargestItem)

                # =====================
                # Algorithm 3 Alg_DynamicV2
                # =====================
                # tempDataList.sort()
                Overhead,Operation,MacroSs,LargestItem = self.gotPerformance(GS,tempDataList,self.Alg_DynamicV2)

                Result_list[12].append(Overhead)
                Result_list[13].append(Operation)
                Result_list[14].append(MacroSs)
                Result_list[15].append(LargestItem)
                
                # ================
                # Algorithm 4 think together
                # ================
                # copy_tempDataList = copy.copy(tempDataList)

                tempDataList.sort()
                copy_DataList = list(tempDataList)

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
                MacroSs  = copy_DataList[0] +add_macross
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
                # Algorithm 5 fix two edges
                # ================
                copy_DataList = copy.copy(tempDataList)

                smallest = copy_DataList[0]
                biggest = copy_DataList[-1]

                # Quo = biggest // smallest
                # Rem = biggest % smallest

                # Overhead_temp = big
                
                copy_DataList[0],copy_DataList[-1],_ = self.Alg_Small_Dynamicv1_v2(smallest,biggest)

                Overhead = copy_DataList[0] - tempDataList[0]
                Overhead += copy_DataList[GS-1] - tempDataList[GS-1]

                Operation = 2*copy_DataList[0]
                for n in range(1,GS-1):
                    smallest = copy_DataList[0]
                    biggest = copy_DataList[n]
                    _,copy_DataList[n],_ = self.Alg_Small_Fix(smallest,biggest)
                    Overhead += copy_DataList[n] - tempDataList[n]
                    Operation += 2*copy_DataList[n]

                Operation += copy_DataList[GS-1]

                Result_list[20].append(Overhead)
                Result_list[21].append(Operation)
                Result_list[22].append(MacroSs)
                Result_list[23].append(LargestItem)


            mean_list=[np.mean(item) for item in Result_list]
            std_list = [np.std(item) for item in Result_list]
            
            

            # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
            OvOp_list.append([mean_list[21],mean_list[17],mean_list[13],mean_list[9],mean_list[5],mean_list[1],\
                            mean_list[20],mean_list[16],mean_list[12],mean_list[8],mean_list[4],mean_list[0]])

            twoEdge_OH.append(mean_list[20])
            largest_item.append([mean_list[23]])
            
        print "OvOp_list,",np.array(OvOp_list).shape
        OvOp_list=np.array(OvOp_list).T
        # marker_list=['x','-','.','_']
            
        #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
        #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
        fileName= "FixOnePacket_RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopTimes)
        with open("./twoEdgeFig/"+fileName+".json","w") as output:
            json.dump(twoEdge_OH,output)
        # self.show_plot(OvOp_list,GS,runNum,largest_item)
        print "twoEdge,",np.round(twoEdge_OH)
        self.show_twoEdge_OH(GS,np.round(twoEdge_OH))



    def show_plot(self,OvOp_list,GS,runNum,largest_item):    
        keysParament_list1 = ["Operation twoEdge Fix","Operation DynamicV3","Operation DynamicV2","Operation SmallDyV1V2","Operation SmallDyV1","Operation SmallFix"]
        keysParament_list2 = ["Overhead twoEdge Fix","Overhead DynamicV3","Overhead DynamicV2","Overhead SmallDyV1V2","Overhead SmallDyV1","Overhead SmallFix"]
        
        # keysParament_list = ["Operation twoEdge Fix","Operation DynamicV3","Operation DynamicV2","Operation SmallDyV1V2","Operation SmallDyV1","Operation SmallFix",\
        #                  "Overhead twoEdge Fix","Overhead DynamicV3","Overhead DynamicV2","Overhead SmallDyV1V2","Overhead SmallDyV1","Overhead SmallFix"]

        half = len(OvOp_list)//2
        print "Half:",half
        fig, axs = plt.subplots(1,2)
        t = np.arange(runNum)
        for i in range(half):
            axs[0].plot(t,OvOp_list[i],label=keysParament_list1[i])
            axs[1].plot(t,OvOp_list[i+half],label=keysParament_list2[i])
        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        axs[1].plot(t,[np.mean(largest_item)]*len(t),label="LargPacketSize Mean"+str(format(np.mean(largest_item),'.2f')))

        axs[0].grid(True)
        axs[0].set_xlabel("run times")
        axs[1].grid(True)
        axs[1].set_xlabel("run times")
        axs[0].legend()
        axs[1].legend()

        strTitle = "GS="+str(GS)+", GF=2^8, Dyn Algorithm 1vs2vs3vs4vs5 " + str(runNum)+" times"
        fig.suptitle(strTitle)
        
        
        # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.show() 

    def show_twoEdge_OH(self,GS,twoEdge_OH):
        result=[]
        xresult = []
        yresult = []
        item_twoEdge = list(set(twoEdge_OH))
        item_twoEdge.sort()

        copy_twoEdge_OH = list(twoEdge_OH)
        copy_twoEdge_OH.sort()

        # xticks_str = [str(item) for item in item_twoEdge]
        
        for item in item_twoEdge:
            result.append(copy_twoEdge_OH.count(item))
        print "result:",result
        xresult = np.array(result)/float(sum(result))

        print "xresult,",xresult
        temp = 0
        for n in xresult:
            temp += n
            yresult.append(temp)

        

        # pl.xticks(rotation=360)
        fig, axs = plt.subplots(2,1)
        axs[0].bar(item_twoEdge,result)
        # axs[0].set_xticks(np.arange(len(item_twoEdge)),xticks_str)
        axs[0].set_xticks(item_twoEdge)
        axs[0].set_title("Distribution Function")
        axs[0].set_ylabel("Times")
        axs[0].set_xlabel("Overhead Sizes")
        
        for tick in axs[0].get_xticklabels():
            tick.set_rotation(90)
            


        axs[1].step(item_twoEdge,yresult)
        # axs[1].plot(np.arange(len(item_twoEdge)),yresult,'b--')
        # axs[1].set_xticks(np.arange(len(item_twoEdge)),xticks_str)
        axs[1].set_xticks(item_twoEdge)
        axs[1].set_title("Cumulative Distribution Function")
        axs[1].set_ylabel("Percentage")
        axs[1].set_xlabel("Overhead Sizes")
        # axs[1].set_xscale('log')
        for tick in axs[1].get_xticklabels():
            tick.set_rotation(90)


        strTitle = "Overhead of TwoEdgeFix Algorithm Packet Size[100 ~ 1400] GS:" +str(GS)
        fig.suptitle(strTitle)
        
        fig.tight_layout()
        plt.xticks(fontsize=10)
        plt.show()


    def gotPerformance(self,GS,tempDataList,algorithm):
        copy_DataList = list(tempDataList)
        # copy_DataList.sort()

        small = copy_DataList[0]
        big =  copy_DataList[1]
        
        QuoRem_list = [[0,0]]
        # Overhead, Operation, MacroSs, Temp_biggest 
        copy_DataList[0], copy_DataList[1], Quo_Rem = algorithm(small,big)

        QuoRem_list.append(Quo_Rem)
        
        for j in range(2,GS):
            if copy_DataList[0] > copy_DataList[j]:
                copy_DataList[0], copy_DataList[j] = copy_DataList[j], copy_DataList[0]

            small = copy_DataList[0]
            big = copy_DataList[j]

            copy_DataList[0], copy_DataList[j], Quo_Rem= algorithm(small,big)
            QuoRem_list.append(Quo_Rem)

            if copy_DataList[0] > small:
                for k in range(1,j):
                    copy_DataList[k] += QuoRem_list[k][0]*Quo_Rem[1]

            elif copy_DataList[0] == small:
                    copy_DataList[j] += copy_DataList[0] - Quo_Rem[1]
            else:
                print "Macro Size should not be smaller"
                return -1

        Overhead = 0
        Operation = 0
        
        # print "tempDataList[i][j]:\n",tempDataList[i][j],'\n',copy_DataList[i][j]
        for j in range(GS):
            Overhead += copy_DataList[j] - tempDataList[j]
            if j< GS -1:
                Operation += 2* copy_DataList[j]
            else:
                Operation += copy_DataList[j]
                
        MacroSs = copy_DataList[0]
        Temp_L1 = copy_DataList[-1]

        
        return Overhead,Operation,MacroSs,Temp_L1

    def gotPerformance_print(self,GS,tempDataList,algorithm):
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

        print "tempDataList:",tempDataList
        print "copy_temList:",copy_tempDataList
        print "Overhead: " + str(copy_tempDataList[0]) +" | Operation: "+str(copy_tempDataList[1]) \
                    +" | MacroSymbol Size: " +str(copy_tempDataList[2]) +" | Biggest Item: "+str(copy_tempDataList[3])+"\n"
        # return copy_tempDataList, [Overhead,Operation,MacroSs,Temp_L1]


def GS2GF8_Algorithms():
    runNum = 150
    GS = 2
    OvOp_list = []
    for i in range(runNum):
        loopNum = 90

        Result_list=[[] for _ in range(24)]

        for i in range(loopNum):
            dataList = [10, random.randint(60,1200)]
            # L1 = random.randint(10,1400)
            # L2 = random.randint(10,1400)

            dataList.sort()

            smaller = dataList[0]
            larger = dataList[1]

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
            # Algaric 4 dynamic v2
            # ================

            if Quo >= Rem:
                Temp_L1 = larger + (Quo -Rem)
                MacroSs = smaller + 1
                Overhead = (Quo - Rem) + 1
                # Operation= 2*(smaller +1) + larger + (Quo - Rem)
            else:
                MacroSs = smaller + (Rem // Quo +1)
                Temp_L1 = larger + (Rem // Quo +1)*Quo -Rem
                Overhead = (Rem // Quo +1) + (Rem // Quo +1)*Quo -Rem

            Operation= 2*MacroSs + Temp_L1

            Result_list[12].append(Overhead)
            Result_list[13].append(Operation)
            Result_list[14].append(MacroSs)
            Result_list[15].append(Temp_L1)
            # ================
            # Algorithm 5 mix dynamicV1 and small fix
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
            # Algorithm 6 mix dynamicV1V2,small,big fix
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
        
        OvOp_list.append([mean_list[20],mean_list[16],mean_list[4],mean_list[12],mean_list[8],mean_list[0]])
        
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=np.array(OvOp_list).T
       # marker_list=['x','-','.','_']

    boxplot_result = []
    fig, axs = plt.subplots(2,1)

    Al_Group = ['Samll&Big&DyV1V2','Small&DyV1','BigFix','DynamicV2','DynamicV1','SmallFix']
    for i in range(6):
        result=[]
        xresult = []
        yresult = []
        item_twoEdge = list(set(OvOp_list[i]))
        item_twoEdge.sort()

        copy_twoEdge_OH = list(OvOp_list[i])
        copy_twoEdge_OH.sort()

        # xticks_str = [str(item) for item in item_twoEdge]
        
        for item in item_twoEdge:
            result.append(copy_twoEdge_OH.count(item))
        print "result:",result
        xresult = np.array(result)/float(sum(result))

        print "xresult,",xresult
        temp = 0
        for n in xresult:
            temp += n
            yresult.append(temp)

        # plt.step(np.arange(len(item_twoEdge)),yresult,label="GS "+str(GS))
        axs[0].plot(item_twoEdge,yresult,label=Al_Group[i])
        boxplot_result.append(OvOp_list[i])

    # axs[1].plot(np.arange(len(item_twoEdge)),yresult,'b--')
    # axs[1].set_xticks(np.arange(len(item_twoEdge)),xticks_str)
    # plt.xticks(item_twoEdge)
    axs[0].legend()
    axs[0].grid()
    axs[0].set_title("Different Algorithm CDF average of "+str(loopNum)+" Repeats")
    axs[0].set_ylabel("Percentage %")
    axs[0].set_xlabel("Overhead Sizes")
    # plt.xlim(0,1200,100)
    # axs[1].set_xscale('log')
    

    
    boxplot_label=["Algorithm "+ Al for Al in Al_Group]
    axs[1].boxplot(boxplot_result,labels=boxplot_label)
    axs[1].grid()
    axs[1].set_xlabel("Generation Size")
    for tick in axs[1].get_xticklabels():
    	tick.set_rotation(10)

    plt.show() 



def showDifferentGSData():
    runNum=200
    loopTimes=200
    GS_Group = [2,4,8,16,32,64,128]


    fig,axs=plt.subplots(2,1)

    boxplot_result = []
    for GS in GS_Group:
        fileName= "FixOnePacket_RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopTimes)
        with open("./twoEdgeFig/"+fileName+".json","r") as input:
            # twoEdge_OH.append(json.load(input))
            twoEdge_OH=json.load(input)
    
        result=[]
        xresult = []
        yresult = []
        item_twoEdge = list(set(twoEdge_OH))
        item_twoEdge.sort()

        copy_twoEdge_OH = list(twoEdge_OH)
        copy_twoEdge_OH.sort()

        # xticks_str = [str(item) for item in item_twoEdge]
        
        for item in item_twoEdge:
            result.append(copy_twoEdge_OH.count(item))
        print "result:",result
        xresult = np.array(result)/float(sum(result))

        print "xresult,",xresult
        temp = 0
        for n in xresult:
            temp += n
            yresult.append(temp)

        # plt.step(np.arange(len(item_twoEdge)),yresult,label="GS "+str(GS))
        axs[0].plot(item_twoEdge,yresult,label="GS "+str(GS))
        boxplot_result.append(twoEdge_OH)
        # axs[1].plot(np.arange(len(item_twoEdge)),yresult,'b--')
        # axs[1].set_xticks(np.arange(len(item_twoEdge)),xticks_str)
    # plt.xticks(item_twoEdge)
    axs[0].legend()
    axs[0].grid()
    axs[0].set_title("Different GS CDF average of "+str(loopTimes)+" Repeats")
    axs[0].set_ylabel("Percentage %")
    axs[0].set_xlabel("Overhead Sizes")
    # plt.xlim(0,1200,100)
    # axs[1].set_xscale('log')
    for tick in axs[0].get_xticklabels():
	    tick.set_rotation(360)

    boxplot_label=["GS "+str(GS) for GS in GS_Group]
    axs[1].boxplot(boxplot_result,labels=boxplot_label)
    axs[1].grid()
    axs[1].set_xlabel("Generation Size")

    plt.show()

if __name__=="__main__":  

    def test():
        GS = 4
        runTimes = 4
        tempDataList = [[random.randint(10,1400) for _ in range(GS)] for _ in range(runTimes)]
        for i in range(runTimes):
            # MacrosymbolSize().gotPerformance_print(item, MacrosymbolSize().algorithm_mix_v3)

            tempDataList[i].sort()
            copy_tempDataList = copy.copy(tempDataList[i])

            smallest = copy_tempDataList[0]
            biggest = copy_tempDataList[-1]

            # Quo = biggest // smallest
            # Rem = biggest % smallest

            # Overhead_temp = big
            print "biggest / smallest = ",str(biggest)+"/"+str(smallest)
            copy_tempDataList[0],copy_tempDataList[3],_ = MacrosymbolSize().Alg_Small_Dynamicv1_v2(smallest,biggest)
            # copy_tempDataList[0],copy_tempDataList[3],_ = MacrosymbolSize().Alg_DynamicV2(smallest,biggest) 
            Overhead = copy_tempDataList[0] - tempDataList[i][0]
            Overhead += copy_tempDataList[GS-1] - tempDataList[i][GS-1]

            Operation = 2*copy_tempDataList[0]
            for n in range(1,GS-1):
                smallest = copy_tempDataList[0]
                biggest = copy_tempDataList[n]
                _,copy_tempDataList[n],_ = MacrosymbolSize().Alg_Small_Fix(smallest,biggest)
                Overhead += copy_tempDataList[n] - tempDataList[i][n]
                Operation += 2*copy_tempDataList[n]

            Operation += copy_tempDataList[GS-1]

            print tempDataList[i]
            print copy_tempDataList
            print "Overhead: " + str(copy_tempDataList[0]) +" | Operation: "+str(copy_tempDataList[1]) \
                    +" | MacroSymbol Size: " +str(copy_tempDataList[2]) +" | Biggest Item: "+str(copy_tempDataList[3])+"\n"
    # test()

    def gotPrime(n):
        import math
        prime=list(range(1,n+1))
        flag=[True]*len(prime)

        def isPrime(n):
            if n <2: 
                return False
            for i in range(2,int(math.sqrt(n))+1):
                if n % i == 0:
            #       print "No"
                    return False
            #print "Yes"
            return True

        result = []
        for i in prime:
            if isPrime(i):
                result.append(i)
        print [1]+result
    # gotPrime(1400)

    def gcd_test():
        def gcd(x,y):
            while x%y != 0:
                t = x%y
                x,y = y,t
            return y

        runTimes = 5
        for _ in range(runTimes):
            x = 1163 #random.randint(10,1400)
            y = 1381 # random.randint(10,1400)
            for i in range(4):
                print "x | y = "+str(x)+"|"+str(y+i)+" = "+str(gcd(x,y+i))
                # print gotPrime(y+i)
                print "x | y = "+str(x+i)+"|"+str(y)+" = "+str(gcd(x+i,y))
                # dprint gotPrime(x+i)
    # gcd_test()



    # MacrosymbolSize().GS4GF8_FixOnePacket()
    # showDifferentGSData()
    GS2GF8_Algorithms()

    
    