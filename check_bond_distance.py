import os
import shutil
from tqdm import tqdm


metal_emelent = ['Mg', 'Al', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Sr', 'Y', 'Zr', 'Nb', 'Mo',
                 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Ba', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
                 'Pb', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'U']

'''
这个脚本用于检查键长是否符合要求，如果符合要求则复制到新的文件夹中，检查方式为：
1. 读取cif文件中的键长信息，如果键长大于max_bond_length或者小于min_bond_length则不符合要求
2. 如果键长符合要求，则检查键中是否含有金属元素，如果含有金属元素则不符合要求
3. 如果键长符合要求，且键中不含有金属元素，则复制到新的文件夹中
'''


def check_and_copy_files(input_folder, output_folder, max_bond_length):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in tqdm(os.listdir(input_folder), desc="Processing files"):
        if filename.endswith(".cif"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as cif_file:
                lines = cif_file.readlines()

            check_bond = False
            for line in lines:
                if "_ccdc_geom_bond_type" in line:
                    check_bond = True
                    continue

                if check_bond:
                    if any(metal in line for metal in metal_emelent):
                        continue

                    bond_length = float(line.split()[2])
                    if bond_length > max_bond_length or bond_length < min_bond_length:
                        check_bond = False
                        break

            if check_bond:
                shutil.copy(file_path, output_folder)


# 请在此替换输入输出文件夹路径
input_folder = ""
output_folder = ""

max_bond_length = 2.466  # 最大键长值
min_bond_length = 1.0  # 最小键长值


print("Input folder: ", input_folder)
print("Output folder: ", output_folder)
print("Max bond length: ", max_bond_length)
print("Min bond length: ", min_bond_length)
check_and_copy_files(input_folder, output_folder, max_bond_length)
print("Done!")
