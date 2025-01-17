from cProfile import label
from collections import Counter
from datetime import datetime, timedelta
from math import comb
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn import impute
import pyfiglet
import os
import shutil
import xlsxwriter
import glob
import sys
from zipfile import ZipFile
import time
from tqdm import tqdm


timstr = datetime.now()
yestr = datetime.now() - timedelta(1)
preyestr = datetime.now() - timedelta(2)


timstr_d = timstr.strftime('%d')
timstr_m = timstr.strftime('%m')
timstr_y = timstr.strftime('%Y')

yestr_d = yestr.strftime('%d')
yestr_m = yestr.strftime('%m')
yestr_y = yestr.strftime('%Y')

preyestr_d = preyestr.strftime('%d')
preyestr_m = preyestr.strftime('%m')
preyestr_y = preyestr.strftime('%Y')



R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'


splitter = '-'*70
split_sec = ' '

def ban():

    print(f'''{G + pyfiglet.figlet_format("Efficiency") + R}
{splitter + W}''')


def lister():
    print(C + f'''    
    1. Scatter data
    2. Baseline check
    3. Data scatter + Baseline 
    4. Excel generator
    5. Excel super stream
    6. final export
    0. Exit
{R + splitter}''' + W)


def curve_func(x, a, b, c, d, e):
    return a/(b*x**3+c*x**2+d*x+e)


