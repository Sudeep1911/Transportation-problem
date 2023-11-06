import tkinter as Tk
from tkinter import *
from functools import partial

global choice
global rows
global cols
rows,cols=0,0
choice=0
text_var = []
entries = []
dem=[]
tex=[]
sup=[]
text=[]

def method():
    def get_varb():
        global choice
        choice=varb.get()
    Label(window, text="Transportation Problem",width=20,font=("bold", 20)).place(x=40,y=53)
    Label(window, text="Choose the method",width=20,font=("bold", 16)).place(x=75,y=110)
    varb= IntVar()
    Radiobutton(window, text="North-West Corner",padx = 20, variable=varb,value=1).place(x=100,y=160)
    Radiobutton(window, text="Minimum Cost",padx = 20, variable=varb,value=2).place(x=100,y=210)
    Radiobutton(window, text="Vogel's Approximation Method",padx = 20,variable=varb,value=3).place(x=100,y=260)
    Button(window,text='Submit',width=20,bg='brown',fg='white',command=get_varb).place(x=120,y=310)


def matrix():
    rows,cols=IntVar(),IntVar()
    x1,y1=20,20
    Label(matrix_frame, text = "Enter rows:", font=('arial',10,'bold')).place(x=x1,y=y1)
    Entry(matrix_frame, textvariable = rows,width = 5).place(x=x1+100,y=y1+3)
    Label(matrix_frame, text = "Enter cols:", font=('arial',10,'bold')).place(x=x1,y=y1+40)
    Entry(matrix_frame, textvariable = cols,width = 5).place(x=x1+100,y=y1+43)
    Button(matrix_frame,text = "Generate",command = partial(enter,rows,cols,x1,y1),width = 10).place(x=x1+25,y=y1+80)

def enter(rows,cols,x1,y1):
    Label(matrix_frame, text="Enter matrix :", font=('arial', 10, 'bold')).place(x=x1, y=y1+120)
    x1+=20
    y1+=160
    rows,cols = rows.get(),cols.get()
    x2 = 0
    y2 = 0
    for i in range(rows):
        text_var.append([])
        entries.append([])
        for j in range(cols):
            text_var[i].append(IntVar())
            entries[i].append(Entry(matrix_frame, textvariable=text_var[i][j],width=5))
            entries[i][j].place(x=x1 + x2, y=y1 + y2)
            x2 += 50

        y2 += 50
        x2 = 0
    y2=y2+165

    Label(matrix_frame, text="Enter Demand :", font=('arial', 10, 'bold')).place(x=x1-20, y=y2)
    k=0
    for i in range(cols):
        tex.append(IntVar())
        dem.append(Entry(matrix_frame, textvariable=tex[i],width=5).place(x=x1 + k, y=y2+40))
        k+=50
    y2+=65
    Label(matrix_frame, text="Enter Supply :", font=('arial', 10, 'bold')).place(x=x1-20, y=y2)

    k=0
    for j in range(rows):
        text.append(IntVar())
        sup.append(Entry(matrix_frame, textvariable=text[j],width=5).place(x=x1 + k, y=y2+40))
        k+=50
    Button(matrix_frame,text="Submit", width=10, command=partial(solu,text_var,tex,text,rows,cols)).place(x=x1+7,y=y2+80)

def least_cell(Supply,Demand,list2):
    list3 = [[0 for _ in range(len(Demand))] for _ in range(len(Supply))]
    while (all(Supply[i] >= 0 for i in range(len(Supply))) and all(Demand[j] >= 0 for j in range(len(Demand)))):
        min_cost = float("inf")
        (k, l) = (None,None)
        for i in range(len(Supply)):
            for j in range(len(Demand)):
                if Supply[i] > 0 and Demand[j] > 0:
                        cost_ij = list2[i][j]
                        if cost_ij < min_cost:
                            min_cost = cost_ij
                            (k, l)=(i,j)
        list3[k][l] = min(Supply[k], Demand[l])
        Supply[k] -= list3[k][l]
        Demand[l] -= list3[k][l]
        if(all(Supply[i]==0 for i in range(len(Supply))) and all(Demand[j]==0 for j in range(len(Demand)))):
            return(list3)

def northwest(Supply,Demand,list2):
    n,m=0,0
    list3 = [[0 for _ in range(len(Demand))] for _ in range(len(Supply))]
    while(n!=len(Supply) and m!=len(Demand)):
        mini=min(Supply[n],Demand[m])
        list3[n][m]=mini
        Supply[n]-=mini
        Demand[m]-=mini
        if(Supply[n]<Demand[m]):
            n+=1
        elif(Demand[m]<Supply[n]):
            m+=1
        else:
            n+=1
            m+=1
    return(list3)
   
def diff(list2,n,m):
   rowdif=[]
   coldif=[]
   for i in range(n):
      arr=list2[i][:]
      arr.sort()
      rowdif.append(arr[1]-arr[0])
   col=0
   while col<m:
      arr=[]
      for j in range(n):
         arr.append(list2[j][col])
      arr.sort()
      col+=1
      coldif.append(arr[1]-arr[0])
   return rowdif,coldif

