from multiprocessing import Pool,cpu_count,Manager#,Lock
import numpy
def tuplize(array):
	if type(array) is list or type(array) is tuple or type(array) is numpy.ndarray:
		result=[]
		for i in array:
			if type(i) is list or type(i) is numpy.ndarray:
				result.append(tuplize(i))
			else:
				result.append(i)
		return tuple(result)
	return array
def get_par(args,name,default=None):
	try:
		return args[name]
	except:
		return default
class Executor:
	default_fun_strc="fun"
	def __init__(self,*fun,**args):
		manager=Manager()
		self.lock_sec_au=manager.Lock()
		self.lock_sec_poc=manager.Lock()
		self.lock_mon_au=manager.Lock()
		self.lock_mon_poc=manager.Lock()
		
		self.clear_fun()
		self.add_fun(fun)
		self.pnum=get_par(args,"pnum",cpu_count())
		self.__xmem__=get_par(args,"__XMEManager__")
		self.results=[]
		'''
		self.dowithlog=get_par(args,"dowithlog",False)
		if self.dowithlog:
			self.logfile=get_par(args,"logfile")
			self.logobj=Logputter(self.logfile,XME_Version_info,get_par(args,"has_been_print",False))
			self.logobj.print_in_screen=get_par(args,"print_in_screen",False)
		'''
	def do_fun(self,args=(),funname=None,returns=None):
		
		locks=args[-4:]
		args=args[:-4]
		
		for i in args:
			'''
			arg=i
			if self.dowithlog:
				if type(arg) is tuple:
					arg+=(self.logobj,)
				elif type(arg) is list:
					arg.append(self.logobj)
				else:
					arg=(arg,self.logobj)
			'''
			if funname==None:
				funname=tuple(self.fun.keys())[-1]
			#result=self.fun[funname](arg)
			'''
			#use global lock
			for j in i:
				if type(i) == type(self.__xmem__):
					i.initial_lock(locks)
			'''
			result=self.fun[funname](*i)
			if returns!=None:
				returns.append(result)
		if returns!=None:
			return returns
	def add_a_pool(self,args,funname=None,close=True,join=True,returns=None):
		pool=Pool(1)
		if funname==None:
			funname=tuple(self.fun.keys())[-1]
		result=pool.apply_async(self.do_fun,(list(args)+[self.lock_sec_poc,self.lock_sec_au,self.lock_mon_poc,self.lock_mon_au],funname,returns))
		#result=pool.apply_async(self.do_fun,(args,funname,returns))
		if close:
			pool.close()
		if join:
			pool.join()
		return tuplize(result.get())
	def build_from_ao(self,ao,close=True,join=True,pnum=None):
		if pnum==None:
			pnum=self.pnum
		pool=Pool(pnum)
		results=[]
		infunname=tuple(self.fun.keys())
		if type(ao) is tuple or type(ao) is list:
			funname=[]
			for i in range(len(ao)):
				if i < len(infunname):
					funname.append(infunname[i])
			for i in range(len(infunname),len(ao)):
				funname.append(infunname[-1])
			new_ao={}
			for i in funname:
				new_ao[i]=()
			for i in range(len(funname)):
				new_ao[funname[i]]+=(ao[i],)
			ao=new_ao
		elif type(ao) is dict:
			new_ao={}
			for i in ao.keys():
				if i in infunname:
					#if i not in new_ao.keys():
					#	new_ao[i]=()
					#new_ao[i]+=(ao[i],)
					if type(ao[i]) is tuple or type(ao[i]) is list:
						new_ao[i]=tuple(ao[i])
					else:
						new_ao[i]=(ao[i],)
				else:
					print("Warnning: fun name:",i,"no in library")
			ao=new_ao
		else:
			ao={infunname[-1]:(ao,)}
		for i in ao.keys():
			for j in ao[i]:
				for k in range(j.pnum):
					results.append(pool.apply_async(self.do_fun,(list(j.args[k])+[self.lock_sec_poc,self.lock_sec_au,self.lock_mon_poc,self.lock_mon_au],i,j.results[k])))
					#results.append(pool.apply_async(self.do_fun,(j.args[k],i,j.results[k])))
		if close:
			pool.close()
		if join:
			pool.join()
		new_results=[]
		for i in results:
			new_results.append(i.get())
		#return tuplize(new_results)
		return new_results
	def add_fun(self,fun):
		if type(fun) is tuple or type(fun) is list:
			tvi=0
			for i in range(len(self.fun.keys()),len(self.fun.keys())+len(fun)):
				self.fun[self.default_fun_strc+str(i)]=fun[tvi]
				tvi+=1
		elif type(fun) is dict:
			for i in self.fun.keys():
				self.fun[i]=fun[i]
		else:
			self.fun[self.default_fun_strc+str(len(self.fun.keys()))]=fun
	#def add_fun2(self,funname,fun):
	#	self.fun[funname]=fun
	#def del_fun(self,funname):
	#	if funname in self.fun.keys():
	#		del(self.fun[funname])
	def clear_fun(self):
		self.fun={}