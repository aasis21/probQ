from probQparser.parser import getSolver
import time
import sys
import os

print('----------------------------------------------------------------------------------')
print('------------------------------ WELCOME TO ProbQ-----------------------------------')
print('----------------------------------------------------------------------------------')

start_time = time.time()
script_dir = os.path.dirname(__file__)
input_file = str(sys.argv[1])
if input_file.split('.')[1] != 'pq':
    print('>>>>>>>>>> wrong file. Please Give a pq file \n')
    exit()
print('>>>>>>>>>> reading source file ' , input_file, '\n')

with open(os.path.join(script_dir, input_file), 'r') as f:
        source = f.read()
if source == '':
    print('>>>>>>>>>> specified file is empty \n')

# get the solver from probQparser
print(">>>>>>>>>> compiling the source ",'\n')
solver  = getSolver(source,0)
code = solver.get_code()
# print('\n',code,'\n')

output_file = input_file.split('.')[0] + '.pl'
print('\n>>>>>>>>>> writing output file ' , output_file, '\n')

with open(output_file, 'w') as problog_file:
    problog_file.write(code)

elapsed_time = time.time() - start_time
print(">>>>>>>>>> Time taken to compile: ", str(elapsed_time), '\n')
print(">>>>>>>>>> Running generated problog code ",'\n')

start_time = time.time()
os.system("problog " + str(output_file))
elapsed_time = time.time() - start_time

print("\n>>>>>>>>>> Total time taken : ", str(elapsed_time), '\n')