if __name__ == '__main__':



    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        ban()

        lister()

        hourly = list(range(0, 24))

        user = 'Retr0'  # change it to yours

        deskdir = fr'C:\Users\{user}\Desktop'

        file_directory = fr'{deskdir}\Eff_n'

        userArg = input('Enter Argument : ')

        match userArg:

            case '1':      

                os.chdir(file_directory)

                for item in hourly:

                    try:

                        print(f"")

                        df_hu = pd.read_excel(f'netpara.xlsx', sheet_name = f'{item}')
                    

                        x_data = df_hu[['User_MHZ']]
                        y_data = df_hu[['DL_User_Throughput']]
                        

                        x_data = np.asanyarray(x_data)
                        y_data = np.asanyarray(y_data)


                        x_data = x_data.flatten()
                        y_data = y_data.flatten()

                        y_data = np.nan_to_num(y_data)

                        print(not np.isnan(x_data).any())
                        print(not np.isnan(y_data).any())
                        print(not np.isinf(x_data).any())
                        print(not np.isinf(y_data).any())

                        x_data = np.nan_to_num(x_data)

                        plt.style.use('dark_background')
                        plt.scatter(x_data, y_data, color='blue',
                                label=f'Hour_{item}_samples')
                        plt.xlabel(f'hour {item}')
                        plt.ylabel('user_throughput')
                        plt.grid(True)
                        plt.legend()
                        plt.show()

                    except(TypeError, KeyError,RuntimeError, ValueError):

                        continue

            case '2':     

                os.chdir(file_directory)

                for item in hourly:

                    try:


                        df_hu = pd.read_excel(f'netpara.xlsx', sheet_name = f'{item}')
                    

                        x_data = df_hu[['User_MHZ']]
                        y_data = df_hu[['DL_User_Throughput']]


                        x_data = np.asanyarray(x_data)
                        y_data = np.asanyarray(y_data)

                        x_data = x_data.flatten()
                        y_data = y_data.flatten()

                        y_data = np.nan_to_num(y_data)
                        x_data = np.nan_to_num(x_data)

                        popt, _ = curve_fit(curve_func, x_data, y_data, maxfev = 10000)

                        a, b, c, d, e = popt

                        x_line = np.arange(min(x_data), max(x_data), 1)
                        y_line = curve_func(x_line, a, b, c, d, e)


                        final = 'y=%.5f/%.5f*x+%.5f*x^2+%.5f*x^3+%.5f' % (
                            a, d, c, b, e)

                        print(f'eq_{item}: {final}')

                        print(f'''----------- coeficients
                        {round(a, 5)}
                        {round(b, 5)}
                        {round(c, 5)}
                        {round(d, 5)}
                        {round(e, 5)}
                        ---------------------''')

                        plt.style.use('dark_background')
                        plt.plot(x_line, y_line, '--', color='red',
                            label=f'Baseline_{item}', linewidth=4)
                        plt.xlabel(f'hour {item}')
                        plt.ylabel('baseline')
                        plt.grid(True)
                        plt.legend()
                        plt.show()

                    except(KeyError, TypeError, RuntimeError, ValueError):

                        print(R + f'data ignored : {item}' + W)

                        continue                 
                    
            case '3':       

                os.chdir(file_directory)

                for item in hourly:

                    try:


                        df_hu = pd.read_excel(f'netpara.xlsx', sheet_name = f'{item}')
                    

                        x_data = df_hu[['User_MHZ']]
                        y_data = df_hu[['DL_User_Throughput']]


                        x_data = np.asanyarray(x_data)
                        y_data = np.asanyarray(y_data)

                        x_data = x_data.flatten()
                        y_data = y_data.flatten()

                        y_data = np.nan_to_num(y_data)

                        

                        x_data = np.nan_to_num(x_data)

                        popt, _ = curve_fit(curve_func, x_data, y_data, maxfev=10000)

                        a, b, c, d, e = popt

                        x_line = np.arange(min(x_data), max(x_data), 1)
                        y_line = curve_func(x_line, a, b, c, d, e)

                        plt.style.use('dark_background')
                        plt.scatter(x_data, y_data, color='blue',
                                    label=f'data_{item}')
                        plt.plot(x_line, y_line, '--', color='red',
                                label=f'Baseline_{item}', linewidth=4)
                        plt.grid(True)
                        plt.legend()
                        plt.show()

                    except(KeyError, TypeError, RuntimeError, ValueError):

                        print(R + f'data ignored : {item}' + W)

                        continue
                    
            case '4':         

                os.chdir(file_directory)

                data_source = fr'{file_directory}\netpara.xlsx'

                for item in hourly:

                    try:

                        os.makedirs(fr'{file_directory}/{item}')
                        data_dest = fr'{file_directory}\{item}\netpara.xlsx'


                        shutil.copyfile(data_source, data_dest)

                        os.chdir(fr'{file_directory}\{item}')

                        df_hu = pd.read_excel(f'netpara.xlsx', sheet_name = f'{item}')
                    

                        x_data = df_hu[['User_MHZ']]
                        y_data = df_hu[['DL_User_Throughput']]
                        index_data = df_hu[['INDEX']]
                        pro_data = df_hu[['PRO']]
                        sec_data = df_hu[['SECTOR']]
                    

                        x_data = np.asanyarray(x_data)
                        y_data = np.asanyarray(y_data)
                        pro_data = np.asanyarray(pro_data)
                        sec_data = np.asanyarray(sec_data)
                        index_data = np.asanyarray(index_data)
                    

                        x_data = x_data.flatten()
                        y_data = y_data.flatten()
                        pro_data = pro_data.flatten()
                        sec_data = sec_data.flatten()
                        index_data = index_data.flatten()

                        

                        x_data = np.nan_to_num(x_data)
                        y_data = np.nan_to_num(y_data)

                        x_data = list(x_data)
                        y_data = list(y_data)
                        pro_data = list(pro_data)
                        sec_data = list(sec_data)
                        index_data = list(index_data)
                    

                        popt, xamarin = curve_fit(curve_func, x_data, y_data, maxfev = 10000)
                        a, b, c, d, e = popt

                        x_line = np.arange(min(x_data), max(x_data), 1)
                        y_line = curve_func(x_line, a, b, c, d, e)


                        final = 'y=%.5f/%.5f*x+%.5f*x^2+%.5f*x^3+%.5f' % (
                            a, d, c, b, e)

                        print(f'eq_{item}: {final}')

                        genix = f''' {final}
                        a = {round(a, 5)} : Numerator
                        b = {round(b, 5)} : Coef X^3
                        c = {round(c, 5)} : Coef X^2
                        d = {round(d, 5)} : Coef X
                        e = {round(e, 5)} : fixed 
                        '''

                        with open(f'eq_{item}.txt', 'a') as equ:

                            equ.write(genix)

                        print(f'''----------- coeficients
                        {round(a, 5)}
                        {round(b, 5)}
                        {round(c, 5)}
                        {round(d, 5)}
                        {round(e, 5)}
                        ---------------------''')

                        n_a = round(a, 5)
                        n_b = round(b, 5)
                        n_c = round(c, 5)
                        n_d = round(d, 5)
                        n_e = round(e, 5)

                        province_list = [
                        'PROVINCE(0)',
                        'PROVINCE(1)',
                        'PROVINCE(2)',
                        'PROVINCE(3)',
                        'PROVINCE(4)',
                        'PROVINCE(5)',
                        'PROVINCE(6)',
                        'PROVINCE(7)',
                        'PROVINCE(8)',
                        'PROVINCE(9)',
                        'PROVINCE(10)',
                        'PROVINCE(11)',
                        'PROVINCE(12)',
                        'PROVINCE(13)',
                        'PROVINCE(14)',
                        'PROVINCE(15)',
                        'PROVINCE(16)',
                        'PROVINCE(17)']

                        for z in range(len(province_list)):

                            x2 = []
                            y2 = []
                            AG_sector = []
                            

                            for i in range(len(pro_data)):

                                if pro_data[i] == province_list[z]:

                                    x2.append(x_data[i])
                                    y2.append(y_data[i])
                                    AG_sector.append(sec_data[i])
                                    

                            
                            plt.scatter(x2, y2, color = 'yellow')

                            # -------------------------------- worst cells

                            x3 = []
                            y3 = []
                            AG_worst = []
                            pro_worst = []
                            pro_good = []
                            index_worst = []

                            
                            pro_main = []



                            list_status = []

                            bh = []


                            for i in range(len(pro_data)):
                                if pro_data[i] == province_list[z]:

                                    if y_data[i] < n_a / (n_d * x_data[i] + n_c * (x_data[i] ** 2) + n_b * (x_data[i] ** 3) + n_e):

                                        AG_worst.append(sec_data[i])
                                        x3.append(x_data[i])
                                        y3.append(y_data[i])
                                        index_worst.append(index_data[i])
                                        pro_worst.append(pro_data[i])
                                        pro_main.append(pro_data[i])
                                        list_status.append("WORST")
                                        bh.append(f"BH Time [{item}]")

                                
                                    elif y_data[i] > n_a / (n_d * x_data[i] + n_c * (x_data[i] ** 2) + n_b * (x_data[i] ** 3) + n_e):

                                        AG_worst.append(sec_data[i])
                                        x3.append(x_data[i])
                                        y3.append(y_data[i])
                                        pro_good.append(pro_data[i])
                                        pro_main.append(pro_data[i])
                                        index_worst.append(index_data[i])
                                        list_status.append("GOOD")
                                        bh.append(f"BH Time [{item}]")

                                        
                            print(R + f'province :' + W + f'{dict(Counter(pro_worst))}')
                            print(G + f'province :' + W + f'{dict(Counter(pro_good))}')
                            # print(len(AG_worst))
                            plt.scatter(x3, y3, color = 'red')
                            # plt.scatter(x4, y4, color = 'blue')

                            plt.plot(x_line, y_line, '--', color='green',
                             label=f'Baseline_{item}', linewidth=4)
                            
                            

                            diff_worst = []

                            # diff_good = []
                            

                            for i in range(len(AG_worst)):


                                diff_worst.append(y3[i] - (n_a / (n_d * x3[i] + n_c * (x3[i] ** 2) + n_b * (x3[i] ** 3) + n_e)))

                            
                            os.chdir(fr'{file_directory}\{item}')

                            outWorkbook1 = xlsxwriter.Workbook(str(province_list[z])+f"_{item}.xlsx")
                            outSheet1 = outWorkbook1.add_worksheet()

                            outSheet1.write("A1", "CELLS")
                            outSheet1.write(0, 0, "SECTORS")
                            # outSheet1.write(0, 0, "Worst SECTORS")
                            outSheet1.write(0, 1, "province")
                            outSheet1.write(0, 2, "BH time")
                            outSheet1.write(0, 3, "User per MHz")
                            outSheet1.write(0, 4, "User throughput")
                            outSheet1.write(0, 5, "DISTANCE TO EXPECTED THROUGHPUT")
                            outSheet1.write(0, 6, "STATUS")
                            outSheet1.write(0, 7, "Index")

    
                            for k in range(len(AG_worst)):
                                outSheet1.write(k + 1, 0, AG_worst[k])
                            for p in range(len(pro_main)):
                                outSheet1.write(p + 1, 1, pro_main[p])
                            for q in range(len(bh)):
                                outSheet1.write(q + 1, 2, bh[q])
                            for j in range(len(x3)):
                                outSheet1.write(j + 1, 3, x3[j])
                            for k in range(len(y3)):
                                outSheet1.write(k + 1, 4, y3[k])
                            for m in range(len(diff_worst)):
                                outSheet1.write(m + 1, 5, diff_worst[m])
                            for o in range(len(list_status)):
                                outSheet1.write(o + 1, 6, list_status[o])
                            for s in range(len(index_worst)):
                                outSheet1.write(s + 1, 7, index_worst[s])
                            outWorkbook1.close()
