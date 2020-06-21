letter = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z' , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z' }
digit  = '0123456789'
symboladdop ={'sub','add'}
symbolmulop={'mul','div'}
idf ='identifier'
symaddop='symboladdop'
symmulop='symbolmulop'
symeq='equal'
symequal='symbolequal'
DT_int ='Int'
DT_flout='float'
####erorr###3
class MyError:
	def __init__(self, Error_name ,types,details,pos_start):
		self.Error_name=Error_name
		self.details =details
		self.type = types
		self.pos_start =pos_start
	def ERRoR(self):
		result = f' Error name :{self.Error_name} ({self.type}: {self.details}) position :{self.pos_start + 1}'
		return result	
		
##tokens#
class Token:
	def __init__(self ,type_,value=None):
		self.type=type_
		self.value=value
	def __repr__(self):
		if self.value:
			return f'{self.type}:{self.value}'
		return f'{self.type}'		
###lexer##	   	
class Scaner:
 	def __init__(self, path):
 		myfile=open(path,'r')
 		text=''
 		for line in myfile:
 			text+=line
 		#print(text)
 		self.text=text
 		self.pos=-1
 		self.current_char= None
 		self.advance()
 	def advance(self):
 		self.pos+=1
 		self.current_char= self.text[self.pos] if self.pos<len(self.text) else '&'
 		#print(self.current_char)
 	def make_token(self):
 
 		tokens =[ ]
 		while self.current_char!= '&':
 			if self.current_char in ' ' or self.current_char=='\n' :
 				self.advance()
 			elif self.current_char in digit:
 				tokens.append(self.make_numbers())
 				#self.advance()
 			elif self.current_char in letter:
 				tokens.append(self.make_letter())
 				#self.advance()
 			else:
 				pos_start = self.pos
 				char = self.current_char
 				self.advance()
 				erorr = MyError('IllegalCharError','Char',char,self.pos)
 				return [] ,erorr.ERRoR()
 		return tokens,None
 	def make_numbers(self):
 			num_str =''
	 		dot_count =0
	 		while self.current_char != '&' and self.current_char in digit or self.current_char =='.':
	 			if self.current_char=='.':
	 				if dot_count ==1: break
	 				dot_count+=1
	 				num_str+='.'
	 			else:
	 				num_str+= self.current_char
	 			self.advance ()
	 		if dot_count ==0:
	 			return Token(DT_int,int(num_str))
	 		else :
	 			return Token(DT_flout,float(num_str))
 	def make_letter(self):
	 		str=''
	 		while self.current_char !='&' and self.current_char in letter or self.current_char in digit:
	 			str+=self.current_char
	 			self.advance()
	 		#print(str)	
	 		if str in symboladdop:
	 			return Token(symaddop,str)
	 		if str in symbolmulop:
	 			return Token(symmulop,str)
	 		if str == symeq:
	 			return Token(symequal,str)		
	 		return Token(idf,str)
class BinOpNode:
	def __init__(self,tpe ,left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node
		self.tpe=tpe
	def __repr__(self):
		return f'{self.tpe}({self.left_node}, {self.op_tok}, {self.right_node})'	 		
class Parser:
	def __init__(self,tokens):
		self.tokens=tokens
		self.current_tok=''
		self.tok_idx =-1
		self.AssignmentToken=[]
		self.advance()
	def advance(self):
		self.tok_idx+=1
		#print(self.tok_idx)
		if self.tok_idx<len(self.tokens):
			self.current_tok=self.tokens[self.tok_idx]
		else :self.current_tok=None	
		#print(self.current_tok)
	def factor(self):
		tok =self.current_tok
		if self.current_tok != None and tok.type in(DT_flout,DT_int,idf):
			self.advance()
			
		else :
			tok_error= self.current_tok
			self.advance()
			error=MyError('InvalidSyntaxError','word',tok_error,self.tok_idx)
			return [] ,error.ERRoR()
		return Token(tok.type,tok.value)
	def Term(self):
		left = self.factor()
		while self.current_tok != None and self.current_tok.type is 'symbolmulop':
			tok_op=self.current_tok
			self.advance()
			right=self.factor()
			left = BinOpNode('Term:',left, tok_op, right)	
		return left

	def expression(self):
		left =self.Term()
		#print(self.current_tok)
		list_tok=[]
		tok_op=None
		right=None
		while self.current_tok != None and self.current_tok.type is 'symboladdop':
			tok_op=self.current_tok
			#print(tok_op)
			self.advance()
			right=self.Term()
			left = BinOpNode('expression:',left, tok_op, right)
		return left	
	def Assignment(self):
		if len(self.tokens)<3:
			error=MyError('InvalidSyntaxError','word','error',self.tok_idx)
			self.advance()
			return [] ,error.ERRoR()
		#print(self.tok_idx)	
		if self.current_tok.type!=idf:
			tok_error= self.current_tok

			error=MyError('InvalidSyntaxError','word',tok_error,self.tok_idx)
			self.advance()
			return [] ,error.ERRoR()
		left = self.current_tok
		
		self.advance()
		tok_op = self.current_tok
		#print(self.tok_idx)
		if tok_op.type is symequal:
			self.advance()
		else:
			tok_error= tok_op.type
			error=MyError('InvalidSyntaxError','word',tok_error,self.tok_idx)
			self.advance()
			
			return [] ,error.ERRoR()
		
		right=self.expression()
		left = BinOpNode('Assignment:',left, tok_op, right)
		return left
	def parse(self):
		res=[]
		while(self.current_tok!=None):

			res.append(self.Assignment())
		return(res)
###RUn#####
def run():
	###scanner
	sScaner=Scaner('E:\\aml\\text.py')
	tokens ,erorrs =sScaner.make_token()
	print(tokens)
	print(erorrs)
	if erorrs : return None,erorrs
	##parser
	parser = Parser(tokens)
	ast =parser.parse()
	print(ast)
	
run()		