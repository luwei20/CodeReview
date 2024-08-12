import subprocess
import glob
import shutil
import os

root_dir = '/home/lw/ctx/'
gcc_test_suit_dir = root_dir + 'gcc/gcc/testsuite'
llvm_test_suit_dir = root_dir + 'llvm-test-suite'
save_dir = root_dir + '/testcases'


cfiles_gcc = glob.glob(os.path.join(gcc_test_suit_dir, '**', '*.c'), recursive=True)
cfiles_llvm = glob.glob(os.path.join(llvm_test_suit_dir, '**', '*.c'), recursive=True)
cfiles = cfiles_gcc + cfiles_llvm
# cfiles = ['/home/lw/ctx/hello.c']

def compile_and_run(cfile, Olevel):
    exe_file = cfile.replace('.c', f'_{Olevel}')
    compile_cmd =  ['clang', cfile, '-o', exe_file, Olevel]
    try:
        # 编译
        subprocess.run(compile_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        # 运行
        result = subprocess.run([exe_file], capture_output=True, text=True, check=True, timeout=10)
        return result.stdout
    except Exception as e:
        print(e)
        print(f"compile or run error : {cfile}")
        return "error"
    finally:
        # 清理可执行文件
        if os.path.exists(exe_file):
            os.remove(exe_file)

def insert_comment(c_file):
    # 读取文件内容
    with open(cfile, 'r') as f:
        content = f.readlines()
    # 在第一行插入路径注释
    relative_path = c_file.replace(root_dir, '', 1)
    content.insert(0, f"// {relative_path}\n")
    # 将新的内容写回文件
    with open(c_file, 'w') as file:
        file.writelines(content)

cfiles_num = len(cfiles)
cfiles = cfiles[58518:]
cnt = 58518 + 1
name_cnt = 7075
for cfile in cfiles:
    cnt += 1
    print(cfile)
    print(f"{cnt} / {cfiles_num} will be compiled and run")
    results = {}
    # 在五种优化级别下编译运行
    for opt in ['-O0', '-O1', '-O2', '-O3', '-Os']:
        output = compile_and_run(cfile, opt)
        results[opt] = output
    #判断是否保留该cfile
    if "error" not in results.values() and len(set(results.values())) == 1:
        insert_comment(cfile)
        shutil.copy2(cfile, os.path.join(save_dir, f'test-{name_cnt}.c'))
        print(f'test-{name_cnt}.c has been saved')
        name_cnt += 1

