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

from mpl_toolkits import mplot3d

# [1] random 2 packets
# [2] one packet is fix, another packet is random
# [3] one packet is random, another packet is random
randomSize_sel = 3 # [1,2,3]

# 1 nomal all the figure
# 2 just Dynamic V1 and V2
# 3 Small Fix vs Big Fix
figShow_sel = 2 # [1,2]

class Algorithms:

    def SmallFix(self,small,big):

        Rem = big % small
        if Rem >0:
            difference =small - Rem
        else:
            difference = 0
        Large = big + difference
        MacroS = small 
        Overhead = difference
        # Operation= 2*small + (big + (small - Rem))
        Operation= 2*MacroS + Large

        return Overhead, Operation, MacroS, Large

    def BigFix(self,small, big):
        
        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)
        
        for n in Quotient:
            if small <= n:
                Large = big 
                MacroS = n 
                Overhead = n - small
                break

        Operation= 2*MacroS + Large

        return Overhead, Operation, MacroS, Large

    def MixSB(self,small, big):
        Rem = big % small

        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)
        
        for n in Quotient:
            if small <= n:
                Large = big 
                MacroS = n 
                Overhead_Big = n - small
                break

        if small - Rem < Overhead_Big:
            MacroS = small
            Large = big + (small - Rem)
            Overhead = small - Rem
        else:
            Overhead = Overhead_Big

        Operation= 2*MacroS + Large

        return Overhead, Operation, MacroS, Large


    def DynamicV1(self, small, big):
        
        Quo = big / small
        Rem = big % small

        Large = big + (Quo-1)*Rem
        MacroS = small + Rem 

        Overhead = Quo * Rem
        Operation= 2*MacroS + Large
    
        return Overhead, Operation, MacroS, Large
        

    def DynamicV2(self, small, big):
        
            Quo = big / small
            Rem = big % small

            if Quo >= Rem:
                Large = big + (Quo -Rem)
                MacroS = small + 1
                Overhead = (Quo -Rem) + 1
                # Operation= 2*(small +1) + big + (Quo - Rem)
            elif Rem % Quo == 0:
                MacroS = small + (Rem // Quo )
                Large = big + (Rem // Quo )*Quo - Rem
                Overhead = (Rem // Quo )*(Quo + 1) - Rem
            else:
                MacroS = small + (Rem // Quo +1)
                Large = big + (Rem // Quo +1)*Quo - Rem
                Overhead = (Rem // Quo +1)*(Quo + 1) - Rem

            Operation= 2*MacroS + Large

            return Overhead, Operation, MacroS, Large
        

    def MixDyV1V2(self, small, big):
        if small <= big:
            Quo = big / small
            Rem = big % small

            if Quo >= Rem:
                Large = big + (Quo -Rem)
                MacroS = small + 1
                Overhead_DyV2 = (Quo -Rem) + 1
                # Operation= 2*(small +1) + big + (Quo - Rem)
            else:
                MacroS = small + (Rem // Quo +1)
                Large = big + (Rem // Quo +1)*Quo - Rem
                Overhead_DyV2 = (Rem // Quo +1)*(Quo + 1) - Rem
            
            if Quo * Rem < Overhead_DyV2:
                Large = big + (Quo-1)*Rem
                MacroS = small + Rem 
                Overhead = Quo * Rem
            else:
                Overhead = Overhead_DyV2
            
            Operation = 2*MacroS + Large

            return Overhead, Operation, MacroS, Large
        else:
            return 0, 0, 0, 0


    def MixSDyV1(self, small, big):
        Quo = big / small
        Rem = big % small

        if Quo*Rem > small - Rem:
            # excuate small fix Al
            Large = big + (small - Rem)
            MacroS = small 
            Overhead = small - Rem
            # Operation= 2*small + (big + (small - Rem))
        else:
            # excuate dynamic fix Al
            Large = big + (Quo-1)*Rem
            MacroS = small + Rem 
            Overhead = Quo * Rem
            # Operation= 2*(small + Rem) + (big + (Quo-1)*Rem)

        Operation= 2*MacroS + Large

        return Overhead, Operation, MacroS, Large

    def MixSDyV2(self, small, big):
        Quo = big / small
        Rem = big % small

        if Quo >= Rem:
            Large = big + (Quo -Rem)
            MacroS = small + 1
            Overhead = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            MacroS = small + (Rem // Quo +1)
            Large = big + (Rem // Quo +1)*Quo - Rem
            Overhead = (Rem // Quo +1)*(Quo + 1) - Rem

        if small - Rem < Overhead:
            Overhead = small - Rem
            MacroS = small
            Large = big + small - Rem

        Operation= 2*MacroS + Large


        return Overhead, Operation, MacroS, Large

    def MixBDyV1(self,small,big):
        Quo = big / small
        Rem = big % small

        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)
        
        for n in Quotient:
            if small <= n:
                Large = big
                MacroS_big = n 
                Overhead_Big = n - small
                break

        Overhead = Quo * Rem
        if Overhead_Big <= Overhead:
            Overhead = Overhead_Big                
            MacroS = MacroS_big
        else:
            Large = big + (Quo-1)*Rem
            MacroS = small + Rem 
        

        Operation= 2*MacroS + Large
    
        return Overhead, Operation, MacroS, Large



    def MixBDyV2(self,small, big):
        Quo = big / small
        Rem = big % small

        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)
        
        for n in Quotient:
            if small <= n:
                
                MacroS_big = n 
                Overhead_Big = n - small
                break

        if Quo >= Rem:
            Large = big + (Quo -Rem)
            MacroS = small + 1
            Overhead = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        elif Rem % Quo == 0:
            MacroS = small + (Rem // Quo )
            Large = big + (Rem // Quo )*Quo - Rem
            Overhead = (Rem // Quo )*(Quo + 1) - Rem
        else:
            MacroS = small + (Rem // Quo +1)
            Large = big + (Rem // Quo +1)*Quo - Rem
            Overhead = (Rem // Quo +1)*(Quo + 1) - Rem
            
        if Overhead_Big<Overhead:
            Overhead = Overhead_Big
            MacroS = MacroS_big
            Large = big 

        Operation= 2*MacroS + Large

        return Overhead, Operation, MacroS, Large


    def MixSBDyV1V2(self, small, big):
        Quo = big / small
        Rem = big % small
        # Small Fix
        Overhead_Small = small - Rem
        # Big Fix
        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)

        for n in Quotient:
            if small <= n:
                Overhead_Big = n - small
                # MacroS = n
                break

        # Dynamic V1
        Overhead_DyV1 = Rem * Quo

        # Dynamic V2
        if Quo >= Rem:
            Large = big + (Quo -Rem)
            MacroS = small + 1
            Overhead_DyV2 = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            MacroS = small + (Rem // Quo +1)
            Large = big + (Rem // Quo +1)*Quo - Rem
            Overhead_DyV2 = (Rem // Quo +1)*(Quo + 1) - Rem

        if Overhead_Small <= Overhead_Big and Overhead_Small <= Overhead_DyV1 and Overhead_Small <= Overhead_DyV2:
            Large = big + (small - Rem)
            MacroS = small 
            Overhead = Overhead_Small
        elif Overhead_Big <= Overhead_DyV1 and Overhead_Big <= Overhead_DyV2:
            Large = big
            MacroS = n
            Overhead = Overhead_Big
        elif Overhead_DyV1 <= Overhead_DyV2:
            Large = big + (Quo-1)*Rem
            MacroS = small + Rem 
            Overhead = Overhead_DyV1
        else:
            Overhead = Overhead_DyV2
        
        Operation= 2*MacroS + Large
        
        return Overhead, Operation, MacroS, Large

    def MixSBDyV2(self, small, big):
        Quo = big / small
        Rem = big % small

        Quotient = []
        for n in range(1,big+1):
            if big%n == 0:
                Quotient.append(n)

        for n in Quotient:
            if small <= n:
                Overhead_Big = n - small
                MacroS = n
                break

        
        if Quo >= Rem:
            Large = big + (Quo -Rem)
            MacroS = small + 1
            Overhead_DyV2 = (Quo -Rem) + 1
            # Operation= 2*(small +1) + big + (Quo - Rem)
        else:
            MacroS = small + (Rem // Quo +1)
            Large = big + (Rem // Quo +1)*Quo - Rem
            Overhead_DyV2 = (Rem // Quo +1)*(Quo + 1) - Rem


        if Overhead_Big <= Quo*Rem and Overhead_Big <= small - Rem and Overhead_Big <= Overhead_DyV2 :
            # execuate big fix Al
            Large = big
            MacroS = n

            Overhead = Overhead_Big
            # Operation= 2*n + big
            
        elif small - Rem <= Quo*Rem and small - Rem <=  Overhead_DyV2 :
            # excuate small fix Al
            Large = big + (small - Rem)
            MacroS = small 
            Overhead = small - Rem
            # Operation= 2*small + (big + (small - Rem))
        elif Quo*Rem <= Overhead_DyV2:
            # excuate dynamic fix Al
            Large = big + (Quo-1)*Rem
            MacroS = small + Rem 
            Overhead = Quo * Rem
        else:
            Overhead = Overhead_DyV2
            
        
        Operation= 2*MacroS + Large


        return Overhead, Operation, MacroS, Large

def show_twoEdges_OH_temp(GS,twoEdges_OH):
        result=[]
        xresult = []
        yresult = []
        item_twoEdge = list(set(twoEdges_OH))
        item_twoEdge.sort()

        copy_twoEdge_OH = list(twoEdges_OH)
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
        axs[0].set_ylabel("Number of times")
        axs[0].set_xlabel("Overhead Sizes")
        axs[0].grid(True)
        for tick in axs[0].get_xticklabels():
            tick.set_rotation(90)
            
        plt.subplots_adjust(top=0.3)

        axs[1].step(item_twoEdge,yresult)
        # axs[1].plot(np.arange(len(item_twoEdge)),yresult,'b--')
        # axs[1].set_xticks(np.arange(len(item_twoEdge)),xticks_str)
        axs[1].set_xticks(item_twoEdge)
        axs[1].set_title("Cumulative Distribution Function")
        axs[1].set_ylabel("Percentage")
        axs[1].set_xlabel("Overhead Sizes")
        axs[1].grid(True)
        # axs[1].set_xscale('log')
        for tick in axs[1].get_xticklabels():
            tick.set_rotation(90)

        strTitle = "Overhead of Small Fix V2 Algorithm, GS:" +str(GS)
        # if randomSize_sel == 1:
        #     strTitle = "Overhead of TwoEdgesFix Algorithm Packet Size[1 ~ 1500] GS:" +str(GS)
        #     strTitle = "Overhead of Small Fix V2 Algorithm, GS:" +str(GS)
        # else:
        #     strTitle = "Overhead of TwoEdgesFix Algorithm Packet Size[100 ~ 1400] GS:" +str(GS)
        fig.suptitle(strTitle)
        
        fig.tight_layout()
        plt.xticks(fontsize=10)
        plt.savefig("./pdfFigure/SmallFixV2CDF.pdf")
        plt.show()
   
def show_twoEdges_OH(GS,twoEdges_OH):
        result=[]
        xresult = []
        yresult = []
        item_twoEdge = list(set(twoEdges_OH))
        item_twoEdge.sort()

        copy_twoEdge_OH = list(twoEdges_OH)
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
        plt.figure(figsize=(8,6))
        plt.bar(item_twoEdge,result)
        # plt.set_xticks(np.arange(len(item_twoEdge)),xticks_str)
        plt.xticks(item_twoEdge)
        plt.title("Distribution Function")
        plt.ylabel("Number of times")
        plt.xlabel("Overhead Sizes")
        plt.grid(True)
        plt.xticks(rotation=90,fontsize=8)
        plt.savefig("./pdfFigure/SmallFixV2CDF_DF.pdf")
        plt.show()

        
        plt.figure(figsize=(8,6))
        plt.step(item_twoEdge,yresult)
        # plt.plot(np.arange(len(item_twoEdge)),yresult,'b--')
        # plt.set_xticks(np.arange(len(item_twoEdge)),xticks_str)
        plt.xticks(item_twoEdge)
        plt.title("Cumulative Distribution Function")
        plt.ylabel("Percentage")
        plt.xlabel("Overhead Sizes")
        plt.grid(True)
        # plt.set_xscale('log')
        plt.grid(True)
        plt.xticks(rotation=90,fontsize=8)
        

        # strTitle = "Overhead of Small Fix V2 Algorithm, GS:" +str(GS)
        # if randomSize_sel == 1:
        #     strTitle = "Overhead of TwoEdgesFix Algorithm Packet Size[1 ~ 1500] GS:" +str(GS)
        #     strTitle = "Overhead of Small Fix V2 Algorithm, GS:" +str(GS)
        # else:
        #     strTitle = "Overhead of TwoEdgesFix Algorithm Packet Size[100 ~ 1400] GS:" +str(GS)
        # plt.title(strTitle)
        
        plt.xticks(fontsize=9)
        plt.savefig("./pdfFigure/SmallFixV2CDF_CDF.pdf")
        plt.show()
  

def GS2GF8_Algorithms():
    runNum = 50
    GS = 2
    OvOp_list = []
    for i in range(runNum):
        loopNum = 3000
        
        Result_list=[[] for _ in range(40)]

        # seed = random.randint(1,2555)
        # rand = random.Random(seed)
        for i in range(loopNum):
            
            # [1] random 2 packets
            if randomSize_sel == 1:
                dataList = [random.randint(1,1500) for _ in range(GS)] 
            elif randomSize_sel == 2:
            # [2] one packet is fix, another packet is random
                # dataList = [10, random.randint(10,1400)] 
                dataList = [random.randint(10,1400) for _ in range(GS)] 
            else:
                dataList = [random.randint(10,400), random.randint(100,1400)] 

            dataList.sort()

            small = dataList[0]
            big = dataList[-1]

            
            # ================
            # Algorithm 1 small fix
            # ================
            #Quo =larger//smaller
            #Rem =larger%smaller

            Overhead, Operation, MacroS, Large = Algorithms().SmallFix(small,big)

            Result_list[0].append(Overhead)
            Result_list[1].append(Operation)
            Result_list[2].append(MacroS)
            Result_list[3].append(Large)

            # ================
            # Algorithm 2 big fix
            # ================

            Overhead, Operation, MacroS, Large = Algorithms().BigFix(small,big)

            Result_list[4].append(Overhead)
            Result_list[5].append(Operation)
            Result_list[6].append(MacroS)
            Result_list[7].append(Large)
            
            # ================
            # Algorithm 3 dynamic v1
            # ================

            Overhead, Operation, MacroS, Large = Algorithms().DynamicV1(small,big)
            
            Result_list[8].append(Overhead)
            Result_list[9].append(Operation)
            Result_list[10].append(MacroS)
            Result_list[11].append(Large)
            
            # ================
            # Algaric 3 dynamic v2
            # ================

            Overhead, Operation, MacroS, Large = Algorithms().DynamicV2(small,big)

            Result_list[12].append(Overhead)
            Result_list[13].append(Operation)
            Result_list[14].append(MacroS)
            Result_list[15].append(Large)

            # ================
            # Algaric 3 Mix dynamic v1v2
            # ================

            Overhead, Operation, MacroS, Large = Algorithms().MixDyV1V2(small,big)

            Result_list[16].append(Overhead)
            Result_list[17].append(Operation)
            Result_list[18].append(MacroS)
            Result_list[19].append(Large)

            # ================
            # Algorithm 4 mix big fix and dynamicV1  
            # ================
                
            Overhead, Operation, MacroS, Large = Algorithms().MixBDyV1(small,big)

            Result_list[20].append(Overhead)
            Result_list[21].append(Operation)
            Result_list[22].append(MacroS)
            Result_list[23].append(Large)
            
            
            # ================
            # Algorithm 5 mix big fix and dynamicV2  
            # ================
                
            Overhead, Operation, MacroS, Large = Algorithms().MixBDyV2(small,big)

            Result_list[24].append(Overhead)
            Result_list[25].append(Operation)
            Result_list[26].append(MacroS)
            Result_list[27].append(Large)

            # ================
            # Algorithm 5 mix dynamic v1v2,small,big fix
            # ================
            Overhead, Operation, MacroS, Large = Algorithms().MixSBDyV1V2(small,big)
            
            Result_list[28].append(Overhead)
            Result_list[29].append(Operation)
            Result_list[20].append(MacroS)
            Result_list[31].append(Large)

            # ================
            # Algorithm 6 mix dynamic v1v2,small,big fix
            # ================
            Overhead, Operation, MacroS, Large = Algorithms().MixSBDyV1V2(small,big)
            
            Result_list[32].append(Overhead)
            Result_list[33].append(Operation)
            Result_list[34].append(MacroS)
            Result_list[35].append(Large)

            # ================
            # Algorithm 6 mix dynamic v1v2,small,big fix
            # ================
            Overhead, Operation, MacroS, Large = Algorithms().MixSB(small,big)
            
            Result_list[36].append(Overhead)
            Result_list[37].append(Operation)
            Result_list[38].append(MacroS)
            Result_list[39].append(Large)

        figShow_sel = 10

        mean_list=[np.mean(item) for item in Result_list]
        std_list = [np.std(item) for item in Result_list]

        if figShow_sel == 1:       
            OvOp_list.append([mean_list[32],mean_list[24],mean_list[20],mean_list[16],mean_list[12],mean_list[8],mean_list[4],mean_list[0],\
                                mean_list[33],mean_list[25],mean_list[21],mean_list[17],mean_list[13],mean_list[9],mean_list[5],mean_list[1]])
        elif figShow_sel == 2:
            OvOp_list.append([mean_list[16],mean_list[12],mean_list[8],
                                mean_list[17],mean_list[13],mean_list[9]])
        elif figShow_sel == 3:
            OvOp_list.append([mean_list[12],mean_list[8],
                                mean_list[13],mean_list[9]])   
        elif figShow_sel == 4:
            OvOp_list.append([mean_list[16],mean_list[12],
                                mean_list[17],mean_list[13]]) 

        elif figShow_sel == 7:
            OvOp_list.append([mean_list[36],mean_list[0],mean_list[4],
                                mean_list[37],mean_list[1],mean_list[5]])
        elif figShow_sel == 8:
            OvOp_list.append([mean_list[0],mean_list[4],
                                mean_list[1],mean_list[5]])                                
        elif figShow_sel == 9:
            OvOp_list.append([mean_list[32],mean_list[24],
                                mean_list[33],mean_list[25]])
        elif figShow_sel == 10:
            OvOp_list.append([mean_list[24],mean_list[20],mean_list[12],mean_list[8],
                                mean_list[25],mean_list[21],mean_list[13],mean_list[9]])
        
        else:
            pass
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=np.array(OvOp_list).T
       # marker_list=['x','-','.','_']
        
    #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
    #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    if figShow_sel == 1:       
        keysParament_list = ["OH SBDyV1V2","OH MixBDyV2","OH MixBDyV1","OH MixDyV1V2","OH DynamicV2","OH DynamicV1","OH BigFix","OH SmallFix",\
                             "OP SBDyV1V2","OP MixBDyV2","OP MixBDyV1","OP MixDyV1V2","OP DynamicV2","OP DynamicV1","OP BigFix","OP SmallFix"]
    elif figShow_sel == 2:
        nameOffig = "MixDyV1V2_compare"
        keysParament_list = ["OH MixDyV1V2","OH DynamicV2","OH DynamicV1",\
                             "OP MixDyV1V2","OP DynamicV2","OP DynamicV1"]
    elif figShow_sel == 3:
        nameOffig = "DyV1DyV2_compare"
        keysParament_list = ["OH DynamicV2","OH DynamicV1",\
                             "OP DynamicV2","OP DynamicV1"]

    elif figShow_sel == 4:
        nameOffig = "MixvsDyV2_compare"
        keysParament_list = ["OH MixDyV1V2","OH DynamicV2",\
                             "OP MixDyV1V2","OP DynamicV2"]

    elif figShow_sel == 7:
        nameOffig = "MixSFBF_compare"
        keysParament_list = ["OH MixSB","OH SmallFix","OH BigFix",\
                             "OP MixSB","OP SmallFix","OP BigFix"]

    elif figShow_sel == 8:
        keysParament_list = ["OH SmallFix","OH BigFix",\
                             "OP SmallFix","OP BigFix"]                         
    elif figShow_sel == 9:
        keysParament_list = ["OH MixSBDy2","OH MixSDy2",\
                             "OP MixSBDy2","OP MixSDy2"]
    elif figShow_sel == 10:
        nameOffig = "MixDyV1V2_BDyv1BDyv2"
        keysParament_list = ["OH MixBDy2","OH MixBDy1","OH DynamicV2","OH DynamicV1",\
                             "OP MixBDy2","OP MixBDy1","OP DynamicV2","OP DynamicV1"]
                             
    else:
        pass


    strTitle_head = "GS=2,GF($2^8$), " 
    if randomSize_sel == 1:
        strTitle_tail =  ", Packets Size [1, 1500], " + str(loopNum)+" examples/Test"
    elif randomSize_sel == 2:
        strTitle_tail =  ", Packets Size [10,1400], " + str(loopNum)+" examples/Test"
    else:
        strTitle_tail =  ", One Random is [10, 400], Another is random [100,1400], " + str(loopNum)+" examples/Test"


    axsMarker=["+","x"]
    if figShow_sel == 1:
        t = np.arange(runNum)    
        # fix,axs = plt.subplots(2,1)

        
        # for i in range(0,len(keysParament_list)/2):
        #     if i < 2: 
        #         axs[0].plot(t,OvOp_list[i],label=keysParament_list[i],marker=axsMarker[i])
        #     else:
        #         axs[0].plot(t,OvOp_list[i],label=keysParament_list[i])
        
        # for i in range(len(keysParament_list)/2,len(keysParament_list)):
        #     if i <len(keysParament_list)/2 +2:
        #         axs[1].plot(t,OvOp_list[i],label=keysParament_list[i],marker=axsMarker[i%(len(keysParament_list)/2)])
        #     else:
        #         axs[1].plot(t,OvOp_list[i],label=keysParament_list[i])
        # axs[1].set_yscale('log')
        
        # plt.title(strTitle)
        strTitle_item = ["Operation", "Overhead"]
        yTitlelabel = ["Operation Number", "Added Overhead / Byte"]
        # for i in range(2):
        #     axs[i].grid(True)
        #     axs[i].legend()
        #     axs[i].set_title(strTitle_head + strTitle_item [i]+ strTitle_tail )
        #     axs[i].set_xlabel("Test Nr.")
        #     axs[i].set_ylabel(yTitlelabel[i])
        
        # plt.subplots_adjust(wspace = 0, hspace = 0.3)
        plt.figure(figsize=(8,4))
        for i in range(0,len(keysParament_list)/2):
            if i < 2: 
                plt.plot(t,OvOp_list[i],label=keysParament_list[i],marker=axsMarker[i])
            else:
                plt.plot(t,OvOp_list[i],label=keysParament_list[i])
       
        

        plt.grid(True)
        plt.legend()
        plt.title(strTitle_head + "Operation" + strTitle_tail )
        plt.xlabel("Test Nr.")
        plt.ylabel("Added Overhead / Byte")
        
        # plt.subplots_adjust(wspace = 0, hspace = 0.3)
        plt.savefig("./pdfFigure/Mixall.pdf")
        plt.show() 
    else :
        plt.figure(figsize=(6, 4))
        t = np.arange(runNum)  
        for i in range(0,len(keysParament_list)/2):
            if i <2:
                plt.plot(t,OvOp_list[i],label=keysParament_list[i],marker=axsMarker[i])
            else:
                plt.plot(t,OvOp_list[i],label=keysParament_list[i])
            
            print "mean value of "+ keysParament_list[i]+str(np.mean(OvOp_list[i]))
        
        # strTitle_head = "GS = 2, GF($2^8$), "
        # # strTitle_tail =  ", Random Size [1, 1500], " + str(loopNum)+" examples of each Test"
        plt.grid(True)
        plt.legend()
        plt.title(strTitle_head + "Overhead" + strTitle_tail )
        plt.xlabel("Test Nr.")
        plt.ylabel("Added Overhead / Byte")
        # plt.yscale('log')
        # plt.savefig("1.pdf")
        plt.savefig("./pdfFigure/"+nameOffig+".pdf")
        plt.show()


def GS4GF8_Algorithms():
    runNum = 250 #150
    GS= 32

    OvOp_list = []
    twoEdges_OH = []
    smallFixV2  = []
    dynamicV3 = []

    fix_number = 93
    seed = random.randint(1,2555)
    rand = random.Random(seed)
    for _ in range(runNum):


        loopNum = 3000 # 90
        
        Result_list=[[] for _ in range(24)]

        for i in range(loopNum):
            # [1] random 2 packets
            if randomSize_sel == 1:
                DataList = [rand.randint(1,1500) for _ in range(GS)] 
            elif randomSize_sel == 2:
            # [2] one packet is fix, another packet is random
                DataList = [fix_number]+[rand.randint(10,1400) for _ in range(GS-1)]
            else:
                DataList = [rand.randint(10,1400) for _ in range(GS)] 

            DataList.sort()
            
            # =====================
            # Algorithm 0 small fix V2
            # ======================
            
            small = DataList[0]
            MacroSs = DataList[0]
            Overhead = 0
            Operation = 2*small
            for i in range(1,GS):
                Rem = DataList[i] % small
                
                Overhead += small - Rem
                # Operation= 2*small + (big + (small - Rem))
                if i < GS-1:
                    Operation += 2*DataList[i] 
                else: 
                    LargestItem = DataList[i] + (small - Rem)
                    Operation += DataList[i] 

            
            Result_list[0].append(Overhead)
            Result_list[1].append(Operation)
            Result_list[2].append(MacroSs)
            Result_list[3].append(LargestItem)

            # ================
            # Algorithm 1 adjust all
            # ================
            # copy_tempDataList = copy.copy(DataList)

            DataList.sort()
            copy_DataList = list(DataList)

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

            Result_list[4].append(Overhead)
            Result_list[5].append(Operation)
            Result_list[6].append(MacroSs)
            Result_list[7].append(LargestItem)
            

            # ================
            # Algorithm 2 fix two edges
            # ================
            copy_DataList = copy.copy(DataList)

            smallest = copy_DataList[0]
            biggest = copy_DataList[-1]

            # Quo = biggest // smallest
            # Rem = biggest % smallest

            # Overhead_temp = big
            
            _,_,copy_DataList[0],copy_DataList[-1] = Algorithms().MixSDyV2(smallest,biggest)

            Overhead = copy_DataList[0] - DataList[0]
            Overhead += copy_DataList[GS-1] - DataList[GS-1]

            Operation = 2*copy_DataList[0]
            for n in range(1,GS-1):
                smallest = copy_DataList[0]
                biggest = copy_DataList[n]
                _,_,_,copy_DataList[n] = Algorithms().SmallFix(smallest,biggest)
                Overhead += copy_DataList[n] - DataList[n]
                Operation += 2*copy_DataList[n]

            Operation += copy_DataList[GS-1]

            Result_list[8].append(Overhead)
            Result_list[9].append(Operation)
            Result_list[10].append(MacroSs)
            Result_list[11].append(LargestItem)


        mean_list=[np.mean(item) for item in Result_list]
        std_list = [np.std(item) for item in Result_list]
        
        # OvOp_list.append([mean_list[0],mean_list[1],mean_list[4],mean_list[5]])
        OvOp_list.append([mean_list[9],mean_list[5],mean_list[1],\
                        mean_list[8],mean_list[4],mean_list[0]])

        smallFixV2.append(mean_list[0])
        dynamicV3.append(mean_list[4])
        twoEdges_OH.append(mean_list[8])
        
       

        
    print "OvOp_list,",np.array(OvOp_list).shape
    OvOp_list=np.array(OvOp_list).T
    # marker_list=['x','-','.','_']
        
    #label_list=["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"] \
    #            + ["Overhead","Operation","MacroSs $\mu$","Bigest Packet Size"]
    
    # keysParament_list1 = ["Operation twoEdge Fix","Operation DynamicV3","Operation DynamicV2","Operation SmallDyV1V2","Operation SmallDyV1","Operation SmallFix"]
    # keysParament_list2 = ["Overhead twoEdge Fix","Overhead DynamicV3","Overhead DynamicV2","Overhead SmallDyV1V2","Overhead SmallDyV1","Overhead SmallFix"]
    
    keysParament_list = ["OP TwoEdgesFix","OP DynamicV3","OP SmallFixV2",\
                        "OH TwoEdgesFix","OH DynamicV3","OH SmallFixV2"]

    if figShow_sel == 1:
        t = np.arange(runNum)
        fix, axs = plt.subplots(2,1)

        for i in range(0,len(keysParament_list)/2):
            axs[0].plot(t,OvOp_list[i],label=keysParament_list[i])
        
        for i in range(len(keysParament_list)/2, len(keysParament_list)):
            axs[1].plot(t,OvOp_list[i],label=keysParament_list[i])
        

        # plt.plot(t,[np.mean(mean_list[0])]*len(t),label="Al.1 Mean"+ str(format(np.mean(mean_list[0]),'.2f')))
        # plt.plot(t,[np.mean(mean_list[3])]*len(t),label="LargPacketSize Mean"+str(format(np.mean(mean_list[3]),'.2f')))
        strTitle_head = "GS = "+str(GS)+", GF($2^8$), " 
        if randomSize_sel == 1:
            strTitle_tail =  ", Random Size [1, 1500], " + str(loopNum)+" examples of each Test"
        elif randomSize_sel == 2:
            strTitle_tail =  ", One Packet is "+str(fix_number)+ "Byte, Anothers are random [10,1400], " + str(loopNum)+" examples of each Test"
        else:
            strTitle_tail =  ", Random Size [10, 1400] " + str(loopNum)+" examples of each Test"

    
        strTitle_item = ["Operation", "Overhead"]
        
        yTitlelabel = ["Operation Number", "Added Overhead / Byte"]
        for i in range(2):
            axs[i].grid(True)
            axs[i].legend()
            axs[i].set_title(strTitle_head + strTitle_item [i]+ strTitle_tail )
            axs[i].set_xlabel("Test Nr.")
            axs[i].set_ylabel(yTitlelabel[i])
            
            # plt.savefig('./MacroFig'+strTitle+'.png')
        plt.subplots_adjust(wspace=0,hspace=0.3)
        plt.show() 
    else:
        
        fileName= "RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopNum)

        # with open("./twoEdgeFig/"+fileName+".json","w") as output:
        #     json.dump(twoEdges_OH,output)
        # show_twoEdges_OH(GS,np.round(twoEdges_OH))

        # with open("./dynamicV3/"+fileName+".json","w") as output:
        #     json.dump(dynamicV3,output)
        # show_twoEdges_OH(GS,np.round(dynamicV3))

        with open("./smallFixV2/"+fileName+".json","w") as output:
            json.dump(smallFixV2,output)
        show_twoEdges_OH(GS,np.round(smallFixV2))

def showDifferentData():
    runNum=250
    loopNum=3000
    GS_Group = [2,4,8,16,32,64,128]

    # plt.figure(figsize=(12, 6))
    fig,axs=plt.subplots(1,2)
    

    boxplot_result = []
    for GS in GS_Group:
        fileName= "RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopNum)

        # with open("./twoEdgeFig/"+fileName+".json","r") as input:           
        #     twoEdge_OH=json.load(input)

        # with open("./dynamicV3/"+fileName+".json","r") as input:
        #     twoEdge_OH=json.load(input)

        with open("./smallFixV2/"+fileName+".json","r") as input:
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
    # axs[0].set_title("CDF of TwoEdgesFix, average of "+str(loopNum)+" examples")
    # axs[0].set_title("CDF of DynamicV3, average of "+str(loopNum)+" examples")
    axs[0].set_title("CDF of SmallFixV2, average of "+str(loopNum)+" examples")
    axs[0].set_ylabel("Percentage %")
    axs[0].set_xlabel("Overhead Sizes")
    # plt.xlim(0,1200,100)
    # axs[1].set_xscale('log')
    for tick in axs[0].get_xticklabels():
	    tick.set_rotation(360)
    plt.subplots_adjust(wspace =0.3, hspace =0)

    boxplot_label=["GS "+str(GS) for GS in GS_Group]
    axs[1].boxplot(boxplot_result,labels=boxplot_label)
    axs[1].grid()
    axs[1].set_xlabel("Generation Size")
    axs[1].set_ylabel("Added Overhead Sizes")
    axs[1].legend()
    
    # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
    plt.savefig("./pdfFigure/"+"CDFofDynamicV3"+".pdf")
    # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
    plt.show()


class GS4GF8_pdf_figure():

    def CompareAll(self):
        randomTimes = 3000# [60]
        loop = 500
        nubAlgorithm=3
        GS = 4
        OvOp_list = [[] for _ in range(nubAlgorithm)]
        for _ in range(loop):
            
            # for i in range(len(randomTimes)):
            # OvOp_list.append([])
            OHArray=[[] for _ in range(nubAlgorithm)] # for small big mix
            for _ in range(randomTimes):
                seed = random.randint(1,2555)
                rand = random.Random(seed)
                DataList = [rand.randint(10,1400) for _ in range(GS)]
                DataList.sort()

                # =====================
                # Algorithm 0 small fix V2
                # ======================
            
                small = DataList[0]
                Overhead = 0
                
                for i in range(1,GS):
                    Rem = DataList[i] % small
                    Overhead += small - Rem

                OHArray[0].append(Overhead)
           

                # ================
                # Algorithm 1 adjust all
                # ================
                # copy_tempDataList = copy.copy(DataList)

                # DataList.sort()
                copy_DataList = list(DataList)

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
                
                for n in range(GS):
                    Overhead += Q[n]*add_macross - R[n]
                    

                OHArray[1].append(Overhead)
            

                # ================
                # Algorithm 2 fix two edges
                # ================
                copy_DataList = copy.copy(DataList)

                smallest = copy_DataList[0]
                biggest = copy_DataList[-1]

                # Quo = biggest // smallest
                # Rem = biggest % smallest

                # Overhead_temp = big
                
                _,_,copy_DataList[0],copy_DataList[-1] = Algorithms().MixSDyV2(smallest,biggest)

                Overhead = copy_DataList[0] - DataList[0]
                Overhead += copy_DataList[GS-1] - DataList[GS-1]
                
                for n in range(1,GS-1):
                    smallest = copy_DataList[0]
                    biggest = copy_DataList[n]
                    _,_,_,copy_DataList[n] = Algorithms().SmallFix(smallest,biggest)
                    Overhead += copy_DataList[n] - DataList[n]
                OHArray[2].append(Overhead)
                
                
                
        for i in range(nubAlgorithm):
            OvOp_list[i].append(np.mean(OHArray[i]))

        print OHArray,":",len(OHArray)
            
        # OvOp_list.append(OHArray)
        plt.figure(figsize=(10, 8))
        #fig, axs = plt.subplots(figsize=(6, 4))
        keysParament_list=['Small Fix V2','Dynamic V3','Two Edges Fix']
        # for i in range(len(OHArray)):
        #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
        plt.boxplot(OvOp_list,labels=keysParament_list)
        plt.grid(True)
        plt.xlabel("Different Algorithms",fontsize=18)
        plt.ylabel("Added Overhead Sizes",fontsize=18)
        plt.xticks(rotation=20)
        # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
        plt.savefig("./pdfFigure/"+"CompGS4AllAl_r"+str(randomTimes)+"l"+str(loop)+".pdf")
        # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
        plt.show()


class GS2GF8_pdf_figure():

    def SmallFix(self,fig_sel):
        if fig_sel == 0:

            def f(x, y):
                Overhead, _, MacroS, Large = Algorithms().SmallFix(y,x)
                return Overhead

            x = np.arange(10, 80)
            y = np.arange(10, 80)

            X, Y = np.meshgrid(x, y)
            Z = f(X, Y)
                    
            

            fig = plt.figure(figsize=(8, 4))
            ax = plt.axes(projection='3d')
            # ax.contour3D(X, Y, Z, 50, cmap='binary')
            
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')

            ax.set_xlabel('Small packet size')
            # ax.xticks(fontsize=12)
            ax.set_ylabel('Big packet size')
            ax.set_zlabel('Overhead ')
            
            strTitle_head = "Small Fix 3D Overhead, GS = 2, GF($2^8$), "
            strTitle_tail =  ""
            ax.set_title(strTitle_head + strTitle_tail,fontsize=12)
        
            # ax.view_init(15, 10)
            # plt.savefig("./pdfFigure/"+"DyV1_1510"+".pdf")
            ax.view_init(80, 180)
            plt.savefig("./pdfFigure/"+"SmallFix_80180"+".pdf")
            plt.show()

        elif fig_sel == 1:
            small_1 = 6
            small_2 = 10
            small_3 = 17
            
            t_1 = np.arange(small_1,50)
            t_2 = np.arange(small_2,50)
            t_3 = np.arange(small_3,50)
            
            
            OHArray_1 = []
            OHArray_2 = [ None for _ in range(4)]
            OHArray_2_boxplot = []
            OHArray_3 = [ None for _ in range(11)]
            OHArray_3_boxplot = []

            for big in t_1:
                Overhead_1, _, _, _ = Algorithms().SmallFix(small_1, big)
                OHArray_1.append(Overhead_1)

            for big in t_2:
                Overhead_2, _, _, _ = Algorithms().SmallFix(small_2, big)
                OHArray_2.append(Overhead_2)
                OHArray_2_boxplot.append(Overhead_2)

            for big in t_3:
                Overhead_3, _, _, _ = Algorithms().SmallFix(small_3, big)
                OHArray_3.append(Overhead_3)
                OHArray_3_boxplot.append(Overhead_3)

            str_label = ["small="+str(small_1),"small="+str(small_2),"small="+str(small_3)]
            # t_real = np.linspace(10,1400,1)  
            strName = ['SmallFix']
            
            plt.figure(figsize=(10, 5.5))

            plt.plot(OHArray_1,label="small="+str(small_1),marker='x')
            plt.plot(OHArray_2,label="samll="+str(small_2),marker='+')
            plt.plot(OHArray_3,label="samll="+str(small_3),marker='+')
                
            
            strTitle_head = "SmallFix Overhead, GS = 2, GF($2^8$), "
            strTitle_tail =  ""
            plt.grid(True)
            plt.legend()
            plt.title(strTitle_head + strTitle_tail,fontsize=18)
            plt.xlabel("Big packet length",fontsize=18)
            plt.ylabel("Overhead / Bytes",fontsize=18)
            plt.xticks(range(len(t_1)),t_1,rotation=90,fontsize=12)
            
            # plt.yscale('log')
            
            
            plt.savefig("./pdfFigure/"+strName[0]+".pdf")
            
            plt.show()
        else:
            str_label = ["small="+str(small_1),"small="+str(small_2),"small="+str(small_3)]
            # t_real = np.linspace(10,1400,1)  
            strName = ['SmallFix']

            top_limit = 500
            boxplot_result = []
            str_label = []
            for small in [27,43,59,75,91,107,123,139]:
            # for small in [6,11,16]:
                t = np.arange(small,top_limit)                                    
                OHArray = []
                for big in t:
                    Overhead, _, _, _ = Algorithms().SmallFix(small, big)
                    OHArray.append(Overhead)


                str_label.append("small="+str(small))
                # t_real = np.linspace(10,1400,1)  
                
                boxplot_result.append(OHArray)
            
            plt.figure(figsize=(10, 7.5))
            strTitle_head = "SmallFix Overhead, GS = 2, GF($2^8$), "
            
            strTitle_tail =  " top limitation is 500 bytes"
            plt.grid(True)
            plt.legend()
            plt.title(strTitle_head + strTitle_tail,fontsize=18)
            plt.xlabel("Big packet length",fontsize=18)
            plt.ylabel("Overhead / Bytes",fontsize=18)
            plt.xticks(rotation=10,fontsize=16)
            plt.boxplot(boxplot_result,labels=str_label)

            strName = ['SmallFix']
            # plt.boxplot(boxplot_result)
            plt.savefig("./pdfFigure/"+strName[0]+"_boxplot.pdf")
            plt.show()

    def BigFix(self):


        big_1 = 1400
        big_2 = 37
        small = 10

        t_1 = np.arange(10,big_1)
        t_2 = np.arange(10,big_2)
        
        OHArray_1 = []
        OHArray_2 = []

        for small in t_1:
            Overhead_1, _, _, _ = Algorithms().BigFix(small, big_1)
            OHArray_1.append(Overhead_1)

        for small in t_2:
            Overhead_2, _, _, _ = Algorithms().BigFix(small, big_2)
            OHArray_2.append(Overhead_2)

        # t_real = np.linspace(10,1400,1)  

        plt.figure(figsize=(12, 6))

        plt.plot(OHArray_1,label="big="+str(big_1),marker='x')
        plt.plot(OHArray_2,label="big="+str(big_2),marker='+')
            
        
        strTitle_head = "BigFix Overhead, GS = 2, GF($2^8$), "
        strTitle_tail =  ""
        
        plt.grid(True)
        plt.legend()
        plt.title(strTitle_head + strTitle_tail,fontsize=12)
        plt.xlabel("Small packet length",fontsize=12)
        plt.ylabel("Overhead / Bytes",fontsize=12)
        plt.xticks(range(len(t_1)),t_1,rotation=90,fontsize=9)

        # plt.yscale('log')
        strName = ['SmallFix','BigFix']
        plt.savefig("./pdfFigure/"+strName[1]+".pdf")
        plt.show()
        

    def BigFix_advance(self,fig_sel):
    
        if fig_sel == 1:
            big_1 = 27
            big_2 = 44
            big_3 = 60
            small = 10

            Quotient_1 = []
            for n in range(1,big_1+1):
                if big_1%n == 0:
                    Quotient_1.append(n)

            Quotient_2 = []
            for n in range(1,big_2+1):
                if big_2%n == 0:
                    Quotient_2.append(n)
            
            Quotient_3 = []
            for n in range(1,big_3+1):
                if big_3%n == 0:
                    Quotient_3.append(n)


            t_1 = np.arange(10,big_1)
            t_2 = np.arange(10,big_2)
            t_3 = np.arange(10,big_3)

            # t_1 = np.linspace(10,big_1,big_1/40)
            # t_2 = np.linspace(10,big_2,big_2/40)
            
            OHArray_1 = []
            OHArray_2 = []
            OHArray_3 = []

            Overhead_1 = None
            for small in t_1:
                
                for n in Quotient_1:
                    if small <= n:
                        Overhead_1 = n - small
                        break

                OHArray_1.append(Overhead_1)

            Overhead_2 = None
            for small in t_2:
                
                for n in Quotient_2:
                    if small <= n:
                        Overhead_2 = n - small
                        break

                OHArray_2.append(Overhead_2)
            
            Overhead_3 = None
            for small in t_3:
                
                for n in Quotient_3:
                    if small <= n:
                        Overhead_3 = n - small
                        break

                OHArray_3.append(Overhead_3)

            # t_real = np.linspace(10,1400,1)  
            
            plt.figure(figsize=(10, 5.5))

            plt.plot(OHArray_1,label="big="+str(big_1),marker='+')
            plt.plot(OHArray_2,label="big="+str(big_2),marker='>')
            plt.plot(OHArray_3,label="big="+str(big_3))
            
            
            strTitle_head = "BigFix Overhead, GS = 2, GF($2^8$), "
            strTitle_tail =  ""

            plt.grid(True)
            plt.legend()
            plt.title(strTitle_head + strTitle_tail,fontsize=18)
            plt.xlabel("Small packet length",fontsize=18)
            plt.ylabel("Overhead / Bytes",fontsize=18)
            plt.xticks(range(len(t_3)),t_3,rotation=90,fontsize=9)

            # plt.yscale('log')
            strName = ['SmallFix','BigFix']
            plt.savefig("./pdfFigure/"+strName[1]+".pdf")
            plt.show()
        else:

            
            boxplot_result = []
            str_label = []
            
            bottom_limit = 10

            for big in [27,43,59,75,91,107,123,139]:
                
            # for small in [6,11,16]:
                Quotient = []
                for n in range(1,big+1):
                    if big%n == 0:
                        Quotient.append(n)

                t = np.arange(bottom_limit,big)
                                            
                OHArray = []
                # Overhead = None
                for small in t:
                    
                    for n in Quotient:
                        if small <= n:
                            Overhead = n - small
                            break

                    OHArray.append(Overhead)


                str_label.append("big="+str(big))
                # t_real = np.linspace(10,1400,1)  
                
                boxplot_result.append(OHArray)
            
            plt.figure(figsize=(10, 7.5))
            strTitle_head = "BigFix Overhead, GS = 2, GF($2^8$), "
            
            strTitle_tail =  " bottom limitation is 10 bytes"
            plt.grid()
            plt.legend()
            plt.boxplot(boxplot_result,labels=str_label)

            plt.title(strTitle_head + strTitle_tail,fontsize=18)
            plt.xlabel("Small packet length",fontsize=18)
            plt.ylabel("Overhead / Bytes",fontsize=18)
            plt.xticks(rotation=10,fontsize=16)
            
            strName = ['BigFix']
            # plt.boxplot(boxplot_result)
            plt.savefig("./pdfFigure/"+strName[0]+"_boxplot.pdf")
            plt.show()

    def MixSmallBigFix(self,fig_sel):
        if fig_sel == 1:
            pass
        else:
            # str_label = ["small="+str(small_1),"small="+str(small_2),"small="+str(small_3)]
            # t_real = np.linspace(10,1400,1)  
            strName = ['SmallFix']

            top_limit = 500
            boxplot_result = []
            str_label = []
            for small in [27,43,59,75,91,107,123,139]:
            # for small in [6,11,16]:
                t = np.arange(small,top_limit)                                    
                OHArray = []
                for big in t:
                    Overhead_SmallFix, _, _, _ = Algorithms().SmallFix(small, big)
                    Overhead_BigFix, _, _, _ = Algorithms().BigFix(small, big)
                    if Overhead_SmallFix <= Overhead_BigFix:
                        OHArray.append(Overhead_SmallFix)
                    else:
                        OHArray.append(Overhead_BigFix)


                str_label.append("small="+str(small))
                # t_real = np.linspace(10,1400,1)  
                
                boxplot_result.append(OHArray)
            
            plt.figure(figsize=(10, 7.5))
            strTitle_head = "Mix SFix BFix Overhead, GS = 2, GF($2^8$), "
            
            strTitle_tail =  " limitation bottom 10 bytes, top is 500 bytes"
            plt.grid(True)
            plt.legend()
            plt.title(strTitle_head + strTitle_tail,fontsize=18)
            plt.xlabel("Big packet length",fontsize=18)
            plt.ylabel("Overhead / Bytes",fontsize=18)
            plt.xticks(rotation=10,fontsize=16)
            plt.boxplot(boxplot_result,labels=str_label)

            strName = ['SmallFix']
            # plt.boxplot(boxplot_result)
            plt.savefig("./pdfFigure/"+strName[0]+"_boxplot.pdf")
            plt.show()


    def DyV1(self):  
        from mpl_toolkits import mplot3d
        

        def f(x, y):
            Overhead, _, MacroS, Large = Algorithms().DynamicV1(x,y)
            return Overhead

        x = np.arange(10, 80)
        y = np.arange(10, 80)

        X, Y = np.meshgrid(x, y)
        Z = f(X, Y)
                
        

        fig = plt.figure(figsize=(8, 4))
        ax = plt.axes(projection='3d')
        # ax.contour3D(X, Y, Z, 50, cmap='binary')
        
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')

        ax.set_xlabel('Small packet size')
        # ax.xticks(fontsize=12)
        ax.set_ylabel('Big packet size')
        ax.set_zlabel('Overhead ')
        
        strTitle_head = "DyV1 3D Overhead, GS = 2, GF($2^8$), "
        strTitle_tail =  ""
        ax.set_title(strTitle_head + strTitle_tail,fontsize=12)
       
        # ax.view_init(75, 270)
        # plt.savefig("./pdfFigure/"+"DyV1_75270"+".pdf")
        ax.view_init(15, 80)
        plt.savefig("./pdfFigure/"+"DyV1_1580"+".pdf")
        plt.show()

        
    

        # plt.figure(figsize=(12, 6))

        # plt.plot(OHArray_1, label="big="+str(big_1),marker='x')
        # plt.plot(LAArray_1, label="Larg Number",marker='x')
        # plt.plot(MacroSArr, label="Macro Symbol")
            
        
        
        # plt.grid(True)
        # plt.legend()
        
        # plt.xlabel("Small packet length",fontsize=12)
        # plt.ylabel("Overhead / Bytes",fontsize=12)
        # plt.xticks(range(len(t_1)),t_1,rotation=90,fontsize=9)


        # # plt.yscale('log')
        # strName = ['SmallFix','BigFix','DyV1_SmallFix']
        # plt.savefig("./pdfFigure/"+strName[2]+".pdf")
        # plt.show()   
        
    def DyV1_BigFix(self):  
        small = 10
        big_1 = 65
        big_2 = 37

        OHArray_1 = []
        LAArray_1 = []
        MacroSArr = []
        for small in range(10,big_1):  
            Overhead, _, MacroS, Large = Algorithms().DynamicV1(small,big_1)

            OHArray_1.append(Overhead)
            LAArray_1.append(Large)
            MacroSArr.append(MacroS)
        
       
        t_1 = np.arange(10,big_1)

        plt.figure(figsize=(12, 6))

        plt.plot(OHArray_1, label="big="+str(big_1),marker='x')
        plt.plot(LAArray_1, label="Larg Number",marker='x')
        plt.plot(MacroSArr, label="Macro Symbol")
            
        
        strTitle_head = "DyV1_BigFix Overhead, GS = 2, GF($2^8$), "
        strTitle_tail =  ""
        plt.grid(True)
        plt.legend()
        plt.title(strTitle_head + strTitle_tail )
        plt.xlabel("Small packet length")
        
        plt.ylabel("Overhead / Bytes")
        plt.xticks(range(len(t_1)),t_1)
        
        # plt.xticks([]) 
        plt.xticks(rotation=90,fontsize=6)
        # plt.yscale('log')
        strName = ['SmallFix','BigFix','DyV1_SmallFix',"DyV1_BigFix"]
        plt.figure(figsize=(10, 5))
        plt.savefig("./pdfFigure/"+strName[3]+".pdf")
        plt.show()    
        
    def DyV2_SmallFix(self):
        
        small = 10
        big_1 = 60
        

        OHArray = []
        LAArray = []
        MacroSArr = []
        for big in range(10,big_1):  
            Overhead, _, MacroS, Large = Algorithms().DynamicV2(small,big)

            OHArray.append(Overhead)
            LAArray.append(Large)
            MacroSArr.append(MacroS)


        
    def DyV2(self):
        from mpl_toolkits import mplot3d
        

        def f(x, y):
            Overhead, _, MacroS, Large = Algorithms().DynamicV2(y,x)
            return Overhead

        x = np.arange(10, 80)
        y = np.arange(10, 80)

        X, Y = np.meshgrid(x, y)
        Z = f(X, Y)
                
        

        fig = plt.figure(figsize=(8, 4))
        ax = plt.axes(projection='3d')
        # ax.contour3D(X, Y, Z, 50, cmap='binary')
        
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')

        ax.set_xlabel('Small packet size')
        # ax.xticks(fontsize=12)
        ax.set_ylabel('Big packet size')
        ax.set_zlabel('Overhead ')
        
        strTitle_head = "DyV1 3D Overhead, GS = 2, GF($2^8$), "
        strTitle_tail =  ""
        ax.set_title(strTitle_head + strTitle_tail,fontsize=12)
       
        # ax.view_init(15, 10)
        # plt.savefig("./pdfFigure/"+"DyV1_1510"+".pdf")
        ax.view_init(80, 180)
        plt.savefig("./pdfFigure/"+"DyV1_80180"+".pdf")
        plt.show()
        
    def compareSBMix(self):
        # randomTimes = [20, 40, 60]
        randomTimes = 300# [60]
        loop = 50
        OvOp_list = [[] for _ in range(3)]
        for _ in range(loop):
            
            # for i in range(len(randomTimes)):
            # OvOp_list.append([])
            OHArray=[[] for _ in range(3)] # for small big mix
            for _ in range(randomTimes):
                seed = random.randint(1,2555)
                rand = random.Random(seed)
                data = [rand.randint(10,1400) for _ in range(2)]
                data.sort()
                Overhead, _, _, _ = Algorithms().SmallFix(data[0],data[1])
                OHArray[0].append(Overhead)
                Overhead, _, _, _ = Algorithms().BigFix(data[0],data[1])
                OHArray[1].append(Overhead)
                Overhead, _, MacroS, Large = Algorithms().MixSB(data[0],data[1])
                OHArray[2].append(Overhead)
            for i in range(3):
                OvOp_list[i].append(np.mean(OHArray[i]))

        print OHArray,":",len(OHArray)
            
        # OvOp_list.append(OHArray)
        # plt.figure(figsize=(6, 4))
        fig, axs = plt.subplots(1,1)
        t = np.arange(len(OHArray[0]))
        keysParament_list=['Small Fix', 'Big Fix', 'MixSB']
        # for i in range(len(OHArray)):
        #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
        axs.boxplot(OvOp_list,labels=keysParament_list)
        plt.grid(True)
        plt.xlabel("Different Algorithms",fontsize=18)
        plt.ylabel("Added Overhead Sizes",fontsize=18)
        
        # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
        plt.savefig("./pdfFigure/"+"CompareSBM_r"+str(randomTimes)+"l"+str(loop)+".pdf")
        # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
        plt.show()
        

    def CompareDyV1V2Mix(self):
        randomTimes = 30# [60]
        loop = 500
        OvOp_list = [[] for _ in range(3)]
        for _ in range(loop):
            
            # for i in range(len(randomTimes)):
            # OvOp_list.append([])
            OHArray=[[] for _ in range(3)] # for small big mix
            for _ in range(randomTimes):
                seed = random.randint(1,2555)
                rand = random.Random(seed)
                data = [rand.randint(10,1400) for _ in range(2)]
                data.sort()
                Overhead, _, _, _ = Algorithms().DynamicV1(data[0],data[1])
                OHArray[0].append(Overhead)
                Overhead, _, _, _ = Algorithms().DynamicV2(data[0],data[1])
                OHArray[1].append(Overhead)
                Overhead, _, MacroS, Large = Algorithms().MixDyV1V2(data[0],data[1])
                OHArray[2].append(Overhead)
            for i in range(3):
                OvOp_list[i].append(np.mean(OHArray[i]))

        print OHArray,":",len(OHArray)
            
        # OvOp_list.append(OHArray)
        # plt.figure(figsize=(6, 4))
        fig, axs = plt.subplots(1,1)
        t = np.arange(len(OHArray[0]))
        keysParament_list=['Dynamic V1', 'Dynamic V2', 'MixDyV1V2']
        # for i in range(len(OHArray)):
        #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
        axs.boxplot(OvOp_list,labels=keysParament_list)
        plt.grid(True)
        plt.xlabel("Different Algorithms",fontsize=18)
        plt.ylabel("Added Overhead Sizes",fontsize=18)
        
        # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
        plt.savefig("./pdfFigure/"+"CompareDyV1V2_r"+str(randomTimes)+"l"+str(loop)+".pdf")
        # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
        plt.show()
    
    def CompareDyV1V2(self):
        randomTimes = 300# [60]
        loop = 500
        OvOp_list = [[] for _ in range(2)]
        for _ in range(loop):
            
            # for i in range(len(randomTimes)):
            # OvOp_list.append([])
            OHArray=[[] for _ in range(2)] # for small big mix
            for _ in range(randomTimes):
                seed = random.randint(1,2555)
                rand = random.Random(seed)
                data = [rand.randint(10,1400) for _ in range(2)]
                data.sort()
                Overhead, _, _, _ = Algorithms().DynamicV1(data[0],data[1])
                OHArray[0].append(Overhead)
                Overhead, _, _, _ = Algorithms().DynamicV2(data[0],data[1])
                OHArray[1].append(Overhead)
                
            for i in range(2):
                OvOp_list[i].append(np.mean(OHArray[i]))

        print OHArray,":",len(OHArray)
            
        # OvOp_list.append(OHArray)
        # plt.figure(figsize=(6, 4))
        fig, axs = plt.subplots(1,1)
        t = np.arange(len(OHArray[0]))
        keysParament_list=['Dynamic V1', 'Dynamic V2']
        # for i in range(len(OHArray)):
        #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
        axs.boxplot(OvOp_list,labels=keysParament_list)
        plt.grid(True)
        plt.xlabel("Different Algorithms",fontsize=18)
        plt.ylabel("Added Overhead Sizes",fontsize=18)
        
        # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
        plt.savefig("./pdfFigure/"+"CompV1V2_r"+str(randomTimes)+"l"+str(loop)+".pdf")
        # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
        plt.show()
    
    def CompareAll(self):
        randomTimes = 300# [60]
        loop = 500
        nubAlgorithm=8
        OvOp_list = [[] for _ in range(nubAlgorithm)]
        for _ in range(loop):
            
            # for i in range(len(randomTimes)):
            # OvOp_list.append([])
            OHArray=[[] for _ in range(nubAlgorithm)] # for small big mix
            for _ in range(randomTimes):
                seed = random.randint(1,2555)
                rand = random.Random(seed)
                data = [rand.randint(10,1400) for _ in range(2)]
                data.sort()
                Overhead, _, _, _ = Algorithms().SmallFix(data[0],data[1])
                OHArray[0].append(Overhead)
                Overhead, _, _, _ = Algorithms().BigFix(data[0],data[1])
                OHArray[1].append(Overhead)
                Overhead, _, _, _ = Algorithms().DynamicV1(data[0],data[1])
                OHArray[2].append(Overhead)
                Overhead, _, _, _ = Algorithms().DynamicV2(data[0],data[1])
                OHArray[3].append(Overhead)
                Overhead, _, _, _ = Algorithms().MixDyV1V2(data[0],data[1])
                OHArray[4].append(Overhead)
                Overhead, _, _, _ = Algorithms().MixBDyV1(data[0],data[1])
                OHArray[5].append(Overhead)
                Overhead, _, _, _ = Algorithms().MixBDyV2(data[0],data[1])
                OHArray[6].append(Overhead)
                Overhead, _, _, _ = Algorithms().MixSBDyV1V2(data[0],data[1])
                OHArray[7].append(Overhead)
                
                
                
            for i in range(nubAlgorithm):
                OvOp_list[i].append(np.mean(OHArray[i]))

        print OHArray,":",len(OHArray)
            
        # OvOp_list.append(OHArray)
        plt.figure(figsize=(10, 8))
        #fig, axs = plt.subplots(figsize=(6, 4))
        keysParament_list=['Small Fix','Big Fix','Dynamic V1', 'Dynamic V2',\
                             'MixDyV1V2','MixBDyV1', 'MixBDyV2','MixSBDyV1V2']
        # for i in range(len(OHArray)):
        #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
        plt.boxplot(OvOp_list,labels=keysParament_list)
        plt.grid(True)
        plt.xlabel("Different Algorithms",fontsize=18)
        plt.ylabel("Added Overhead Sizes",fontsize=18)
        plt.xticks(rotation=20)
        # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
        plt.savefig("./pdfFigure/"+"CompAllAl_r"+str(randomTimes)+"l"+str(loop)+".pdf")
        # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
        plt.show()
    
    # def CompareAll(self):
    #     randomTimes = 300# [60]
    #     loop = 500
    #     nubAlgorithm=8
    #     OvOp_list = [[] for _ in range(nubAlgorithm)]
    #     for _ in range(loop):
            
    #         # for i in range(len(randomTimes)):
    #         # OvOp_list.append([])
    #         OHArray=[[] for _ in range(nubAlgorithm)] # for small big mix
    #         for _ in range(randomTimes):
    #             seed = random.randint(1,2555)
    #             rand = random.Random(seed)
    #             data = [rand.randint(10,1400) for _ in range(2)]
    #             data.sort()
    #             Overhead, _, _, _ = Algorithms().SmallFix(data[0],data[1])
    #             OHArray[0].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().BigFix(data[0],data[1])
    #             OHArray[1].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().DynamicV1(data[0],data[1])
    #             OHArray[2].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().DynamicV2(data[0],data[1])
    #             OHArray[3].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().MixDyV1V2(data[0],data[1])
    #             OHArray[4].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().MixBDyV1(data[0],data[1])
    #             OHArray[5].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().MixBDyV2(data[0],data[1])
    #             OHArray[6].append(Overhead)
    #             Overhead, _, _, _ = Algorithms().MixSBDyV1V2(data[0],data[1])
    #             OHArray[7].append(Overhead)
                
                
                
    #         for i in range(nubAlgorithm):
    #             OvOp_list[i].append(np.mean(OHArray[i]))

    #     print OHArray,":",len(OHArray)
            
    #     # OvOp_list.append(OHArray)
    #     plt.figure(figsize=(10, 8))
    #     #fig, axs = plt.subplots(figsize=(6, 4))
    #     keysParament_list=['Small Fix','Big Fix','Dynamic V1', 'Dynamic V2',\
    #                          'MixDyV1V2','MixBDyV1', 'MixBDyV2','MixSBDyV1V2']
    #     # for i in range(len(OHArray)):
    #     #     ax.boxplot(OHArray[i],labels=keysParament_list[i])
    #     plt.boxplot(OvOp_list,labels=keysParament_list)
    #     plt.grid(True)
    #     plt.xlabel("Different Algorithms",fontsize=18)
    #     plt.ylabel("Added Overhead Sizes",fontsize=18)
    #     plt.xticks(rotation=20)
    #     # plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_SF"+".pdf")
    #     plt.savefig("./pdfFigure/"+"CompAllAl_r"+str(randomTimes)+"l"+str(loop)+".pdf")
    #     # plt.savefig("./pdfFigure/"+"CDFofSmallFixV2"+".pdf")
    #     plt.show()
    

if __name__=="__main__":  

    
    # GS2GF8_Algorithms()
    # GS4GF8_Algorithms()
    # showDifferentData()
    # GS2GF8_pdf_figure().SmallFix(0)
    # GS2GF8_pdf_figure().BigFix_advance(2)
    # GS2GF8_pdf_figure().DyV1()
    # GS2GF8_pdf_figure().DyV2()
    #   GS2GF8_pdf_figure().compareSBMix()
    #   GS2GF8_pdf_figure().CompareDyV1V2Mix()
    # GS2GF8_pdf_figure().CompareDyV1V2()
    GS2GF8_pdf_figure().CompareAll()
    # GS4GF8_pdf_figure().CompareAll()
    # boxplot_result = [range(120), list(set([random.randint(1,20) for _ in range(120)]))]
    # strName = ['SmallFix']

    # # plt.boxplot(boxplot_result,labels=str_label)
    # plt.boxplot(boxplot_result)
    
    # plt.show()
    