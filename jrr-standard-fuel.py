import gmsh
import sys
import math
import numpy as np

gmsh.initialize()

lc = 0.1
meshname = 'standard-fuel'
gmsh.model.add(meshname)

#set alias, occ & geo
occ_alias = gmsh.model.occ
geo_alias = gmsh.model.geo
alias = geo_alias

#set tag, point, line, curve, surf
pointtag = 0
linetag = 0
curvetag = 0
surftag = 0

#fa = fuel assembly
#length, width, water gap, clad
falength = 7.72
fawidth = 7.72
fawithoutgap = 7.62
watergap = 0.05
boundclad = 0.48

temppoint = 1
startpoint = temppoint
startline = linetag+1
xcoord = [-3.86, -3.81, -3.33, -3.08, 3.08, 3.33, 3.81, 3.86] # 3.08 -> 2.45
yorigin = 3.686
ytopcoord = [3.86, 3.81]
ybotcoord = [-3.81, -3.86]
delty = [0, 0.038, 0.114, 0.152]
count = 0

rowline = []
columnline = []
topdimtag = []
bottomdimtag = []
leftdimtag = []
rightdimtag = []
boundnodetag = []
boundlinetag = []
numpoint_in_x = 0

meshid = 1 # 组件分块用的编号，其中0表示完整组件
numfuelplate = 20 # 20 -> 16
nummeshinfuel = 8
length_of_fuel = 6.16 # 6.16 -> 4.9
meshsize = length_of_fuel/nummeshinfuel #只有fuel！

if meshid in [1,4,7]:
    tempx = xcoord[3] # tempx = -3.08
elif meshid in [2, 5, 8]:
    tempx = xcoord[0] # tempx = -3.86
elif meshid in [3, 6, 9]:
    tempx = xcoord[0] # tempx = -3.86

if meshid == 0: #只有 y = 3.86 和 y = 3.81
    y = 3.86
    for x in xcoord:
        pointtag += 1
        alias.addPoint(x, y, 0, lc, pointtag)
        boundnodetag.append(pointtag) # 识别为边界点boundnode
        numpoint_in_x += 1
        if x != xcoord[0] and x != xcoord[len(xcoord)-1] and y == ytopcoord[0]: # 在ytop，不在xcoord开头结尾
            topdimtag.append([0, pointtag]) # 识别为topdim，顶边，0表示点
        if x == -length_of_fuel/2 and nummeshinfuel > 1: # 燃料边界点，mesh个数 > 1
            for i in range(nummeshinfuel-1):
                x += meshsize
                pointtag += 1 # 调整了一点原代码顺序
                alias.addPoint(x, y, 0, lc, pointtag) # alias = gmsh.model.geo
                boundnodetag.append(pointtag) # 识别为边界点boundnode
                topdimtag.append([0,pointtag]) # 识别为上边界topdim
                numpoint_in_x += 1
    count += 1 # y = 3.86这一行
    y = 3.81
    for x in xcoord:
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1
        if x == -3.86: # 左边界点
            boundnodetag.append(pointtag) # 标记为边界点
            leftdimtag.append([0,pointtag]) # 标记为左边界点
        elif x == 3.86: # 右
            boundnodetag.append(pointtag)
            rightdimtag.append([0,pointtag])
        if x == -length_of_fuel/2 and nummeshinfuel > 1: # 在燃料的左边界且有mesh
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
    count += 1 # y = 3.81

else: # meshid != 0
    for i in range(len(ytopcoord)): # ytopcoord = [3.86, 3.81]
        y = ytopcoord[i]
        numpoint_in_x = 0 # 新的meshid新的计数，相当于pointtag个数
        for j in range(len(xcoord)): # i对应y坐标， j对应x坐标
            x = xcoord[j]
            pointtag += 1
            alias.addPoint(x, y, 0, lc, pointtag)
            numpoint_in_x += 1
            if i == 0: # y = 3.86
                boundnodetag.append(pointtag) #标记边界点
                if j != 0 and j != len(xcoord)-1:
                    topdimtag.append([0,pointtag]) #标记顶边
            elif j == 0: # y != 3.86最左侧
                boundnodetag.append(pointtag) #标记边界点
                leftdimtag.append([0,pointtag]) #标记左边
            elif j == len(xcoord)-1: # y != 3.86最右侧
                boundnodetag.append(pointtag) #标记边界点
                rightdimtag.append([0,pointtag]) #标记右边
            if x ==  tempx and nummeshinfuel > 1: # tempx取决于meshid， ？？？划分燃料？
                for k in range(nummeshinfuel-1):
                    x += meshsize
                    pointtag += 1
                    alias.addPoint(x, y, 0, lc, pointtag)
                    numpoint_in_x += 1
                    if i == 0:
                        boundnodetag.append(pointtag)
                        topdimtag.append([0,pointtag])
        count += 1 # 对每一个y = ytopcoord[i]