# ----------------------------------------------------------------------------------------------------------------

                        #     plt.style.use('bmh')

                        # plt.show()
                        
                        os.chdir(fr'{file_directory}\{item}')
                        outWorkbook2 = xlsxwriter.Workbook(f"2_Baseline_CELLS_{item}.xlsx")
                        outSheet2 = outWorkbook2.add_worksheet()
                        outSheet2.write(0, 0, "BH time")
                        outSheet2.write(0, 1, "X")
                        outSheet2.write(0, 2, "Y")
                        for k in range(len(x_line)):
                            outSheet2.write(k+1,0, f"BH Time [{item}]")
                        for k in range(len(x_line)):
                            outSheet2.write(k+1,1, x_line[k])
                        for k in range(len(y_line)):
                            outSheet2.write(k+1,2, y_line[k])
                        outWorkbook2.close()


                    except(TypeError, KeyError, RuntimeError, ValueError):

                        print(R + f'data folder ignored : {item}' + W)

                        continue  

            case '5':

                os.chdir(fr'{file_directory}')

                os.makedirs(fr'{file_directory}/Baselines')

                os.makedirs(fr'{file_directory}/final_data')

                for item in hourly:

                    try:

                        destination = fr'{file_directory}\{item}'

                        os.chdir(destination)

                        os.system(fr'rm netpara.xlsx')

                        excel_list_refrence = [
                            f'PROVINCE(0)_{item}.xlsx',
                            f'PROVINCE(1)_{item}.xlsx',
                            f'PROVINCE(2)_{item}.xlsx',
                            f'PROVINCE(3)_{item}.xlsx',
                            f'PROVINCE(4)_{item}.xlsx',
                            f'PROVINCE(5)_{item}.xlsx',
                            f'PROVINCE(6)_{item}.xlsx',
                            f'PROVINCE(7)_{item}.xlsx',
                            f'PROVINCE(8)_{item}.xlsx',
                            f'PROVINCE(9)_{item}.xlsx',
                            f'PROVINCE(10)_{item}.xlsx',
                            f'PROVINCE(11)_{item}.xlsx',
                            f'PROVINCE(12)_{item}.xlsx',
                            f'PROVINCE(13)_{item}.xlsx',
                            f'PROVINCE(14)_{item}.xlsx',
                            f'PROVINCE(15)_{item}.xlsx',
                            f'PROVINCE(16)_{item}.xlsx',
                            f'PROVINCE(17)_{item}.xlsx'
                        ]

                        emp = []

                        for file in os.listdir(destination):

                            if file in excel_list_refrence:

                                emp.append(file)

                            else:

                                continue    


                        excels = [pd.ExcelFile(name) for name in emp]

                        frames = [x.parse(x.sheet_names[0],header = None, index_col=None) for x in excels]

                        frames[1:] = [df[1:] for df in frames[1:]]

                        combined = pd.concat(frames)

                        combined.to_excel(f"final_data_{item}.xlsx", header=False, index=False)
                    
                        base_source = fr'{file_directory}\{item}\2_Baseline_CELLS_{item}.xlsx'

                        base_destin = fr'{file_directory}\Baselines'

                        shutil.move(base_source, base_destin)

                        final_source = fr'{file_directory}\{item}\final_data_{item}.xlsx'

                        final_destination = fr'{file_directory}\final_data'

                        shutil.move(final_source, final_destination)

                        eq_source = fr'{file_directory}\{item}\eq_{item}.txt'

                        eq_destination = fr'{file_directory}\Baselines'

                        shutil.move(eq_source, eq_destination)

                    except(TypeError, KeyError, RuntimeError, ValueError):

                        continue

            case '6':

                conat_file_destin = fr'{file_directory}\final_data'
 

                file_list = glob.glob(conat_file_destin + "/*.xlsx")
                

                excl_list = []
                
                for file in file_list:
                    excl_list.append(pd.read_excel(file))
                

                excl_merged = pd.DataFrame()
                    
                
                excl_merged = pd.concat(
                    excl_list, ignore_index=True)

                excl_merged.to_excel('report_data_generation.xlsx', index=False)

                
            case '0': 

                sys.exit()
