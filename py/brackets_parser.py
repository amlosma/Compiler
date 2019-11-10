##assigment_2_compilr
# - match with =
#$ match with  #
# % match with ^
#~ match with !

lift_stack  = ['(','{','[','$','%','~','-','*','<','/']
right_stack = [')','}',']','#','^','!','=','+','>','\\']
input = input('your string ')
mystack=[]
for char in input:
        if char in lift_stack:
                mystack.append(char)
              #  print (len(mystack))
        elif char in right_stack:
                if not mystack :
                        print('the string is not correct ^^')
                        exit()
                    
                else :
                        symbol = mystack.pop()
                        if ( lift_stack.index(symbol) == right_stack.index(char) ):
                                continue
                        else:
                                print('the string is not correct ^^')
                                exit()
                        
                        


if not mystack:
        print('the string correct ^_^ ')
else:
        print('the string is not correct ^^')
      