for i in range(numfuelplate): # i：燃料盘编号
    for j in delty: # 燃料盘y方向坐标
        for x in xcoord: # 燃料盘x方向坐标
            pointtag += 1
            alias.addPoint(x, yorigin-j, 0, lc, pointtag) #yorigin：第一个燃料盘上边界
            if x == -3.86:
                boundnodetag.append(pointtag) # 标记为边界点
                leftdimtag.append([0,pointtag]) # 标记为左边界
            elif x == 3.86:
                boundnodetag.append(pointtag) # 右
                rightdimtag.append([0,pointtag])
            if x == -3.08 and nummeshinfuel > 1: # 燃料左起始点
                for k in range(nummeshinfuel-1):
                    x += meshsize
                    pointtag += 1
                    alias.addPoint(x, yorigin-j, 0, lc, pointtag)
        count += 1 # 对每一个燃料盘 y
    yorigin -= 0.38 # 两个盘的距离，计算下一个盘

if meshid == 0: #只有 y = -3.86 和 y = -3.81
    for x in xcoord:
        y = -3.81
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1
        if x == -3.86:# 标记边界点
            boundnodetag.append(pointtag)# 标记为边界点
            leftdimtag.append([0,pointtag])# 标记为左边界
        elif x == 3.86:
            boundnodetag.append(pointtag)# 标记为边界点
            rightdimtag.append([0,pointtag])# 标记为右边界
        if x == -3.08 and nummeshinfuel > 1: # mesh燃料
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
    count += 1 # y = -3.81

    for x in xcoord:
        y = -3.86
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1
        boundnodetag.append(pointtag) # 标记边界
        if x != xcoord[0] and x != xcoord[len(xcoord)-1]:
            bottomdimtag.append([0,pointtag]) # 标记底边
        if x == -3.08 and nummeshinfuel > 1: # mesh燃料
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
                boundnodetag.append(pointtag)# 标记为边界点
                bottomdimtag.append([0,pointtag])# 标记为底边界
    count += 1 # y = -3.86

else: # meshid != 0
    for i in range(len(ybotcoord)): # ybotcoord: list[float] = [-3.81, -3.86]
        y = ybotcoord[i]
        for j in range(len(xcoord)):
            x = xcoord[j] # i,j为坐标
            alias.addPoint(x, y, 0, lc, pointtag+1)
            pointtag += 1
            #boundnodetag.append(pointtag) # ？都标记为边界点？这一行注释?
            if i == len(ybotcoord)-1:
                boundnodetag.append(pointtag)
                if j != 0 and j != len(xcoord)-1:
                    bottomdimtag.append([0,pointtag])
            elif j == 0:
                boundnodetag.append(pointtag)
                leftdimtag.append([0,pointtag])
            elif j == len(xcoord)-1:
                boundnodetag.append(pointtag)
                rightdimtag.append([0,pointtag])
            if x == tempx and nummeshinfuel > 1:
                for k in range(nummeshinfuel-1):
                    x += meshsize
                    alias.addPoint(x, y, 0, lc, pointtag+1)
                    pointtag += 1
                    if i == len(ybotcoord) - 1:
                        boundnodetag.append(pointtag)
                        bottomdimtag.append([0,pointtag])
        count += 1 # y = ybotcoord[i]

#按行标记
for i in range(count): #count：（y）3.86、3.81、-3.81、-3.86、每一个燃料盘的y
    temprowline = []
    for k in range(numpoint_in_x-1): #x方向点个数
        alias.addLine(temppoint,temppoint+1,linetag+1) # 添加线
        temppoint += 1
        linetag += 1
        temprowline.append(linetag) # 先放在temprowline
        if i == 0:
            boundlinetag.append(linetag) #边界线
            topdimtag.append([1,linetag]) #顶边线，1表示线
        elif i == count-1:
            boundlinetag.append(linetag) #边界线
            bottomdimtag.append([1,linetag]) #底边线
    temppoint += 1
    rowline.append(temprowline) # temprowline放进rowline

