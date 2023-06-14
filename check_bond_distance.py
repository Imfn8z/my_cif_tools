import os
import shutil
from tqdm import tqdm


metal_emelent = ['Mg', 'Al', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Sr', 'Y', 'Zr', 'Nb', 'Mo',
                 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Ba', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
                 'Pb', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'U']
metal_patterns = [re.compile(metal) for metal in metal_elements]
'''
这个脚本用于检查键长是否符合要求，如果符合要求则复制到新的文件夹中，判断规则为：
1. 读取cif文件中的键长信息，如果键长大于max_bond_length或者小于min_bond_length则不符合要求
2. 如果两个原子为金属元素，则使用单独的判据判定（1.0-3.0）
'''


def check_and_copy_files(input_folder, output_folder, max_bond_length, min_bond_length):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in tqdm(os.listdir(input_folder), desc="Processing files"):

        if filename.endswith(".cif"):
            if 'FAILED' in filename:
                continue

            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as cif_file:
                lines = cif_file.readlines()

            check_bond = False

            for line in lines:
                if "_ccdc_geom_bond_type" in line:
                    check_bond = True
                    continue
                    
                if check_bond :
                    parts = line.split()
                    atom1, atom2 = parts[0], parts[1]

                    if all(any(pattern.match(atom) for pattern in metal_patterns) for atom in [atom1, atom2]):
                        bond_length = float(parts[2])
                        #print(line)
                        #print(bond_length)
                        if bond_length < 1.0 or bond_length > 3.0: # 这里是排除了金属-金属间的键，按1-3.0A的范围排除
                            check_bond = False
                            break
                        else:
                            continue

                    bond_length = float(parts[2])
                    if bond_length > max_bond_length or bond_length < min_bond_length:
                        check_bond = False
                        break

            if check_bond:     
                shutil.copy(file_path, output_folder)

#在这里替换输入和输出文件夹的绝对路径
input_folder = "/home/huangbo/v230603/outputs/20230607_162900_bonds_1-2.466_atoms_1.0/"
output_folder = "/home/huangbo/v230603/outputs/20230607_162900_bonds_1-2.466_atoms_1.0_metal_1-3.0/"


max_bond_length = 2.466  # 最大键长值
min_bond_length = 1.0  # 最小键长值
print("Max bond length: ", max_bond_length)
print("Min bond length: ", min_bond_length)

check_and_copy_files(input_folder, output_folder, max_bond_length, min_bond_length)
print("Done!")
print(len)
