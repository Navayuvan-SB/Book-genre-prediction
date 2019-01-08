import Tkinter
from Tkinter import *
import ttk
from PIL import Image, ImageTk
from nltk.tokenize import word_tokenize
import urllib2
import random
import os
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

class MachineLearning:

	def __init__(self):
		pass


	def getHtml(self):
		self.genreListBox.delete(0, END)
		self.individualListBox.delete(0, END)
		r = open("Genres.txt", "r")
		for x in r:

			path = os.getcwd()+ "/" + x[37:-1]+".txt"

			if not os.path.exists(path):
				print "true"
				response = urllib2.urlopen(x)
				page = response.read()
				out = open(x[37:-1]+".txt", "w")
				out.write(page)
				out.close()
		r.close()

		self.getData()

	def getData(self):
		r = open("Genres.txt", "r")
		self.documents = []
		time = 1
		for x in r:
			inq = open(x[37:-1]+".txt", "r")

			for q in inq:
				search = "<a class=\"bookTitle\" href=\"/book/show/"
				if search in q:
					a = q
					a = ' '.join(a.split())
					f = ""
					o = 0
					for e in range(len(a)):
						if a[e] == '>':
							o = 1
							continue
						if o == 1 and a[e] == '(':
							break
						if o == 1:
							f = f + a[e]
					#print f
					f = word_tokenize(f)
					for words in f:
						if time == 1:
							self.documents.append([])
							self.documents[0].append(0)
							time = 0
						else:
							if words not in self.documents[0]:
								self.documents[0].append(words)

			inq.close()


		r.close()

		self.updateDataSet()

	def updateDataSet(self):
		r = open("Genres.txt", "r")
		ids = 0
		t = 1
		self.genreid = [] 
		self.labels = []
		for x in r:
			self.genreid.append([])
			self.genreid[ids].append(x[37:-1])
			self.genreid[ids].append(ids+1)

			self.genreListBox.insert(END, x[37:-1])

			response = urllib2.urlopen(x)
			inq = open(x[37:-1]+".txt", "r")
			labelid = 0
			for q in inq:
				search = "<a class=\"bookTitle\" href=\"/book/show/"
				if search in q:
					labelid = labelid + 1
					a = q
					a = ' '.join(a.split())
					f = ""
					o = 0
					for e in range(len(a)):
						if a[e] == '>':
							o = 1
							continue
						if o == 1 and a[e] == '(':
							break
						if o == 1:
							f = f + a[e]


					fInsert =x[37:-1]+ str(labelid) + "-" + f
					self.individualListBox.insert(END, fInsert)


					# print f
					self.documents.append([])
					self.documents[t].append(f)
					self.labels.append(ids+1)
					# print t
					f = word_tokenize(f)

					for j in range(1,len(self.documents[0])):
						flag = 0
						for i in range(len(f)):
							if f[i] == self.documents[0][j]:
								#self.documents[t].append(1)
								flag = 1
						if flag == 1:
							self.documents[t].append(1)
						else:
							self.documents[t].append(0)
					t = t + 1
			ids = ids + 1
		r.close()

		self.makeDocument()

	def makeDocument(self):
		for x in range(1,len(self.documents)):
			self.documents[x].append(self.labels[x-1])

		self.trainTestData()

	def trainTestData(self):
		doc = self.documents[:]
		del doc[0]
		random.shuffle(doc)

		self.featuresets = []
		self.finallabels = []

		for x in range(len(doc)):
			self.featuresets.append([])
			for y in range(1,len(doc[x])):
				if y != len(doc[x])-1:
					self.featuresets[x].append(doc[x][y])
				else:
					self.finallabels.append(doc[x][y])

		#print len(featuresets)
		#print len(finallabels)

		out = open("Result.txt", "w")
		out1 = open("Result1.txt", "w")

		out.write(str(self.featuresets))
		out1.write(str(self.finallabels))

		self.trainClassifier()

		#print self.documents[0]
	def trainClassifier(self):
		
		self.LR = LogisticRegression()
		self.LR.fit(self.featuresets, self.finallabels)
		self.indicateLabel.config(text="<Trained>", bg = "yellow")
		self.mw.geometry("1000x920")
		#self.mainFrame2 = Frame(self.mw, bg = "#ffd9b3", width = 1000, height = 640)

	def indivSelected(self, event):
		
		selected = self.individualListBox.get(self.individualListBox.curselection())
		selectedWrap = ""
		flag = 0
		#print selected
		for x in range(len(selected)):
			if selected[x] == "-":
				flag = 1

			if flag == 1:
				selectedWrap = selectedWrap + selected[x]

		selectedWrap = selectedWrap[1:] 
		selectedWrap = word_tokenize(selectedWrap)

		#print selectedWrap

		selectedFeatures = [[]]
		for j in range(1,len(self.documents[0])):
			flag = 0
			for i in range(len(selectedWrap)):
				#print selectedWrap[i] , " ---- " , self.documents[0][j]
				if selectedWrap[i] == self.documents[0][j]:
					#self.documents[t].append(1)
					flag = 1
			if flag == 1:
				selectedFeatures[0].append(1)
			else:
				selectedFeatures[0].append(0)
		#print selectedFeatures
		result = self.LR.predict(selectedFeatures)

		result = result[0]

		for k in range(len(self.genreid)):
			if str(result) == str(self.genreid[k][1]):
				resultString = self.genreid[k][0]
		self.resultIndivLabel.grid(row = 1, column = 1, columnspan = 1)
		self.resultIndividual.set("Predicted Genre: " + resultString)

	def genreSelected(self, event):

		genre = self.genreListBox.get(self.genreListBox.curselection())
		genreBookCount = 0
		for i in range(len(self.genreid)):
			if genre == self.genreid[i][0]:
				genreId = self.genreid[i][1]

		genreDocument = []
		for i in range(len(self.documents)):
			if genreId == self.documents[i][len(self.documents[i])-1]:
				genreDocument.append(self.documents[i])
				genreBookCount = genreBookCount + 1

		
		docs = genreDocument[:]
		del docs[0]
		random.shuffle(docs)

		self.featuresetsG = []
		self.finallabelsG = []

		for x in range(len(docs)):
			self.featuresetsG.append([])
			for y in range(1,len(docs[x])):
				if y != len(docs[x])-1:
					self.featuresetsG[x].append(docs[x][y])
				else:
					self.finallabelsG.append(docs[x][y])


		predicted = self.LR.predict(self.featuresetsG)
		accuracyScore = accuracy_score(self.finallabelsG, predicted, normalize = False)
		#print "Total : ", genreBookCount
		#print "Correct : ", accuracyscore
		
		accuracyPercent = accuracy_score(self.finallabelsG, predicted, normalize = True)
		#print "Accuracy percent : ", accuracyPercent*100

		self.resultGenreListBox.delete(0, END)
		self.resultGenreListBox.insert(END, "Genre :"+genre)
		self.resultGenreListBox.insert(END, "Total no of books: "+str(genreBookCount))
		self.resultGenreListBox.insert(END, "Correctly predicted: "+str(accuracyScore))
		self.resultGenreListBox.insert(END, "Wrongly predicted: "+str(genreBookCount-accuracyScore))
		self.resultGenreListBox.insert(END, "Accuracy percent: "+str(accuracyPercent*100))