for i in range(numpoint_in_x): #标记列
    temppoint = startpoint + i
    tempcolumnline = []
    for j in range(count-1):
        #print(temppoint)
        alias.addLine(temppoint,temppoint+numpoint_in_x,linetag+1) #这一行到下一行的两个点
        linetag += 1
        tempcolumnline.append(linetag)
        temppoint += numpoint_in_x
        if i == 0:
            boundlinetag.append(linetag) #标记边界线
            leftdimtag.append([1,linetag]) #标记左边界线
        elif i == numpoint_in_x-1:
            boundlinetag.append(linetag) #标记边界线
            rightdimtag.append([1,linetag]) #标记右边界线
    columnline.append(tempcolumnline)

#慢化剂、燃料、包壳表面
modesurf = []
fuelsurf = []
cladsurf = []

templine = startline

for i in range(count-1): #count:行数，按行按列每个矩形都作成CurveLoop,addPlaneSurface
    for j in range(numpoint_in_x-1):#numpoint_in_x:x方向点个数
        templist = []
        templist.append(templine)
        templist.append(templine+j*(count-2)-(numpoint_in_x-2)*i+numpoint_in_x*count-1)
        templist.append(-(templine+numpoint_in_x-1))
        templist.append(-(templine+j*(count-2)-(numpoint_in_x-2)*i+(numpoint_in_x-1)*count))
        # print(templist)
        alias.addCurveLoop(templist, curvetag+1)
        curvetag += 1
        alias.addPlaneSurface([curvetag], surftag+1)
        surftag += 1
        templine += 1

tempsurf = 1
modeytag = []
fuelxtag = []
fuelytag = []
tempmodeytag = 6

for i in range(nummeshinfuel):#标记燃料的x坐标
    fuelxtag.append(4+i)

for i in range(numfuelplate):#标记燃料的y坐标
    fuelytag.append(4+4*i)

for i in range(numfuelplate-1):#标记慢化剂的y坐标
    modeytag.append(tempmodeytag)
    tempmodeytag += 4

for i in range(count-1): #count行数
    for j in range(numpoint_in_x-1): #x坐标数
        if i+1 == 1 or i+1 == count-1: #第一行或倒数第一行，ifelif的顺序从外到内
            modesurf.append(tempsurf) #水隙
        elif j+1 == 1 or j+1 == numpoint_in_x-1: #第一列或倒数第一列
            modesurf.append(tempsurf) #水隙
        elif j+1 == 2 or j+1 == numpoint_in_x-2: #第二列或倒数第二列
            cladsurf.append(tempsurf) #包壳
        elif i+1 == 2 or i+1 == count-2: #第二行或倒数第二行
            modesurf.append(tempsurf) #慢化剂
        elif i+1 in fuelytag and j+1 in fuelxtag: #xy坐标表示fuel
            fuelsurf.append(tempsurf) #燃料
        elif i+1 in modeytag:
            modesurf.append(tempsurf)#慢化剂
        else:
            cladsurf.append(tempsurf)#包壳
        tempsurf += 1

for i in range(len(columnline)):#columnline:列的集合
    for j in range(count-1):#x坐标为j
        line = columnline[i][j] #只有纵向的线段
        gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)# 在曲线标记上设置超限网格约束
        # 输入：tag，numNodes，meshType=“Progression”，coeff=1

for i in range(count): #count行数
    for j in range(numpoint_in_x-1):#numpoint_in_x:x方向点个数
        line = rowline[i][j]#行的集合
        if j == 0:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        elif j == 1:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        elif j == 2:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        # elif j == 4:
        #     gmsh.model.geo.mesh.setTransfiniteCurve(line, 18)
        elif j in [3,3+nummeshinfuel]:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        elif j == 3+nummeshinfuel:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        elif j == 4+nummeshinfuel:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)
        elif j == 5+nummeshinfuel:
            gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)

