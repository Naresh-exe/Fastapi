import csv

def gen(batch):
    for i in batch:
        company=i[0]
        industry=i[1]
        title=i[2]
        country=i[3]
        print(company,industry,title,country)
with open("summary.csv","r") as f:
    reader=csv.reader(f)
    data=list(reader)
    e=data[1:]
    BATCHSIZE=5
    for row in range(0,len(e),BATCHSIZE):
        print(row)
        batch=e[row:row+BATCHSIZE]
        print(batch)
        gen(batch)
