import pymysql
import  re 

f = open("dict.txt")
db = pymysql.connect('localhost','root','123456','yydict')

cursor = db.cursor()

for line in f:
    try:
        line = f.readline()
        result = re.split(r'\s+',line)
        obj = re.match(r'([-a-zA-Z]+)\s+(.+)',line)
        word = obj.group(1)
        mean = obj.group(2)
        sql = "insert into words (word,mean) values ('%s','%s')"%(word,mean)
    except:
        continue
    try:
        cursor.execute(sql)
        db.commit()
        print('ok')
    except Exception as e:
        print(e)
        db.rollback()

cursor.close()
db.close()
f.close()