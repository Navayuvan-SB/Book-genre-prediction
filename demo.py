from nltk.tokenize import word_tokenize
import urllib2
import random
class main:

	def getUrl(self):

		r = open("Genres.txt", "r")
		self.documents = []
		time = 1
		for x in r:
			response = urllib2.urlopen(x)
			page = response.read()
			out = open("html.txt", "w")
			out.write(page)
			out.close()

			inq = open("html.txt", "r")

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
			page = response.read()
			out = open("html.txt", "w")
			out.write(page)
			out.close() 
			inq = open("html.txt", "r")
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
						for i in range(len(f)):
							if f[i] == self.documents[0][j]:
								self.documents[t].append(1)
							else:
								self.documents[t].append(0)
					t = t + 1
			ids = ids + 1

	def makeDocument(self):
		for x in range(1,len(self.documents)):
			self.documents[x].append(self.labels[x-1])

	def trainTestData(self):
		doc = self.documents
		del doc[0]
		random.shuffle(doc)

		trainData = []
		testData = []

		


m = main()
m.getUrl()
m.updateDataSet()
m.makeDocument()

print len(m.documents)
print len(m.labels)
print m.genreid
print m.documents