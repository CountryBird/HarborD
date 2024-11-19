 # -*- coding: utf-8 -*-
import os

def mod_textchange(year,month,day,hour,midValue):
    with open('aermod.inp', 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if i==37:  # STARTEND로 시작하는 줄 찾기
            # 시간 값을 2자리로 맞추기 위해 zfill(2)를 사용
            new_time = str(hour).zfill(2)
            old_time = str(hour - 1).zfill(2) if hour > 1 else "01"  # 처음은 01부터 시작
            
            if not midValue: # 현재시간 - 현재시간
                if hour == 1:
                    content[i] = line.replace(f"23 06 10 01 23 06 10 01", # 하드 코딩값 대체
                                        f"{year} {month} {day} {new_time} {year} {month} {day} {new_time}")
                
                else:
                    content[i] = line.replace(f"{year} {month} {day} {old_time} {year} {month} {day} {new_time}",
                                        f"{year} {month} {day} {new_time} {year} {month} {day} {new_time}")
                    
            else: # 현재시간 - 다음시간
                next_time = str(hour+1).zfill(2)
                content[i] = line.replace(f"{year} {month} {day} {new_time} {year} {month} {day} {new_time}",
                                    f"{year} {month} {day} {new_time} {year} {month} {day} {next_time}")
                
            line = content[i]  # 수정된 줄을 다음 반복에서도 사용하기 위해 갱신
            break

    with open('aermod.inp', 'w') as file:
        file.writelines(content)

def plot_textchange(year,month,day,hour,midValue):
    with open('aerplot.inp', 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if i==117:  # STARTEND로 시작하는 줄 찾기
            # 시간 값을 2자리로 맞추기 위해 zfill(2)를 사용
            new_time = str(hour).zfill(2)
            old_time = str(hour - 1).zfill(2) if hour > 1 else "01"  # 처음은 01부터 시작
            
            if not midValue: # 현재시간 - 현재시간
                if hour == 1: # 하드 코딩값 대체
                    content[i] = line.replace(f"2306100100", f"{year}{month}{day}{new_time}00")
                
                else:
                    content[i] = line.replace(f"{year}{month}{day}{old_time}30", f"{year}{month}{day}{new_time}00")
                    
            else: # 현재시간 - 다음시간
                content[i] = line.replace(f"{year}{month}{day}{new_time}00", f"{year}{month}{day}{new_time}30")
                
            line = content[i]  # 수정된 줄을 다음 반복에서도 사용하기 위해 갱신
            break

    with open('aerplot.inp', 'w') as file:
        file.writelines(content)

def default(year,month,day,hour,original_dir):
    os.chdir("AERMOD")
    with open('aermod.inp', 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if i==37:  # STARTEND로 시작하는 줄 찾기
            # 시간 값을 2자리로 맞추기 위해 zfill(2)를 사용
            new_time = str(hour).zfill(2)
            content[i] = line.replace(f"{year} {month} {day} {new_time} {year} {month} {day} {new_time}",
                                  f"23 06 10 01 23 06 10 01")
            line = content[i]  # 수정된 줄을 다음 반복에서도 사용하기 위해 갱신
            break

    with open('aermod.inp', 'w') as file:
        file.writelines(content)
    os.chdir(original_dir)
    
    os.chdir("AERPLOT")
    
    with open('aerplot.inp', 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if i==117:  # STARTEND로 시작하는 줄 찾기
            # 시간 값을 2자리로 맞추기 위해 zfill(2)를 사용
            new_time = str(hour).zfill(2)
            content[i] = line.replace(f"{year}{month}{day}{new_time}",f"2306100100")
            line = content[i]  # 수정된 줄을 다음 반복에서도 사용하기 위해 갱신
            break

    with open('aerplot.inp', 'w') as file:
        file.writelines(content)

def make_KMZ(year,month,day):
    original_dir = os.getcwd()
    
    for hour in range(1,24):

        os.chdir("AERMOD")
        mod_textchange(year,month,day,hour,False)
        os.system("aermod.exe")
        os.chdir(original_dir)

        os.chdir("AERPLOT")
        plot_textchange(year,month,day,hour,False)
        os.system("aerplot.exe")
        os.chdir(original_dir)
        
        if hour == 23:
            default(year,month,day,hour,original_dir)
        else:
            os.chdir("AERMOD")
            mod_textchange(year,month,day,hour,True)
            os.system("aermod.exe")
            os.chdir(original_dir)

            os.chdir("AERPLOT")
            plot_textchange(year,month,day,hour,True)
            os.system("aerplot.exe")
            os.chdir(original_dir)
            
    os.chdir("..") # 나중에 geojson은 HarborD에 만들기 위해