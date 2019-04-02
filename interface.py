from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import webbrowser
from PIL import ImageTk, Image
import os
import numpy as np

import stund

import plot


def donothing():
    x = 0


def callbackStress():

    if(ans[0].get() == 1):
        title = "Gauss"
    else:
        title = "Jacobi"

    fileName = selected.get()
    print(fileName)
    int_answer = int(AnswerBox.get())
    plotDictionary = stund.main(
        file=fileName, funcType=ans[0].get(), ite=int_answer)
    elemNodes = np.array(plotDictionary["Barras"])-1
    nodeCords = np.array(plotDictionary["Pontos"])
    stress = np.array(plotDictionary["Deformacoes"])*(-1)
    ite = str(plotDictionary["Iteracoes"])

    print(ite)
    # print(elemNodes)
    # print(stress)
    plot.displayTruss(elemNodes, nodeCords, stress, 'Tensão', ite, title=title)


def callbackDeformation():

    if(ans[0].get() == 1):
        title = "Gauss"
    else:
        title = "Jacobi"

    fileName = selected.get()
    print(fileName)
    int_answer = int(AnswerBox.get())
    print(int_answer)
    plotDictionary = stund.main(
        file=fileName, funcType=ans[0].get(), ite=int_answer)
    elemNodes = (np.array(plotDictionary["Barras"])-1)
    nodeCords = np.array(plotDictionary["Deformados"])
    ite = str(plotDictionary["Iteracoes"])
    stress = []
    for i in range(len(elemNodes)):
        stress.append(0)
    plot.displayTrussDeformation(
        elemNodes, nodeCords, stress, 'Deformacao', ite=ite, title=title)


def openFile():
    selectedFile = filedialog.askopenfile(mode='rb', filetypes=(
        ("Text File", "*.fem"), ("All Files", "*.*")), title='Select a file')
    selected.delete(0, END)
    selected.insert(0, str(selectedFile.name))


def callbackWeb():
    webbrowser.open_new(
        r"https://github.com/vitorsv1/STUND/blob/master/README.md")


root = Tk()

# Radio Options

MODES = [
    ("Gauss", 1),
    ("Jacobi", 2)
]
v = IntVar()
v.set(1)  # initialize

# Texts
wellcomeText = "Seja bem-vindo ao STUND, o software de cálculo de treliças."
tutorialText = "Para a utilização, selecione um arquivo .txt nos formatos \n corretos (qualquer dúvida clique em ajuda) e clique em 'Criar Gráfico'\n"

root.style = ttk.Style()
COLOR = '#3E4149'


# Window config
root.minsize(1060, 480)
root.geometry("320x160")
root.configure(background='#3E4149')

# Menu (File, help)
menubar = Menu(root)

# File


filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Salvar", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Arquivo", menu=filemenu)
# Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Documentação", command=callbackWeb)
menubar.add_cascade(label="Ajuda", menu=helpmenu)


root.config(menu=menubar)

title = Label(root, text="\nSTUND",
              background='#3E4149', foreground='#eeeeee', font="Helvetica 16 bold")
title.pack()

subtitle = Label(root, text="Software de Treliças Universitário Dinåmico\n\n",
                 background='#3E4149', foreground='#eeeeee')
subtitle.pack()


lbl0 = Label(root, text=wellcomeText,
             background='#3E4149', foreground='#eeeeee')
lbl0.pack()

lbl1 = Label(root, text=tutorialText,
             background='#3E4149', foreground='#eeeeee')
lbl1.pack()

selectedFile = "aah"
selected = Entry()
selected.insert(0, "arquivoentrada.fem")
selected.pack()
button1 = Button(root, text='Selecione o arquivo texto',
                 highlightbackground='#3E4149', command=openFile)
button1.pack()


subtitle = Label(root, text="\n \n Número máximo de iterações (padrão 80)",
                 background='#3E4149', foreground='#eeeeee')
subtitle.pack()
AnswerBox = Entry()
AnswerBox.insert(0, 80)
AnswerBox.pack()

ans = []
for text, mode in MODES:
    b = Radiobutton(root, text=text,
                    variable=v, value=mode, highlightbackground='#3E4149', background='#3E4149')
    ans.append(v)
    b.pack()

cb = Button(root, text="Criar gráfico de tensão",
            highlightbackground='#3E4149', command=callbackStress)
cb.pack()

cb = Button(root, text="Criar gráfico de deformação",
            highlightbackground='#3E4149', command=callbackDeformation)
cb.pack()

# file = filedialog.askopenfile(mode='rb', title='Select a file')

mainloop()


# root.filename = filedialog.askopenfilename(
#    initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
# print(root.filename)
