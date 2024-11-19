from make_kmz import make_KMZ
from kmz_parser import parser

year,month,day = input("원하는 년월일 입력(YY MM DD): ").split()

make_KMZ(year,month,day)

for hour in range(1,24):
    parser(year,month,day,str(hour).zfill(2),"00")
    
    if hour != 23: 
        parser(year,month,day,str(hour).zfill(2),"30")