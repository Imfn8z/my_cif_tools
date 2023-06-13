import os
from multiprocessing import Pool
from pymatgen.io.cif import CifParser
from pymatgen.core import Structure
import shutil
import warnings
warnings.filterwarnings("ignore")

'''
这个脚本的功能是从一个文件夹中读取所有的CIF文件，然后计算每个CIF文件中所有原子之间的距离，
如果所有原子之间的距离都大于一个阈值，那么就把这个CIF文件复制到另一个文件夹中。具体步骤为：
1. 读取CIF文件
2. 计算所有原子之间的距离
3. 如果所有原子之间的距离都大于阈值，那么就把这个CIF文件复制到另一个文件夹中
'''

# 设定距离阈值，如果原子间的距离大于这个值才会被复制到新文件夹中
distance_threshold = 1.0 

# 输入和输出路径
input_dir = ''
output_dir = ''

def process_file(filename):
    if filename.endswith(".cif"):
        file_path = os.path.join(input_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, filename)

        # 使用Pymatgen库读取CIF文件
        parser = CifParser(file_path)
        structure = parser.get_structures()[0]

        flag = False
        # 计算所有原子间的距离
        for i in range(len(structure)):
            for j in range(i+1, len(structure)):
                if structure.get_distance(i, j) < distance_threshold:
                    flag = True
                    break
            if flag:
                break

        if not flag:
            
            shutil.copy2(file_path, output_file_path)
            #print(file_path)
            output_file_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))])
            print(f"Number of files in the output directory: {output_file_count}")

# 使用Pool来创建多个进程，进程数量默认为CPU的核心数
with Pool() as p:
    file_list = [f for f in os.listdir(input_dir) if f.endswith('.cif')]
    p.map(process_file, file_list)