tempsurf = 1
for i in range(count-1): # count行数
    for j in range(numpoint_in_x-1): # numpoint_in_x:x方向点个数
        gmsh.model.geo.mesh.setTransfiniteSurface(tempsurf, "AlternateLeft") # 在曲面标记上设置超限网格约束
        # Input: tag, arrangement = "Left", cornerTags = []
        tempsurf += 1

alias.synchronize() # 将内置CAD表示与当前Gmsh模型同步

fuelgroup = gmsh.model.addPhysicalGroup(2, fuelsurf, -1)
gmsh.model.setPhysicalName(2, fuelgroup, 'fuel')
cladgroup = gmsh.model.addPhysicalGroup(2, cladsurf, -1)
gmsh.model.setPhysicalName(2, cladgroup, 'clad')
watergroup = gmsh.model.addPhysicalGroup(2, modesurf, -1)
gmsh.model.setPhysicalName(2, watergroup, 'water')

numsurfs = len(fuelsurf)+len(cladsurf)+len(modesurf) #总表面数

matindexofsurf = []
matnameofsurf = []
for i in range(numsurfs):
    physicaltag = gmsh.model.getPhysicalGroupsForEntity(2, i+1) # 从dim和tag获取physical groups的tags
    tempname = gmsh.model.getPhysicalName(2, physicaltag[0]) # tag转换为物理名称
    matindexofsurf.append(int(physicaltag))
    matnameofsurf.append(tempname)

nummix = len(list(set(matindexofsurf))) # 共有123，3种

matindex = []
matname = []

for j in range(nummix):
    for i in range(numsurfs):
        if matindexofsurf[i] == j+1 and j+1 not in matindex: # 标记首次出现的三种材料？确保都出现？
            matindex.append(j+1)
            matname.append(matnameofsurf[i])

tempsurf = 1
for i in range(count-1):
    for j in range(numpoint_in_x-1):
        gmsh.model.mesh.setRecombine(2, tempsurf)
        tempsurf += 1

gmsh.model.mesh.generate(2)
gmshfile = meshname+'.msh'
gmsh.write(gmshfile)

ifdisplay = '1'
if ifdisplay == '1':
    # Launch the GUI to see the results:
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()
gmsh.finalize()

with open(gmshfile, 'r') as obj:
    lines = obj.readlines()
    for linenumber, line in enumerate(lines): # 标记entities、nodes、elements
        temp = line.split()
        if '$Entities' in temp: # 实体
            entityline = linenumber # 记下行号（9）
        if '$EndEntities' in temp:
            endentityline = linenumber
            boundary_linenumber = linenumber - 1
        if '$Nodes' in temp:
            nodeline = linenumber
        if '$Elements' in temp:
            elementline = linenumber
        if '$EndElements' in temp:
            endeleline = linenumber
    num_entities = endentityline - entityline # 实体个数
    num_nodes = int(lines[nodeline + 1].split()[1])   # 节点数？
    num_elements = int(lines[elementline + 1].split()[1]) # element数
    num_entities_block = int(lines[elementline + 1].split()[0])
    templine = nodeline + 2
    nodecoord = []
    coordline = 0
    boundarynode = []
    nodetag = []
    boundaryentity_dimtag = []
    for i in range(num_entities):
        if coordline < elementline - 1:
            temp = lines[templine].split()
            tempentitydim = int(temp[0])
            tempentitytag = int(temp[1])
            tempnumnode = int(temp[3])
            tempnodeline = templine + 1
            for node in range(tempnumnode):
                tempnodetag = lines[tempnodeline].split()[0]
                nodetag.append(tempnodetag)
                if tempentitydim == 0 and tempentitytag in boundnodetag:
                    boundaryentity_dimtag.append([tempentitydim, tempentitytag])
                    boundarynode.append(tempnodetag)
                if tempentitydim == 1 and tempentitytag in boundlinetag:
                    boundaryentity_dimtag.append([tempentitydim, tempentitytag])
                    boundarynode.append(tempnodetag)
                tempnodeline += 1
            coordline = templine + tempnumnode + 1
            for j in range(tempnumnode):
                tempcoord = lines[coordline].split()
                nodecoord.append(tempcoord[:2])
                coordline += 1
            templine = coordline
    templine = elementline + 2
    node_in_element = []
    element_type_index = []
    mat_index = []
    elementtag = []
    ele_to_bureg = []