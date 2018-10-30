#!/usr/bin/env python3
# Elham Jaffar
# Udacity - FSND - Project (1): Log Analysis
# It uses PostgreSQL to answer a three quesiton  
#This file prints out the result in command line based and it saves the output to output.txt file

import psycopg2

#To manage colors for questions and answers 
#(It has been taken form https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python)
class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#Questions
quesiton_1 = "What are the most popular three articles of all time?"
quesiton_2 = "Who are the most popular article authors of all time?"
quesiton_3 = "On which days did more than 1% of requests lead to errors?"
#Answers as Queries
#The CONCAT() function adds two or more expressions together.
#date_trunc to group the time by day
#round to round the numbers 
query_to_answer_1 = "select title, count(title) as views from articles,log where log.status = '200 OK' and log.path = concat('/article/',articles.slug) group by title order by views desc limit 3;"
query_to_answer_2 = "select name, count(author) as views from articles,log, authors where log.status = '200 OK' and log.path = concat('/article/',articles.slug) and articles.author = authors.id group by name order by views desc;"
query_to_answer_3 = "select to_char(day,'Mon DD,YYYY'), error_percentage from (select date_trunc('day', time) as day, round(100.0*sum(case log.status when '404 NOT FOUND' then 1 else 0 end)/count(log.status),3) as error_percentage from log  group by 1 order by 1) subq where error_percentage > 1;"

#getResult: To pass a request and return a result
def getResult(query):
	#Connect to the database
	db = psycopg2.connect(database="news")
	c = db.cursor()
  	c.execute(query)
  	answers = c.fetchall()
  	db.close()
  	return answers

#write the output to text file
file = open('output.txt','w')

#Answer Question 1
#It takes an query and its prints out the result
def answer_question_1(query):
	answer = getResult(query)
	print(color.BOLD + color.RED + quesiton_1 + color.END)
	file.write(quesiton_1 + "\n") #Write to the output file
	for a in answer:
		print("\""+ str(a[0]) + "\"" + ' -- ' + str(a[1]) + 'views')
		file.write("\""+ str(a[0]) + "\"" + ' -- ' + str(a[1]) + 'views' + "\n")

#Answer Question 2
#It takes an query and its prints out the result
def answer_question_2(query):
	answer = getResult(query)
	print(color.BOLD + color.RED + quesiton_2 + color.END)
	file.write(quesiton_2 + "\n")
	for a in answer:
		print(str(a[0])+ ' -- ' + str(a[1]) + 'views')
		file.write(str(a[0])+ ' -- ' + str(a[1]) + 'views' + "\n")

#Answer Question 3
#It takes an query and its prints out the result
def answer_question_3(query):
	answer = getResult(query)
	print(color.BOLD + color.RED + quesiton_3 + color.END)
	file.write(quesiton_3 + "\n")
	for a in answer:
		#round the percentage before ocnvert it to string
		print(str(a[0]) + ' -- ' + str(round(a[1],2)) + '%')
		file.write(str(a[0]) + ' -- ' + str(round(a[1],2)) + '%' + "\n")


#print out the answers
answer_question_1(query_to_answer_1)
#to get space between questions
file.write("" + "\n") 
print("")
answer_question_2(query_to_answer_2)
#to get space between questions
file.write("" + "\n")
print("")
answer_question_3(query_to_answer_3)
print("")
print("The questions and their answers have been already saved in output.txt file, in black/white format !")
file.close()