class main(MachineLearning):

	def __init__(self):

		MachineLearning.__init__(self)
		self.gui()


	def gui(self):

		self.mw = Tkinter.Tk()
		self.mw.title("Book Tools v1.01")
		self.mw.geometry("1000x280")
		self.mw.resizable(0,0)

		mainFrame1 = Frame(self.mw, bg = "#ffd9b3", width = 1000, height =280)
		mainFrame1.grid(row = 0, column = 0, columnspan = 1)
		mainFrame1.grid_propagate(0)

		Frame1 = Frame(mainFrame1, bg = "white", width = 1000, height = 180, highlightbackground = "#ffd9b3", highlightcolor = "#ffd9b3", highlightthickness = 5)
		Frame1.grid(row = 0, column = 0, columnspan = 1)
		Frame1.pack_propagate(0)

		canvas1 = Label(Frame1, width = 100, height = 100, bg="white")
		img = Image.open('img.png')
		img1 = ImageTk.PhotoImage(img)
		canvas1.config(image = img1)
		canvas1.pack(side=TOP, expand = YES)

		Frame2 = Frame(mainFrame1, width = 800, height = 100, bg="white", highlightthickness = 5, highlightcolor = "#ffd9b3", highlightbackground="#ffd9b3")
		Frame2.grid(row = 1, column = 0, columnspan = 2)
		Frame2.grid_propagate(0)

		subFrame2 = Frame(Frame2, width = 780, height = 40, bg = "white")
		subFrame2.grid(row = 0, column = 0, columnspan = 1)
		subFrame2.pack_propagate(0)

		genreFilePathLabel = Label(subFrame2, width = 30, height = 50, bg="white", fg = "black", text = "Genres File Path:")
		genreFilePathLabel.pack(side=LEFT, expand = YES)

		entry = Entry(subFrame2, width = 50)
		entry.pack(side=RIGHT, expand = YES)
		entry.insert(0,"Genres.txt")

		subFrame3 = Frame(Frame2, width = 780, height = 40, bg="white")
		subFrame3.grid(row = 1, column = 0, columnspan = 1)
		subFrame3.pack_propagate(0)

		fetchButton = Button(subFrame3, width = 30, height = 50, text = "Fetch & Train", command = self.getHtml)
		fetchButton.pack(side = LEFT, expand = YES)

		self.indicateLabel = Label(subFrame3, width = 25, height = 50, text = "<Stopping>", fg="black", bg="red")
		self.indicateLabel.pack(side=RIGHT, expand = YES)

		self.mainFrame2 = Frame(self.mw, bg = "#ffd9b3", width = 1000, height = 640)
		self.mainFrame2.grid(row = 1, column = 0, columnspan = 1)
		self.mainFrame2.grid_propagate(0)


		Frame3 = Frame(self.mainFrame2, bg = "#ffd9b3", width = 800, height = 320, highlightbackground = "#ffd9b3", highlightcolor = "#ffd9b3", highlightthickness = 5)
		Frame3.grid(row = 0, column = 0, columnspan = 2, padx = (92,0))
		Frame3.grid_propagate(0)

		Frame4 = Frame(self.mainFrame2, bg = "#ffd9b3", width = 800, height = 320, highlightbackground = "#ffd9b3", highlightcolor = "#ffd9b3", highlightthickness = 5)
		Frame4.grid(row = 1, column = 0, columnspan = 2, padx = (100,0))
		Frame4.pack_propagate(0)

		booksLabel = Label(Frame3, bg = "#ffd9b3", width = 80, height = 2, text = "Individual Books")
		booksLabel.config(font=("Airal", 12))
		booksLabel.grid(row = 0, column = 0, columnspan = 2)

		self.individualListBox = Listbox(Frame3, bg="white", width = 49, height = 15)
		self.individualListBox.grid(row = 1, column = 0, columnspan = 1)
		self.individualListBox.bind("<Double-Button-1>", self.indivSelected)

		self.resultIndividual = StringVar()
		self.resultIndividual.set("")
		self.resultIndivLabel = Label(Frame3, bg="green",fg = "black",  width = 40, height = 15, textvariable = self.resultIndividual)
		self.resultIndivLabel.grid(row = 1, column = 1, columnspan = 1)
		self.resultIndivLabel.grid_forget()

		accuracyGenreLabel = Label(Frame4, bg = "#ffd9b3", width = 80, height = 2, text = "Accuracy analysis based \n on Genres:")
		accuracyGenreLabel.config(font=("Airal", 12))
		accuracyGenreLabel.grid(row = 0, column = 0, columnspan = 2)

		self.genreListBox = Listbox(Frame4, bg="white", width = 40, height = 14)
		self.genreListBox.grid(row = 1, column = 0, columnspan = 1)
		self.genreListBox.bind("<Double-Button-1>", self.genreSelected)

		self.resultGenreListBox = Listbox(Frame4, bg="white", width = 55, height = 14)
		self.resultGenreListBox.grid(row = 1, column = 1, columnspan = 1)

m = main()
m.mw.mainloop()		