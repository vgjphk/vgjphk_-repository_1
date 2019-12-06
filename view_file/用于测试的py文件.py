# -*- coding:utf-8 -*-
import csv

data = []
with open('D:/py/data.csv') as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    header = next(csv_reader)  # 读取第一行每一列的标题
    for row in csv_reader:  # 将csv 文件中的数据保存到data中
        data.append(row)
    csvfile.close()

# print(data[0][1])
street=[]
streetsign=[]
streetarea=[]
for i in range(len(data)):
    if(data[i][24]!='-'):
        if(data[i][24] not in street):
            street.append(data[i][24])
            streetarea.append([i])
        else:
            for j in range(len(street)):
                if(street[j] == data[i][24]):
                    streetarea[j].append(i)

print(street)

# a =0
# print(streetsign)
# for i in range(len(street)):
#     # print(streetarea[i])
#     a = a+len(streetarea[i])
# print(a)
#
# hood = []
# hoodsign = []
# hoodarea = []
# for i in range(len(streetarea)):
#     # print(streetarea[i])
#     hood.append([])
#     hoodsign.append([])
#     hoodarea.append([])
#     for j in streetarea[i]:
#         if(data[j][15] not in hood[i]):
#             hood[i].append(data[j][15])
#             hoodsign[i].append(data[j][16])
#             hoodarea[i].append([j])
#         else:
#             for k in range(len(hood[i])):
#                 if(hood[i][k] == data[j][15]):
#                     hoodarea[i][k].append(j)
#     # print(hood[i])
#     # print(hoodsign[i])
#
# for i in range(6):
#     print("<select class=\"department\" id=\"iidepartment%d\" onchange=\"fdepartment%d()\" style=\"width:240px\">"%(i+1,i+1))
#     print("    <option>请选择</option>")
#     for j in range(len(hood[i])):
#         print("    <option>%s</option>"%hood[i][j])
#     print("</select>")

# -*- coding:utf-8 -*-
# import csv
#
# data = []
# with open('D:/py/data.csv') as csvfile:
#     csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
#     header = next(csv_reader)  # 读取第一行每一列的标题
#     for row in csv_reader:  # 将csv 文件中的数据保存到data中
#         data.append(row)
#     csvfile.close()
#
# # print(data[0][1])
# types=[]
# typessign=[]
# typesarea=[]
# for i in range(len(data)):
#     if(data[i][9]!='-'):
#         if(data[i][9] not in types):
#             types.append(data[i][9])
#             typessign.append(data[i][10])
#             typesarea.append([i])
#         else:
#             for j in range(len(types)):
#                 if(types[j] == data[i][9]):
#                     typesarea[j].append(i)
#
# # print(types)
# # a =0
# # print(typessign)
# # for i in range(len(types)):
# #     print(typesarea[i])
# #     a = a+len(typesarea[i])
# # print(a)
#
# hood = []
# hoodsign = []
# hoodarea = []
# for i in range(len(typesarea)):
#     hood.append([])
#     hoodsign.append([])
#     hoodarea.append([])
#     for j in typesarea[i]:
#         if(data[j][11] not in hood[i]):
#             hood[i].append(data[j][11])
#             hoodsign[i].append(data[j][12])
#             hoodarea[i].append([j])
#         else:
#             for k in range(len(hood[i])):
#                 if(hood[i][k] == data[j][11]):
#                     hoodarea[i][k].append(j)
#     # print(hood[i])
#     # print(hoodsign[i])
#
# small = []
# smallsign = []
# smallarea = []
# for i in range(len(types)):
#     small.append([])
#     smallsign.append([])
#     smallarea.append([])
#     for j in range(len(hood[i])):
#         small[i].append([])
#         smallarea[i].append([])
#         smallsign[i].append([])
#         for k in hoodarea[i][j]:
#             if data[k][13] not in small[i][j]:
#                 small[i][j].append(data[k][13])
#                 smallsign[i][j].append(data[k][14])
#                 smallarea[i][j].append([k])
#             else:
#                 for m in range(len(small[i][j])):
#                     if data[k][13] == small[i][j][m]:
#                         smallarea[i][j][m].append(k)
# print(small)
# for i in range(len(small)):
#     for j in range(len(small[i])):
#         print(small[i][j])


# print("<input type=\"text\" name=\"tiny_type\"  placeholder=\"请输入大类名称\"/>")
# print("<select class=\"tiny_type\" id=\"iitinytype0\" onchange=\"ftinytype0()\" style=\"width:240px\">")
# print("    <option>请输入小类名称")
# print("</select>")
# for i in range(len(small)):
#     for j in range(len(small[i])):
#         print("<select class=\"tiny_type%d\" id=\"iitinytype%d_%d\" onchange=\"ftinytype%d_%d()\" style=\"width:240px\">"%(i+1,i+1,j+1,i+1,j+1))
#         print("    <option>请选择</option>")
#         for k in range(len(small[i][j])):
#             print("    <option>%s</option>"%small[i][j][k])
#         print("</select>")



# print(len(types))
# for i in range(len(types)):
#     for j in range(len(small[i])):
#         print("function ftinytype%d_%d(){\n    document.getElementById('itinytype').value=document.getElementById('iitinytype%d_%d').value;\n}"%(i+1,j+1,i+1,j+1))

# $("#iibigtype1").change(function(){
#     $("#iibigtype1 option").each(function(i,o){
#         if($(this).attr("selected"))
#         {
#             $(".tiny_type1").hide();
#             $(".tiny_type1").eq(i).show();
#         }
#     });
# });
# $("#iibigtype1").change();

# for i in range(len(types)):
#     print("$(\"#iibigtype%d\").change(function(){"%(i+1))
#     print("    $(\"#iibigtype%d option\").each(function(i,o){"%(i+1))
#     print("        if($(this).attr(\"selected\"))")
#     print("        {")
#     print("            $(\".tiny_type%d\").hide();"%(i+1))
#     print("            $(\".tiny_type%d\").eq(i).show();"%(i+1))
#     print("        }")
#     print("    });")
#     print("});")
#     print("$(\"#iibigtype%d\").change();"%(i+1))