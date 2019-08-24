# -*- coding: utf-8 -*-
#
#Author: TT_last
#
#This is a daemon for linux judge
#
#
#
import codecs
import sys, os, time, atexit
import subprocess
import fcntl
import sqlite3
from signal import SIGTERM
import configparser
import importlib

#This is the class for judge
#
daemondir = "Path of mine"
cfgfile = "/daemon.ini" # Don't change it!!!!
host = "127.0.0.1"
dbname = "test_db"
cefile = "ce.txt"
dadir = "./data"
tmdir = "./temp"
lockerpath = "/home/rika/"
langf = {1:"Main.c",2:"Main.cpp",3:"Main.java",4:"Main.cpp",5:"Main.cs",6:"Main.vb"}


#This is a daemon module
class Daemon:
	'''
	A daemon for Aqours judge
	'''
	def __init__(self,stdin='/dev/null',stdout='/dev/null',stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr

	def start(self):
		'''
		'''
		os.chdir("./judge");
		#os.umask(0)

		#redirect standard io
		'''
		sys.stdout.flush()
		sys.stderr.flush()
		sin = file(self.stdin,"r")
		sout = file(self.stdout,"a+")
		serr = file(self.stderr,"a+",0)
		os.dup2(sin.fileno(),sys.stdin.fileno())
		os.dup2(sout.fileno(),sys.stdout.fileno())
		os.dup2(serr.fileno(),sys.stderr.fileno())
		'''
		self.run()

	def run(self):
		pass


def makefile(indir,lang,val):
	try:
		os.chdir("./judge")
		sfile = indir + "/" + langf[lang]
		fd = codecs.open(sfile,"wb",'utf-8')
		fd.write(val)
		fd.close()
		return True
	except:
		return False



class judge:
	'''

	'''
	def __init__(self,lang,datadir = "./data",tmpdir = "./temp",
			timelimit = 1000,memlimit = 65535,outlimit = 8192,spj = False,tc = False):
		self.lang = lang
		self.datadir = datadir
		self.tmpdir = tmpdir
		self.timelimit = timelimit
		self.memlimit = memlimit
		self.outlimit = outlimit
		self.spj = spj
		self.tc = tc

	def setlimit(self,timelimit = 1000,memlimit = 65535,outlimit = 8192):
		self.timelimit = timelimit
		self.memlimit = memlimit
		self.outlimit = outlimit

	def run(self):
		try:
			#os.chdir("./Judge")
			self.result,self.mem,self.time = (0,0,0)
			if self.spj and self.tc:
				p = subprocess.Popen("./judge -l "+str(self.lang)+" -D "+self.datadir\
						+" -d "+self.tmpdir+" -t "+str(self.timelimit)+" -m "+str(self.memlimit)+" -o "+str(self.outlimit) + " -S dd -T",shell=True,stdout=subprocess.PIPE)
			elif self.spj:
				p = subprocess.Popen("./judge  -l "+str(self.lang)+" -D "+self.datadir\
						+" -d "+self.tmpdir+" -t "+str(self.timelimit)+" -m "+str(self.memlimit)+" -o "+str(self.outlimit) + " -S dd",shell=True,stdout=subprocess.PIPE)
			elif self.tc:
				p = subprocess.Popen("./judge -l "+str(self.lang)+" -D "+self.datadir\
						+" -d "+self.tmpdir+" -t "+str(self.timelimit)+" -m "+str(self.memlimit)+" -o "+str(self.outlimit) + " -T",shell=True,stdout=subprocess.PIPE)
			else:
				# os.chdir("./judge")
				# print("执行的命令：" + "./judge -l "+str(self.lang)+" -D "+self.datadir\
				#		+" -d "+self.tmpdir+" -t "+str(self.timelimit)+" -m "+str(self.memlimit)+" -o "+str(self.outlimit))
				p = subprocess.Popen("./judge -l "+str(self.lang)+" -D "+self.datadir\
						+" -d "+self.tmpdir+" -t "+str(self.timelimit)+" -m "+str(self.memlimit)+" -o "+str(self.outlimit),shell=True,stdout=subprocess.PIPE)
			for l in p.stdout:
				(self.result,self.mem,self.time) = l.split()
			self.result = int(self.result)
			self.mem = int(self.mem)
			self.time = int(self.time)
		except:
			print("执行评测进程不成功")
			exit(1)

OJ_WAIT = 0
OJ_RUN = 1
OJ_AC = 2
OJ_PE = 3
OJ_TLE = 4
OJ_MLE = 5
OJ_WA = 6
OJ_OLE = 7
OJ_CE = 8
OJ_RE = [9, 10, 11, 12, 15]
OJ_RF = 13
OJ_SE = 14

#this is the judgeDaemon
class JudgeDaemon(Daemon):
	def run(self):
		cfg = configparser.ConfigParser()
		cfg.readfp(open(daemondir+cfgfile))
		host = cfg.get('daemon','Host')
		# dbname = cfg.get('daemon','DataBase')
		cefile = cfg.get('daemon','CE_File')
		dadir = cfg.get('daemon','DataFolder')
		tmdir = cfg.get('daemon','TempFolder')
		lockerpath = cfg.get('daemon','LockerPath')
		# while True:
		try:
			# print("小守护进程执行中...")
			# 连接OJ数据库获取数据
			# con = sqlite3.connect('db.sqlite3') # 本机使用
			con = sqlite3.connect('../db.sqlite3') # 服务器使用
			# print("数据库已连接上")
			cur = con.cursor()
			# print("游标已指定")
			# users = db.users
			# problems = db.problems
			# solutions = db.solutions
			# one_solution = solutions.find_and_modify({'result':OJ_WAIT}, {"$set":{"result":OJ_RUN}})
			sql = "SELECT * FROM judger_code WHERE WJ=1"
			# print("SQL语句已定义")
			cur.execute(sql)
			# print("查询语句SELECT * FROM judger_code WHERE WJ=1已执行")
			solutions = cur.fetchall()
			# print("已获取所有等待评测的代码")
			one_solution = solutions[0] # 找出所有正在等待的代码中的第一条代码
			# print("查找到等待评测的代码为：" + str(one_solution[0]))

			if one_solution != None:
				# user = users.find_one({'name':one_solution['userName']}) 
				user_id = int(one_solution[5]) # 找出该代码的提交者id，转换成int型
				sql_get_user = "SELECT * FROM judger_user WHERE id=?"
				cur.execute(sql_get_user, (user_id,))
				user = cur.fetchall()[0]
				username = user[1]

				lang = one_solution[4] # 找出该代码的语言
				if lang == "cpp":
					lang = 2
				elif lang == "java":
					lang = 3
				code = one_solution[1] # 找出该代码的内容
				problem = int(one_solution[2]) # 找出对应的problem的id
				code_ID = one_solution[0] # 找出对应的主码

				if makefile(tmdir, int(lang), code):
					sql_get_problem = "SELECT * FROM judger_problem WHERE id=?"
					cur.execute(sql_get_problem, (problem,))

					one_problem = cur.fetchall()[0]
					time_limit = one_problem[2] # ms单位的时间限制
					memory_limit = one_problem[3] # kb单位的空间限制

					# if int(one_problem['spj']) == 1 and int(one_problem['TC']) == 1:
						# gzhujudge = judge(one_solution["language"],datadir = dadir +"/" + str(one_solution['problemID']),tmpdir=tmdir,spj=True,tc=True);
					# elif int(one_problem['spj']) == 1:
						# gzhujudge = judge(one_solution["language"],datadir = dadir +"/" + str(one_solution['problemID']),tmpdir=tmdir,spj=True);
					# elif int(one_problem['TC']) == 1:
						# gzhujudge = judge(one_solution["language"],datadir = dadir +"/" + str(one_solution['problemID']),tmpdir=tmdir,tc=True);
					# else:
					aqours_judge = judge(lang, datadir = dadir +"/" + str(problem), tmpdir=tmdir)
					aqours_judge.setlimit(int(time_limit),int(memory_limit))	
					aqours_judge.run()

					if aqours_judge.result == OJ_CE:
						# ce_file = open(tmdir + '/' + cefile)
						# try:
							# all_ce_text = ce_file.read()
							# ce_file.close()
						print("Compile Error")
						sql_ce = "UPDATE judger_code SET WJ=0, CE=1 WHERE id=?"
						cur.execute(sql_ce, (code_ID,))
						con.commit()
						con.close()
							# solutions.update({"_id":one_solution["_id"]},{"$set":{"CE":all_ce_text}})
						# except:
							# ce_file.close()
							# solutions.update({"_id":one_solution["_id"]},{"$set":{"CE":"错误：编译信息无法获取！（可能存在乱码）\n"}})
					elif aqours_judge.result == OJ_AC: #AC
						print("Accepted!")
						# problems.update({"problemID":int(one_solution['problemID'])},{"$inc":{"AC":1}})
						# userfile = lockerpath + str(username) + ".lock"
						# print("userfile:" + str(userfile))
						# userlocker = open(userfile, 'w')
						# print("userlocker执行成功")
						# fcntl.flock(userlocker, fcntl.LOCK_EX)
						# print("文件加锁成功")
						sql_ac = "UPDATE judger_code SET WJ=0, AC=1, time_used=?, memory_used=? WHERE id=?"
						# print(sql_ac)
						cur.execute(sql_ac, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
						# is_ac = solutions.find_one({'problemID':int(one_solution['problemID']),'userName':one_solution['userName'],'result':OJ_AC})
						# if is_ac == None:
							# users.update({'name':user['name']},{"$inc":{"solved":1}})
						# solutions.update({"_id":one_solution["_id"]},{"$set":{"result":gzhujudge.result,"time":gzhujudge.time,"memory":gzhujudge.mem}})
						# fcntl.flock(userlocker, fcntl.LOCK_UN)
						userlocker.close()
					elif aqours_judge.result == OJ_MLE:
						print("Memory Limit Exceeded")
						sql_mle = "UPDATE judger_code SET WJ=0, MLE=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_mle, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_TLE:
						print("Time Limit Exceeded")
						sql_tle = "UPDATE judger_code SET WJ=0, TLE=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_tle, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_WA:
						print("Wrong Answer")
						sql_wa = "UPDATE judger_code SET WJ=0, WA=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_wa, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_PE:
						print("Presentation Error")
						sql_pe = "UPDATE judger_code SET WJ=0, PE=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_pe, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_OLE:
						print("Output Limit Exceeded")
						sql_ole = "UPDATE judger_code SET WJ=0, OLE=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_ole, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_RF:
						print("Restricted Function")
						sql_rf = "UPDATE judger_code SET WJ=0, RF=1 WHERE id=?"
						cur.execute(sql_rf, (code_ID,))
						con.commit()
						con.close()
					elif aqours_judge.result == OJ_SE:
						print("System Error")
						sql_se = "UPDATE judger_code SET WJ=0, SE=1 WHERE id=?"
						cur.execute(sql_se, (code_ID,))
						con.commit()
						con.close()
					else:
						print("Runtime Error")
						sql_re = "UPDATE judger_code SET WJ=0, RE=1, time_used=?, memory_used=? WHERE id=?"
						cur.execute(sql_re, (aqours_judge.time, aqours_judge.mem, code_ID))
						con.commit()
						con.close()
						# else:
						# solutions.update({"_id":one_solution["_id"]},{"$set":{"result":gzhujudge.result,"time":gzhujudge.time,"memory":gzhujudge.mem}})
				# else:
					# pass
		except:
			pass
			# print("没有等待评测的任务")



if __name__ == "__main__":
	importlib.reload(sys)
	daemon = JudgeDaemon(stdout="/dev/stdout")
	daemondir = os.getcwd()
	daemon.run()
