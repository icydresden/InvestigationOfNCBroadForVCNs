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


# randomSize_sel = 1
GS = 8
def GS4GF8_Algorithms(randomSize_sel):
    if randomSize_sel == 1:
        runNum = 250 #150
        GS= 4
        OvOp_list = []
        twoEdges_OH = []
        fix_number = 93
        seed = random.randint(1,2555)
        rand = random.Random(seed)

        Result_list=[]
        str_label = []
        loop = 30
        for small in [27,43,59,75,91,107,123,139]:
            OHArray = []
            str_label.append("small="+str(small))
            for _ in range(loop):
                DataList = [small]+[rand.randint(small+1,1401) for _ in range(GS-1)] 
                DataList.sort()
                # =====================
                # Algorithm 0 small fix Al2
                # ======================
            
                small = DataList[0]
                MacroSs = DataList[0]
                Overhead = 0
                # Operation = 2*small
                for i in range(1,GS):
                    Rem = DataList[i] % small
                    
                    Overhead += small - Rem
                    # Operation= 2*small + (big + (small - Rem))
                    # if i < GS-1:
                    #     Operation += 2*DataList[i] 
                    # else: 
                    #     LargestItem = DataList[i] + (small - Rem)
                    #     Operation += DataList[i] 
                OHArray.append(Overhead)
            
            
            # Result_list[1].append(Operation)
            # Result_list[2].append(MacroSs)
            # Result_list[3].append(LargestItem)
            Result_list.append(OHArray)
        plt.figure(figsize=(10, 7.5))
        strTitle_head = "SmallFixV2, Overhead, GF($2^8$), "
        
        strTitle_tail =  " top limitation is 1400 bytes"
        plt.grid()
        plt.legend()
        plt.boxplot(Result_list,labels=str_label)

        plt.title(strTitle_head + strTitle_tail,fontsize=18)
        plt.xlabel("Generation Size",fontsize=18)
        plt.ylabel("Overhead / Bytes",fontsize=18)
        plt.xticks(rotation=10,fontsize=16)
        
        strName = ['SmallFixV2']
        # plt.boxplot(boxplot_result)
        plt.savefig("./pdfFigure/"+strName[0]+"_boxplot.pdf")
        plt.show()
    else:
        pass

def showDifferentData():
    fig_select = 3

    runNum=250
    loopNum=3000
    GS_Group = [2,4,8,16,32,64,128]

    plt.figure(figsize=(6, 4))
    # fig,axs=plt.subplots(1,2)
    
    
    boxplot_result = []
    for GS in GS_Group:
        fileName= "RunNum_"+str(runNum)+"_GS_"+str(GS)+"_Repeat_"+str(loopNum)

        
        #
        if fig_select == 1:
            with open("./twoEdgeFig/"+fileName+".json","r") as input:           
                twoEdge_OH=json.load(input)
        elif fig_select == 2:
            with open("./dynamicV3/"+fileName+".json","r") as input:
                twoEdge_OH=json.load(input)
        elif fig_select == 3:
            with open("./smallFixV2/"+fileName+".json","r") as input:
                twoEdge_OH=json.load(input)
        else:
            pass

    
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
        plt.plot(item_twoEdge,yresult,label="GS "+str(GS))
        boxplot_result.append(twoEdge_OH)
        
    

    plt.legend()
    plt.grid()
    ###
    ### 2
    
    if fig_select == 1:
        plt.title("CDF of TwoEdgesFix, average of "+str(loopNum)+" examples")
    elif fig_select == 2:
        plt.title("CDF of DynamicV3, average of "+str(loopNum)+" examples")
    elif fig_select == 3:
        plt.title("CDF of SmallFixV2, average of "+str(loopNum)+" examples")
    else:
        pass


    plt.ylabel("Percentage %")
    plt.xlabel("Overhead Sizes")
    # plt.xlim(0,1200,100)
    # axs[1].set_xscale('log')
    plt.xticks(rotation=360)
    plt.subplots_adjust(wspace =0.3, hspace =0)
    plt.grid(True)
    

    if fig_select == 1:
        plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_1"+".pdf")
    elif fig_select == 2:
        plt.savefig("./pdfFigure/"+"CDFofDynamicV3_1"+".pdf")
    elif fig_select == 3:        
        plt.savefig("./pdfFigure/"+"CDFofSmallFixV2_1"+".pdf")
    else:
        pass
    plt.show()


    boxplot_label=["GS "+str(GS) for GS in GS_Group]
    plt.boxplot(boxplot_result,labels=boxplot_label)
    plt.grid()
    plt.xlabel("Generation Size")
    plt.ylabel("Added Overhead Sizes")
    plt.legend()
    plt.grid(True)
    
    if fig_select == 1:
        plt.savefig("./pdfFigure/"+"CDFofTwoEdgesFix_2"+".pdf")
    elif fig_select == 2:        
        plt.savefig("./pdfFigure/"+"CDFofDynamicV3_2"+".pdf")
    elif fig_select == 3: 
        plt.savefig("./pdfFigure/"+"CDFofSmallFixV2_2"+".pdf")
    plt.show()




if __name__=="__main__":
    # GS4GF8_Algorithms(1)
    showDifferentData()