def vam(Supply,Demand,list2):
    list3 = [[0 for _ in range(len(Demand))] for _ in range(len(Supply))]
    list4=list2
    n,m=len(Supply),len(Demand)
    while(all(Supply[i] >= 0 for i in range(len(Supply))) and all(Demand[j] >= 0 for j in range(len(Demand)))):
        row,col=diff(list4,n,m)
        maxi1=max(row)
        maxi2=max(col)
        if(maxi1>=maxi2):
            for ind,val in enumerate(row):
                if(val==maxi1):
                    mini1=min(list4[ind])
                    for ind2,val2 in enumerate(list4[ind]):
                        if(val2==mini1):
                            mini2=min(Supply[ind],Demand[ind2])
                            list3[ind][ind2]=mini2
                            Supply[ind]-=mini2
                            Demand[ind2]-=mini2
                            if(Demand[ind2] == 0):
                                for r in range(n):
                                    list4[r][ind2] = 1000
                            elif(Supply[ind]==0):
                                for r in range(m):
                                    list4[ind][r] = 1000
                            break
                    break
        elif(maxi2>maxi1):
            for ind,val in enumerate(col):
                if(val==maxi2):
                    mini1=1000
                    for j in range(n):
                        mini1=min(mini1,list2[j][ind])
                    for ind2 in range(n):
                        val2=list2[ind2][ind]
                        if(val2==mini1):
                            mini2=min(Supply[ind2],Demand[ind])
                            list3[ind2][ind]=mini2
                            Supply[ind2]-=mini2
                            Demand[ind]-=mini2
                            if(Demand[ind] == 0):
                                for r in range(n):
                                    list4[r][ind] = 1000
                            elif(Supply[ind2]==0):
                                for r in range(m):
                                    list4[ind2][r]=1000
                            break
                    break
        if(all(Supply[i]==0 for i in range(len(Supply))) and all(Demand[j]==0 for j in range(len(Demand)))):
            return(list3)

def solu(text_var,tex,text,rows,cols):        
    list1=[]
    list2=[]
    list3=[]
    l=[]
    check=choice
    for i in range(rows):
        list2.append([])
        l.append([])
        for j in range(cols):
            list2[i].append(text_var[i][j].get())
            l[i].append(text_var[i][j].get())

    Demand=[]
    for i in range(cols):
        Demand.append(tex[i].get())

    Supply=[]
    for j in range(rows):
        Supply.append(text[j].get())



    if(sum(Demand)<sum(Supply)):
        result_text.insert(INSERT,f"The Demand {sum(Demand)} which is less than {sum(Supply)},\nso adding a coloumn containing 0 and {sum(Supply)-sum(Demand)} to Demand.\n\n")
        for i in range(0,rows):
            list2[i].append(0)
            l[i].append(0)
        cols+=1
        Demand.append(sum(Supply)-sum(Demand))
        
    elif(sum(Supply)<sum(Demand)):
        result_text.insert(INSERT,f"The Supply {sum(Supply)} which is less than {sum(Demand)},\nso adding a row containing 0 and {sum(Demand)-sum(Supply)} to Demand.\n\n")
        list1=[]
        k=[]
        for j in range(0,cols):
            list1.append(0)
            k.append(0)
        list2.append(list1)
        l.append(k)
        rows+=1
        Supply.append(sum(Demand)-sum(Supply))
    
    ques=""
    for i in range(0,rows):
        for j in range(0,cols):
            ques+=str(list2[i][j])
            ques+="\t"
        ques+="\n"
    
    dem=""
    for i in range(cols):
        dem+=str(Demand[i])
        dem+="\t"
    sup=""
    for j in range(rows):
        sup+=str(Supply[j])
        sup+="\t"
        
    result_text.insert(INSERT,f"The question:\n{ques}\nDemand:\n{dem}\n\nSupply\n{sup}\n\n")
    
    if(check==1):
        list3=northwest(Supply,Demand,list2)
    elif(check==2):
        list3=least_cell(Supply,Demand,l)
    elif(check==3):
        list3=vam(Supply,Demand,list2)
    
    solution=0
    for i in range(0,rows):
        for j in range(0,cols):
            solution+=l[i][j]*list3[i][j]

    res=""
    result_text.insert(INSERT,f"Allocations:\n")
    for i in range(0,rows):
        for j in range(0,cols):
            res+=str(list3[i][j])
            res+="\t"
        res+="\n"
    result_text.insert(INSERT,res)
    result_text.insert(INSERT,f"\nThe optimal solution :{solution} \n")
    result_text.pack()
    result_text.config(state=DISABLED)

def destroy():
    window.destroy()

window = Tk()
window.title("Matrix")
window.geometry("1200x550")
matrix_frame=Frame(window)
matrix_frame.place(x=420,y=0,width=350,height=550)
result_frame=Frame(window)
result_frame.place(x=770,y=0,width=430,height=550)
result_text=Text(result_frame,width=430,height=550,bg="#EEEEEE")
method()
Button(window,text='Enter Dimensions',width=20,bg='brown',fg='white',command=matrix).place(x=120,y=340)
Button(window,text="Exit",width=20,bg='brown',fg='white',command=destroy).place(x=120,y=370)
window.mainloop()
