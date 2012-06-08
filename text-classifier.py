# Lobang Club Dev Challenge Submission by Ray Dino
# Version 6
# May 18 , 2012

from sys import argv
import csv
import math

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
	csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [cell for cell in row]

		
def main():
	tokens = " ,'\":~`!@#$%^&*()-_+={}[]\\/?>.<|1234567890"
	minlen = 1
	blacklist = ["AND", "IN", "FOR", "THE", "A", "AN", "MY"]

	if (len(argv)!=4):
		print "Usage: %s <categories> <training set> <competition set>" % (argv[0])
		exit()
	
	category_arg = argv[1]
	training_arg = argv[2]
	competition_arg = argv[3]
	
	categories = {}
	origcategories = {}
	labelno = 0
	termcatcount = {}
	termcount = {}
	
	categories_file = open(category_arg, 'rU')
	reader = unicode_csv_reader(categories_file)
	for row in reader:
		cat = row[0].upper().strip()
		if cat not in categories:
			origcategories[cat] = row[0].strip()
			categories[cat] = 0
		categories[cat]+=1
		labelno+=1
		terms = str.split(row[0])
		for term in terms:
			uterm = term.upper().strip(tokens)
			if len(uterm) > minlen and uterm not in blacklist:
				if uterm not in termcount:
					termcount[uterm] = 1
				termcount[uterm]+=1
				if (uterm, cat) not in termcatcount:
					termcatcount[(uterm, cat)] = 1
				termcatcount[(uterm, cat)]+=1
	
	training_file = open(training_arg, 'rU')
	reader = unicode_csv_reader(training_file)
	reader.next()
	for row in reader:
		cat = row[1].upper().strip()
		if cat not in categories:
			origcategories[cat] = row[1].strip()
			categories[cat] = 0
		categories[cat]+=1
		labelno+=1
		terms = str.split(row[0])
		for term in terms:
			uterm = term.upper().strip(tokens)
			if len(uterm) > minlen and uterm not in blacklist:
				if uterm not in termcount:
					termcount[uterm] = 1
				termcount[uterm]+=1
				if (uterm, cat) not in termcatcount:
					termcatcount[(uterm, cat)] = 1
				termcatcount[(uterm, cat)]+=1

	result_name = "results.csv"
	result_file = open(result_name, "w")
	
	competition_file = open(competition_arg, 'rU')
	reader = unicode_csv_reader(competition_file)
	for row in reader:
		prob = {}
		found = False
		terms = str.split(row[0])
		for term in terms:
			uterm = term.upper().strip(tokens)
			if uterm in termcount:
					found = True
					break;
		if found:
			for category in categories:
				cat = category.upper()
				logprob = 0
				terms = str.split(row[0])
				for term in terms:
					uterm = term.upper().strip(tokens)
					if len(uterm) > minlen and uterm not in blacklist:
						if (uterm, cat) not in termcatcount:
							termcatcount[(uterm,cat)]=1
						if uterm not in termcount:
							termcount[uterm] = 1
						logprob += math.log(float(termcatcount[(uterm, cat)])/float(termcount[uterm]))
				prob[cat] = math.exp(logprob)
			
			key = ""
			maxn = 0.0
			for p in prob:
				if prob[p] > maxn:
					maxn = prob[p]
					key = p
				
			keys = [key]
			for p in prob:
				if key!=p and ((prob[key]-(prob[key]*0.3))<=prob[p]):
					keys.append(p)
			for k in keys:
				result_file.write("%s,%s\n" % (row[0], origcategories[k]));
		
	print "%s result file created!" % result_name

main()
