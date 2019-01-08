from nltk.tokenize import word_tokenize
import urllib2
import random
import os
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

class main:

	def getHtml(self):
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
			response = urllib2.urlopen(x)
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

	def makeDocument(self):
		for x in range(1,len(self.documents)):
			self.documents[x].append(self.labels[x-1])

	def trainTestData(self):
		doc = self.documents
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


		self.train_X = self.featuresets[:320]
		self.train_Y = self.finallabels[:320]
		self.test_X = self.featuresets[320:]
		self.test_Y = self.finallabels[320:]

	def trainClassifier(self):
		LR = LogisticRegression()
		LR.fit(self.featuresets, self.finallabels)
		 
		predict_y = LR.predict([[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

		print predict_y

		#accuracy = accuracy_score(self.test_Y, predict_y, normalize=True)

		#print "LR: ", accuracy


m = main()
m.getHtml()
m.getData()
m.updateDataSet()
m.makeDocument()
m.trainTestData()
m.trainClassifier()
#print len(m.documents)
#print len(m.labels)
#print m.genreid
#print m.documents

#for x in range(len(m.documents)):
#	print len(m.documents[x])
