from probQparser.parser import *
import time
import sys
import os

print('----------------------------------------------------------------------------------')
print('------------------------------- WELCOME TO ProbQ-----------------------------------')
print('----------------------------------------------------------------------------------')

start_time = time.time()
script_dir = os.path.dirname(__file__)
print(script_dir)
input_file = str(sys.argv[1])
if input_file.split('.')[1] != 'pq':
    print('wrong file. Please Give a pq file')
    exit()
print('>>>>>>>>>> reading source file ' , input_file)
with open(os.path.join(script_dir, input_file), 'r') as f:
        source = f.read()
if source == '':
    print('EMPTY FILE')
print('----------------------------------------------------------------------------------')
#print(source)
parse(source,0)                                                                             #call parser 
print('----------------------------------------------------------------------------------')
print('------------------------------- PROBLOG CODE--------------------------------------')
print('----------------------------------------------------------------------------------')
code = solver.get_code()                                                                    #call solver
#print(code)                                                                                 #print ProbLogCode

output_file = input_file.split('.')[0] + '.pl'
print('\n>>>>>>>>>> writing output file ' , output_file)
with open(output_file, 'w') as problog_file:    
    problog_file.write(code)                                                                

elapsed_time = time.time() - start_time 
print(">>>>>>>>>> Time taken to compile: ", str(elapsed_time))
print('----------------------------------------------------------------------------------')
print('-------------------------------RUNNING PROBLOG CODE--------------------------------')
print('----------------------------------------------------------------------------------\n \n')
start_time = time.time()
print('----------------------------------------------------------------------------------')
print('--------------------------------------ANSWER--------------------------------------')
print('----------------------------------------------------------------------------------\n')
os.system("problog " + str(output_file))                                                    
elapsed_time = time.time() - start_time                                                     #time taken
print('\n----------------------------------------------------------------------------------')
print('--------------------------------------ANSWER--------------------------------------')
print('----------------------------------------------------------------------------------\n \n')
print("\nTotal time elapsed : ", str(elapsed_time))
