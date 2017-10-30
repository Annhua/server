import xlrd
import xlwt

MyWorkbook=xlrd.open_workbook('yy.xlsx')
mySheets=MyWorkbook.sheets()
mySheet=mySheets[0]

myRowValues = mySheet.row_values(0)
# print(myRowValues)
nrows=mySheet.nrows #获取行数
ncols = mySheet.ncols#获取列数

for i in range(nrows):
    # print(i)
    for j in range(1,ncols):
        # print(j)
        v0=mySheet.cell_value(i, j-1)
        v1= mySheet.cell_value(i, j)
        # print(v0)
        book={}
        book[v0]=v1
        print(book)


# list=[]
# for i in range(1,nrows):
#     # print(i)
#     new=mySheet.row_values(i)
#     book={}
#     for j in range(len(myRowValues)):
#         book[myRowValues[j]]=new[j]
#     list.append(book)
# print(list)


myWorkbook=xlwt.Workbook()
mySheet = myWorkbook.add_sheet('A Test Sheet')





