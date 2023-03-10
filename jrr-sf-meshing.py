import gmsh
import math
import sys
import numpy as np

inputfile = 'ini_jrr_input'

# If sys.argv is passed to gmsh.initialize(), Gmsh will parse the command line
# in the same way as the standalone Gmsh app:
meshname = 'JRR_SF'
lc = 3

gmsh.initialize(sys.argv)
gmsh.model.add(meshname)
occ_alias = gmsh.model.occ
geo_alias = gmsh.model.geo
alias = geo_alias

pointtag = 0
linetag = 0
curvetag = 0
surftag = 0

falength = 7.72
fawidth = 7.72
fawithoutgap = 7.62
watergap = 0.05
boundclad = 0.48

temppoint = 1
startpoint = temppoint
startline = linetag+1
xcoord0 = [-3.86, -3.81, -3.33, -3.08, 3.08, 3.33, 3.81, 3.86]
xcoord1 = [-0.965, -0.915, -0.435, -0.185, 0.965]
xcoord2 = [-0.965, 0.965]
xcoord3 = [-0.965, 0.185, 0.435, 0.915, 0.965]
yorigin0 = 3.686
yorigin1 = 0.806
yorigin2 = 0.836
yorigin3 = 0.866
ytopcoord0 = [3.86, 3.81]
ytopcoord1 = [0.98, 0.93]
ytopcoord2 = [0.95]
ytopcoord3 = [0.98]
ybotcoord0 = [-3.81, -3.86]
ybotcoord1 = [-0.98]
ybotcoord2 = [-0.95]
ybotcoord3 = [-0.93, -0.98]
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

meshid = 0
xcoord = xcoord0[:]
ytopcoord = ytopcoord0[:]
ybotcoord = ybotcoord0[:]
yorigin = yorigin0
numfuelplate = 20
nummeshinfuel = 8
length_of_fuel = 6.16
meshsize = length_of_fuel/nummeshinfuel
# meshname = meshname + str(meshid)

if meshid in [1, 4, 7]:
    tempx = xcoord[3]  
elif meshid in [2, 5, 8]:
    tempx = xcoord[0]
elif meshid in [3, 6, 9]:
    tempx = xcoord[0]

if meshid == 0:
    for x in xcoord:
        y = 3.86
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1
        boundnodetag.append(pointtag)
        numpoint_in_x += 1
        if x != xcoord[0] and x != xcoord[len(xcoord)-1] and y == ytopcoord[0]:
            topdimtag.append([0, pointtag])
        if x == -length_of_fuel/2 and nummeshinfuel > 1:
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
                boundnodetag.append(pointtag)
                topdimtag.append([0, pointtag])
                numpoint_in_x += 1
    count += 1
    for x in xcoord:
        y = 3.81
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1   
        if x == -3.86:
            boundnodetag.append(pointtag)
            leftdimtag.append([0, pointtag])
        elif x == 3.86:
            boundnodetag.append(pointtag)
            rightdimtag.append([0, pointtag])
        if x == -length_of_fuel/2 and nummeshinfuel > 1:
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
    count += 1
else:
    for i in range(len(ytopcoord)):
        y = ytopcoord[i]
        numpoint_in_x = 0
        for j in range(len(xcoord)):
            x = xcoord[j]
            alias.addPoint(x, y, 0, lc, pointtag+1)
            pointtag += 1
            numpoint_in_x += 1
            if i == 0:
                boundnodetag.append(pointtag)
                if j != 0 and j != len(xcoord)-1:
                    topdimtag.append([0, pointtag])
            elif j == 0:
                boundnodetag.append(pointtag)
                leftdimtag.append([0, pointtag])
            elif j == len(xcoord)-1:
                boundnodetag.append(pointtag)
                rightdimtag.append([0, pointtag])
            if x == tempx and nummeshinfuel > 1:
                for k in range(nummeshinfuel-1):
                    x += meshsize
                    alias.addPoint(x, y, 0, lc, pointtag+1)
                    pointtag += 1
                    numpoint_in_x += 1
                    if i == 0:
                        boundnodetag.append(pointtag)
                        topdimtag.append([0,pointtag])
        count += 1

for i in range(numfuelplate):
    for j in delty:
        for x in xcoord:
            alias.addPoint(x, yorigin-j, 0, lc, pointtag+1)
            pointtag += 1
            if x == -3.86:
                boundnodetag.append(pointtag)
                leftdimtag.append([0,pointtag])
            elif x == 3.86:
                boundnodetag.append(pointtag)
                rightdimtag.append([0,pointtag])
            if x == -3.08 and nummeshinfuel > 1:
                for k in range(nummeshinfuel-1):
                    x += meshsize
                    alias.addPoint(x, yorigin-j, 0, lc, pointtag+1)
                    pointtag += 1
        count += 1
    yorigin -= 0.38

if meshid == 0:
    for x in xcoord:
        y = -3.81
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1
        if x == -3.86:
            boundnodetag.append(pointtag)
            leftdimtag.append([0,pointtag])
        elif x == 3.86:
            boundnodetag.append(pointtag)
            rightdimtag.append([0,pointtag])  
        if x == -3.08 and nummeshinfuel > 1:
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
    count += 1

    for x in xcoord:
        y = -3.86
        alias.addPoint(x, y, 0, lc, pointtag+1)
        pointtag += 1 
        boundnodetag.append(pointtag)
        if x != xcoord[0] and x != xcoord[len(xcoord)-1]:
            bottomdimtag.append([0,pointtag])
        if x == -3.08 and nummeshinfuel > 1:
            for i in range(nummeshinfuel-1):
                x += meshsize
                alias.addPoint(x, y, 0, lc, pointtag+1)
                pointtag += 1
                boundnodetag.append(pointtag)
                bottomdimtag.append([0,pointtag])
    count += 1
else:
    for i in range(len(ybotcoord)):
        y = ybotcoord[i]
        for j in range(len(xcoord)):
            x = xcoord[j]
            alias.addPoint(x, y, 0, lc, pointtag+1)
            pointtag += 1
            boundnodetag.append(pointtag)
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
        count += 1

for i in range(count):
    temprowline = []  
    for k in range(numpoint_in_x-1):
        alias.addLine(temppoint,temppoint+1,linetag+1)
        temppoint += 1
        linetag += 1
        temprowline.append(linetag)
        if i == 0:
            boundlinetag.append(linetag)
            topdimtag.append([1,linetag])
        elif i == count-1:
            boundlinetag.append(linetag)
            bottomdimtag.append([1,linetag])
    temppoint += 1
    rowline.append(temprowline)

for i in range(numpoint_in_x):
    temppoint = startpoint + i
    tempcolumnline = []
    for j in range(count-1):
        # print(temppoint)
        alias.addLine(temppoint,temppoint+numpoint_in_x,linetag+1)
        linetag += 1
        tempcolumnline.append(linetag)
        temppoint += numpoint_in_x
        if i == 0:
            boundlinetag.append(linetag)  
            leftdimtag.append([1,linetag])
        elif i == numpoint_in_x-1:
            boundlinetag.append(linetag)
            rightdimtag.append([1,linetag])      
    columnline.append(tempcolumnline)


modeloop = []
modesurf = []
fuelloop = []
fuelsurf = []
cladloop = []
cladsurf = []
templine = startline  
for i in range(count-1):
    for j in range(numpoint_in_x-1):
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
for i in range(nummeshinfuel):
    fuelxtag.append(4+i)
fuelytag = []
for i in range(numfuelplate):
    fuelytag.append(4+4*i)
tempmodeytag = 6
for i in range(numfuelplate-1):
    modeytag.append(tempmodeytag)
    tempmodeytag += 4

for i in range(count-1):
    for j in range(numpoint_in_x-1):
        if i+1 == 1 or i+1 == count-1:
            modesurf.append(tempsurf)
        elif j+1 == 1 or j+1 == numpoint_in_x-1:
            modesurf.append(tempsurf)
        elif j+1 == 2 or j+1 == numpoint_in_x-2:
            cladsurf.append(tempsurf)
        elif i+1 == 2 or i+1 == count-2:
            modesurf.append(tempsurf)
        elif i+1 in fuelytag and j+1 in fuelxtag:
            fuelsurf.append(tempsurf)
        elif i+1 in modeytag:
            modesurf.append(tempsurf)
        else:
           cladsurf.append(tempsurf) 
        tempsurf += 1

for i in range(len(columnline)):
    for j in range(count-1):
        line = columnline[i][j]
        gmsh.model.geo.mesh.setTransfiniteCurve(line, 2)

for i in range(count):
    for j in range(numpoint_in_x-1):
        line = rowline[i][j]
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
for i in range(count-1):
    for j in range(numpoint_in_x-1):
        gmsh.model.geo.mesh.setTransfiniteSurface(tempsurf, "AlternateLeft")
        tempsurf += 1

# print(modesurf)
alias.synchronize()

fuelgroup = gmsh.model.addPhysicalGroup(2, fuelsurf, -1)
gmsh.model.setPhysicalName(2, fuelgroup, 'fuel')
cladgroup = gmsh.model.addPhysicalGroup(2, cladsurf, -1)  
gmsh.model.setPhysicalName(2, cladgroup, 'clad')
watergroup = gmsh.model.addPhysicalGroup(2, modesurf, -1)  
gmsh.model.setPhysicalName(2, watergroup, 'water')

# gmsh.model.addPhysicalGroup(1, boundlinetag, 2)
# gmsh.model.setPhysicalName(1, 2, 'Reflective')

numsurfs = len(fuelsurf)+len(cladsurf)+len(modesurf)

matindexofsurf = []
matnameofsurf = []
for i in range(numsurfs):
    physicaltag = gmsh.model.getPhysicalGroupsForEntity(2, i+1)
    tempname = gmsh.model.getPhysicalName(2, physicaltag[0])
    matindexofsurf.append(int(physicaltag))
    matnameofsurf.append(tempname)

nummix = len(list(set(matindexofsurf)))  

matindex = []
matname = []
for j in range(nummix):
    for i in range(numsurfs):
        if matindexofsurf[i] == j+1 and j+1 not in matindex:
            matindex.append(j+1)
            matname.append(matnameofsurf[i])

# gmsh.option.setNumber('Mesh.MeshSizeFactor', lc)


tempsurf = 1
for i in range(count-1):
    for j in range(numpoint_in_x-1):
        gmsh.model.mesh.setRecombine(2, tempsurf) # 在模型实体上设置重组网格约束尺寸“dim”和标记“tag”
        tempsurf += 1

gmsh.model.mesh.generate(2)
gmshfile = meshname+'.msh'
gmsh.write(gmshfile)

display = '1'
# if display == '1':
    # Launch the GUI to see the results:
    # if '-nopopup' not in sys.argv:
    #     gmsh.fltk.run()
# gmsh.finalize()

def gmsh_to_vitas_fe(elementtype):
    typeindex_map = {
        '1' : '1',
        '2' : '5',
        '3' : '10',
        '4' : '15',
        '5' : '25',
        '6' : '20',
        '8' : '2',
        '9' : '6',
        '11' : '16',
        '16' : '11',
        '17' : '26',
        '18' : '21',
        '10' : '52'
    }
    return typeindex_map.get(elementtype, None)
def reorder(globalnodetag, localnodecoord, type, islargetosmall):
    def takefloat(elem):
        return float(elem[type])
    
    # globalnodeindex = []
    # localnodecoord = []
    # newconnectivity = []
    # for boundnode in (boundnode_in_this_ele):
    #     for i in range(len(nodetag)):
    #         if nodetag[i] == boundnode:
    #             globalnodeindex.append(nodetag[i])
    #             localnodecoord.append(coordinate[i])
    oldnodecooord = localnodecoord[:]
    returnlist = []
    sorted_localnodecoord = localnodecoord
    sorted_localnodecoord.sort(key=takefloat, reverse=islargetosmall)
    length = len(localnodecoord)
    for i in sorted_localnodecoord:
        for j in range(length):
            if oldnodecooord[j] == i:
                returnlist.append(globalnodetag[j])
    
    return returnlist
def list_move_left(list, offset):
    for i in range(offset):
        list.insert(len(list), list[0])
        list.remove(list[0])
    # return templist
def list_move_right(list, offset):
    templist = list[:]
    for i in range(offset):
        templist.insert(0, templist.pop())
    return templist
def listclean(oldlist):
    newlist = str(oldlist).replace('[', '').replace(']', '')
    newlist = newlist.replace("'", '').replace(',', '')
    return (newlist)
def ljust_list(oldlist, numspace):
    newlist = []
    for i in range(len(oldlist)):
        newlist.append(oldlist[i].ljust(numspace))
    return(newlist)
def iflisthasequal(list1, list2):
    tag = False
    for i in list1:
        if i in list2:
            tag = True
    
    return(tag)
with open(gmshfile, 'r') as obj:
    lines = obj.readlines()
    for linenumber, line in enumerate(lines):
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
    templine = nodeline + 2 # 从……开始
    nodecoord = []
    coordline = 0
    boundarynode = []
    nodetag = []
    boundaryentity_dimtag = [] 
    for i in range(num_entities):
        if coordline < elementline - 1:
            temp = lines[templine].split() # 三个数据：entity dim,entity tag, num node
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
                if tempentitydim == 1 and tempentitytag in boundlinetag: # 没用到
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

    for i in range(num_entities_block):
        if templine < endeleline:
            temp = lines[templine].split()
            tempbrindex = int(temp[1])
            tempeletype = temp[2]
            tempnumelement = int(temp[3])
            node_in_ele_line = templine + 1
            for j in range(tempnumelement):
                element_type_index.append(tempeletype)
                mat_index.append(matindexofsurf[tempbrindex-1])
                # ele_to_bureg.append(bureg_index[tempbrindex-1])
                temp2 = lines[node_in_ele_line].split()
                elementtag.append(temp2[0])
                node_in_element.append(temp2[1:])
                node_in_ele_line += 1
            templine = node_in_ele_line
eletypeindex_in_VITAS_FE = []
for i in range(num_elements):
    temptype = element_type_index[i]
    realtypeindex = gmsh_to_vitas_fe(temptype)
    eletypeindex_in_VITAS_FE.append(realtypeindex)
numboundaryele = 0
numboundary_surf = 0
boundaryelement = []
boundnode_in_ele = []
elementorder = []
refsurf = []
for i in range(num_elements):
    if eletypeindex_in_VITAS_FE[i] in ['6', '11']:
        temporder = 2
    else:
        temporder = 1
    elementorder.append(temporder)
    numnode_in_boundary = 0
    for j in node_in_element[i]:
        if j in boundarynode:
            boundnode_in_ele.append(j)
            numnode_in_boundary += 1
    if temporder == 1:
        if numnode_in_boundary >= 2:
            numboundaryele += 1
            numboundary_surf += 1
            refsurf.append('2')
            boundaryelement.append(elementtag[i])
            if numnode_in_boundary > 2:
                numboundary_surf += 1
                boundaryelement.append(elementtag[i])
                refsurf.append('3')
    else:
        if numnode_in_boundary >= 3:
            numboundaryele += 1
            numboundary_surf += 1
            boundaryelement.append(elementtag[i])
            refsurf.append('2')
            if numnode_in_boundary > 3:
                numboundary_surf += 1
                boundaryelement.append(elementtag[i])  
                refsurf.append('3')    

# print(boundaryentity_dimtag)  
# reorder the connectivity
globaleletag = []
boundaryeleindex = []
for i in boundaryelement:
    for j in range(num_elements):
        if elementtag[j] == i:
            globaleletag.append(elementtag[j])
            boundaryeleindex.append(j)
new_node_in_element = []
for i in range(num_elements):
    if i not in boundaryeleindex:
        connectivity = node_in_element[i]
        connectivity.reverse()
boundeleconnect = []
for i in range(numboundary_surf):
    eleindex = boundaryeleindex[i]
    oldconnectivity = node_in_element[eleindex]
    boundnode_in_this_ele = []
    local_dimtag = []
    for j in range(len(boundarynode)):
        for k in range(len(oldconnectivity)):
            tempnodetag = oldconnectivity[k]
            if tempnodetag == boundarynode[j]:
                boundnode_in_this_ele.append(tempnodetag)
                local_dimtag.append(boundaryentity_dimtag[j])
    globalnodetag = []
    globalnodeindex = []
    localnodecoord = []
    newconnectivity = []
    for boundnode in (boundnode_in_this_ele):
        for ii in range(len(nodetag)):
            if nodetag[ii] == boundnode:
                globalnodetag.append(nodetag[ii])
                globalnodeindex.append(ii)
                localnodecoord.append(nodecoord[ii])
                kkkk = int(nodetag[ii])
                if eletypeindex_in_VITAS_FE[eleindex] == '6': 
                    globalnodetag = globalnodetag[:3]
                elif eletypeindex_in_VITAS_FE[eleindex] == '11':
                    globalnodetag = globalnodetag[:4]
    # def reorder(globalnodetag, localnodecoord, type, islargetosmall)
    # type = 0  X
    # type = 1  Y  
    # islargetosmall = True     from largest to smallest
    # islargetosmall = False    from smallest to largest 
    # print(local_dimtag)   
    if iflisthasequal(bottomdimtag, local_dimtag) and iflisthasequal(leftdimtag, local_dimtag):
        sorted_connect = reorder(globalnodetag, localnodecoord, 1, True)  
    elif iflisthasequal(bottomdimtag, local_dimtag) and not(iflisthasequal(leftdimtag, local_dimtag)):
            sorted_connect = reorder(globalnodetag, localnodecoord, 0, False)         
    elif iflisthasequal(rightdimtag, local_dimtag) and iflisthasequal(bottomdimtag, local_dimtag):
        sorted_connect = reorder(globalnodetag, localnodecoord, 0, False)
    elif iflisthasequal(rightdimtag, local_dimtag) and not(iflisthasequal(bottomdimtag, local_dimtag)):
            sorted_connect = reorder(globalnodetag, localnodecoord, 1, False)
    elif iflisthasequal(topdimtag, local_dimtag) and iflisthasequal(rightdimtag, local_dimtag):
        sorted_connect = reorder(globalnodetag, localnodecoord, 1, False)
    elif iflisthasequal(topdimtag, local_dimtag) and not(iflisthasequal(rightdimtag, local_dimtag)):
            sorted_connect = reorder(globalnodetag, localnodecoord, 0, True)
    elif iflisthasequal(leftdimtag, local_dimtag) and iflisthasequal(topdimtag, local_dimtag):
        sorted_connect = reorder(globalnodetag, localnodecoord, 0, True)
    elif iflisthasequal(leftdimtag, local_dimtag) and not(iflisthasequal(topdimtag, local_dimtag)):
        sorted_connect = reorder(globalnodetag, localnodecoord, 1, True)
    # print(sorted_connect)
    tempconnectivity = oldconnectivity[:]
    for jj in range(1):
        for kk in range(len(oldconnectivity)):
            if oldconnectivity[kk] == sorted_connect[jj]:
                tempindex = kk
        if eletypeindex_in_VITAS_FE[eleindex] in ['5', '10']:
            # if tempconnectivity[tempindex - 1] == sorted_connect[jj + 1]:
            #     tempconnectivity.reverse()
            tempconnectivity.reverse()
            # print(tempconnectivity)
            while tempconnectivity[1] != sorted_connect[0]:
                list_move_left(tempconnectivity, 1)
            # print(tempconnectivity)
            newconnectivity = tempconnectivity
        # else:
        #     if eletypeindex_in_VITAS_FE[eleindex] in ['6', '11']:
        #         if eletypeindex_in_VITAS_FE[eleindex] == '6':
        #             pointnodeconnect = tempconnectivity[:3]
        #             linenodeconnect = tempconnectivity[3:]
        #         if eletypeindex_in_VITAS_FE[eleindex] == '11':
        #             pointnodeconnect = tempconnectivity[:4]
        #             linenodeconnect = tempconnectivity[4:]
        #         if pointnodeconnect[tempindex - 1] == sorted_connect[jj + 1]:
        #             pointnodeconnect.reverse()
        #             linenodeconnect.reverse()
        #         newpointnodeconnect = list_move_left(pointnodeconnect, tempindex)
        #         newlinenodeconnect = list_move_left(linenodeconnect, tempindex) 
        #         newpointnodeconnect = list_move_right(newpointnodeconnect, 1)
        #         newlinenodeconnect = list_move_right(newlinenodeconnect, 1)  
        #         for iii in range(len(newpointnodeconnect)):
        #             newconnectivity.append(newpointnodeconnect[iii])
        #             newconnectivity.append(newlinenodeconnect[iii]) 
        #         # newconnectivity = list_remove_right(newconnectivity, 2)
    boundeleconnect.append(newconnectivity)
nemeshfile = meshname + '.nemesh'
nemesh_content = []
nemesh_content.append('! ANL FINITE ELEMENT INPUT FILE DESCRIPTION  9 HEADER LINES ALWAYS')
nemesh_content.append('! CARD TYPE 1:  (Input Style: 0-indexed 1-not indexed) (Debug Printing: 1-10)')
nemesh_content.append('! CARD TYPE 2:  (# Elements) (# Nodes) (# Edit Regions) (# boundary element surfaces)') 
nemesh_content.append('! CARD TYPE 3:  [Optional Index] (ElementType) (Material)  ! READ AS (ELEMENTTYPE(I),I=1,NUMELEMENTS)') 
nemesh_content.append('! CARD TYPE 4:  [Optional Index] (Element Connectivity)    ! READ AS (CONNECTIVITY(J),J=1,ELEMENTVERTICES) per element') 
nemesh_content.append('! CARD TYPE 5:  [Optional Index] (X) [Y] [Z]               ! READ AS (XYZ(I,J),J=1,NUMDIMENSIONS)          per mesh point') 
nemesh_content.append('! CARD TYPE 6:  [Optional Index] (Element #) (Ref. Surf.) (bound. cond.) ! READ AS (BOUNDARYLIST(I,J),J=1,3)  per boundary element surface') 
nemesh_content.append('! CARD TYPE 7:  [Optional Index] (Reaction rate) (# elements)  ! READ AS EDITREACTION(I),EDITREGELEMENTS(I)   per edit region') 
nemesh_content.append('! CARD TYPE 8:  [Optional Index] (Edit Region Elements ! READ AS (EDITREGION(I,J),J=1,NUMELEMENTS) per edit region') 
nemesh_content.append('0'.ljust(6) + '00'.ljust(6))
nemesh_content.append(str(num_elements).ljust(6) + str(num_nodes).ljust(6) + '0'.ljust(6) + str(numboundary_surf).ljust(6)) 
for i in range(num_elements):
    tempstr = str(i+1).ljust(6) + eletypeindex_in_VITAS_FE[i].ljust(6) + str(mat_index[i]).ljust(6)
    nemesh_content.append(tempstr) 
for i in range(num_elements):
    tempconnectivity = []
    if elementtag[i] in boundaryelement:
        for j in range(numboundary_surf):
            if boundaryelement[j] == elementtag[i]:
                tempconnectivity = boundeleconnect[j][:]
    else:
        tempconnectivity = node_in_element[i][:]
    # tempconnectivity = node_in_element[i][:]
    templist = ljust_list(tempconnectivity, 6)
    templist = listclean(templist)
    tempstr = str(i+1).ljust(6) + templist
    nemesh_content.append(tempstr)
    
for i in range(num_nodes):
    templist = ljust_list(nodecoord[i], 30)
    templist = listclean(templist)
    tempstr = str(i+1).ljust(6) + templist
    nemesh_content.append(tempstr)
for i in range(numboundary_surf):
    tempstr = str(i+1).ljust(6) + boundaryelement[i].ljust(6) + refsurf[i].ljust(6) + '0'.ljust(6)
    nemesh_content.append(tempstr)
# for i in range(num_elements):
#     tempstr = str(i+1).ljust(6) + elementtag[i].ljust(6) + str(ele_to_bureg[i]).ljust(6) 
#     nemesh_content.append(tempstr)
with open(nemeshfile, 'w') as write_obj:
    for i in range(len(nemesh_content)):
        write_obj.write(nemesh_content[i])
        write_obj.write('\n')
# write .regionalias files
regionaliasfile = meshname + '.regionalias'
# numbureg = numbuzone
# tempburegindex = set(bureg_index)
# for bureg in tempburegindex:
#     if bureg != 0:
#         numbureg += 1
regionalias = []
regionalias.append(nemeshfile)
for j in range(nummix):
    regionalias.append('ALIAS REGION_00000000' + str(matindex[j]) + '  ' + 'R_' + matname[j])
# if ifbu == '1':
#     regionalias.append('NUMBUREG'.ljust(15) + str(numbureg).ljust(10))
#     for j in range(num_elements):
#         tempstr = 'BUREG'.ljust(10) + elementtag[j].ljust(10) + str(ele_to_bureg[j]).ljust(10) 
#         regionalias.append(tempstr)
with open(regionaliasfile, 'w') as reobj:
    for k in range(len(regionalias)):
        reobj.write(regionalias[k] + '\n')


# produce .assignment files
assignment_file = meshname+'.assignment'
assignment = []
assignment.append('! MATERIAL_DEF  <Material name>   { <isotope name>  <concentration> }')
assignment.append('! ---------------------------------------------------------------------------')
for i in range(nummix):
    assignment.append('MATERIAL_DEF'.ljust(20) + (matname[i] + '_M').ljust(20) + (matname[i]).ljust(20) + '1.0')
assignment.append('! REGION_ALIAS  <Name of mesh region> <Name of composition>')
assignment.append('! ---------------------------------------------------------------------------')
for i in range(nummix):
    assignment.append('REGION_ALIAS'.ljust(20) + ('R_' + matname[i]).ljust(20) + (matname[i] + '_M').ljust(20))
assignment.append('! REGION_PROPERTY   <Name of mesh region> {<property>     <initial setting>}')
assignment.append('! ---------------------------------------------------------------------------')
for i in range(nummix):
    assignment.append('REGION_PROPERTY'.ljust(20) + ('R_' + matname[i]).ljust(20) + 'Density(g/cc)'.ljust(20)+ '1.0')
with open(assignment_file, 'w') as objfile:
    for i in range(len(assignment)):
        objfile.write(assignment[i] + '\n')

########################################################################
# pointtag = 0
# linetag = 0
# curvetag = 0
# surftag = 0

# falength = 7.72
# fawidth = 7.72
# fawithoutgap = 7.62
# watergap = 0.05
# boundclad = 0.48
# alias.addRectangle(-falength/2, -fawidth/2, 0, falength, fawidth, 1)

# pointtag = 4
# templengthlist = [7.62, 6.66, 6.66]
# tempwidthlist = [7.62, 7.62, 7.372]
# for i in range(3):
#     length = templengthlist[i]
#     width = tempwidthlist[i]
#     alias.addPoint(-length/2, width/2, 0, lc, pointtag+1)
#     alias.addPoint(length/2, width/2, 0, lc, pointtag+2)
#     alias.addPoint(length/2, -width/2, 0, lc, pointtag+3)
#     alias.addPoint(-length/2, -width/2, 0, lc, pointtag+4)
#     pointtag += 4

# linetag = 4
# temppoint = 4
# alias.addLine(temppoint+1,temppoint+5,linetag+1)
# alias.addLine(temppoint+5,temppoint+9,linetag+2)
# alias.addLine(temppoint+9,temppoint+10,linetag+3)
# alias.addLine(temppoint+10,temppoint+6,linetag+4)
# alias.addLine(temppoint+6,temppoint+2,linetag+5)
# alias.addLine(temppoint+2,temppoint+3,linetag+6)
# alias.addLine(temppoint+3,temppoint+7,linetag+7)
# alias.addLine(temppoint+7,temppoint+11,linetag+8)
# alias.addLine(temppoint+11,temppoint+12,linetag+9)
# alias.addLine(temppoint+12,temppoint+8,linetag+10)
# alias.addLine(temppoint+8,temppoint+4,linetag+11)
# alias.addLine(temppoint+4,temppoint+1,linetag+12)
# linetag += 12

# watercurv = alias.addCurveLoop([5,6,7,8,9,10,11,12,13,14,15,16])

# surftag = 1
# temporiginy = 3.61
# cladlength = 6.66
# cladwidth = 0.152
# fplength = 6.16
# fpwidth = 0.076
# modelength = 6.66
# modewidth = 0.228
# cladplatelist = []
# fuelplatelist = []
# modeplatelist = []
# fuelbottom = linetag
# fuelright = linetag+1
# fueltop = linetag+2
# fuelleft = linetag+3

# tothole = [watercurv]
# for i in range(numfuelplate):
#     # alias.addRectangle(-cladlength/2, temporiginy-cladwidth/2, 0, cladlength, cladwidth, surftag+1)
#     alias.addRectangle(-fplength/2, temporiginy-fpwidth/2, 0, fplength, fpwidth, surftag+1)
#     # cladplatelist.append(surftag+1)
#     fuelplatelist.append(surftag+1)
#     surftag += 1
#     temporiginy -= 0.38  
#     linetag += 4

# modebottom = linetag
# moderight = linetag+1
# modetop = linetag+2
# modeleft = linetag+3
# temporiginy = 3.42
# for i in range(numfuelplate-1):
#     alias.addRectangle(-modelength/2, temporiginy-modewidth/2, 0, modelength, modewidth, surftag+1)
#     modeplatelist.append(surftag+1)
#     surftag += 1
#     temporiginy -= 0.38 
#     linetag += 4

# curv1 = alias.getCurveLoops(1)
# alias.addPlaneSurface([curv1[0],watercurv], surftag+1)
# surftag += 1
# modeplatelist.append(surftag)

# tothole = tothole + fuelplatelist + modeplatelist
# alias.addPlaneSurface(tothole, surftag+1)
# surftag += 1
# cladsurf = surftag

# alias.remove([(2,1)])

# # The `setTransfiniteCurve()' meshing constraints explicitly specifies the
# # location of the nodes on the curve.
# tempfueltop = fueltop
# tempfuelbottom = fuelbottom
# tempfuelright = fuelright
# tempfuelleft = fuelleft
# for i in range(numfuelplate):
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfueltop, 25)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelbottom, 25)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelright, 2)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelleft, 2)
#     tempfuelbottom += 4
#     tempfuelleft += 4
#     tempfuelright +=4 
#     tempfueltop += 4

# tempmodetop    = modetop
# tempmodebottom = modebottom
# tempmoderight  = moderight
# tempmodeleft   = modeleft
# for i in range(numfuelplate):
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodetop, 27)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodebottom, 27)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmoderight, 2)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodeleft, 2)
#     tempmodetop += 4
#     tempmodebottom += 4
#     tempmoderight +=4 
#     tempmodeleft += 4

# alias.synchronize()

# fuelgroup = gmsh.model.addPhysicalGroup(2, fuelplatelist, -1)
# gmsh.model.setPhysicalName(2, fuelgroup, 'fuel')
# cladgroup = gmsh.model.addPhysicalGroup(2, [cladsurf], -1)  
# gmsh.model.setPhysicalName(2, cladgroup, 'clad')
# watergroup = gmsh.model.addPhysicalGroup(2, modeplatelist, -1)  
# gmsh.model.setPhysicalName(2, watergroup, 'water')
#######################################################################

# gmsh.model.mesh.renumberNodes()
# for i in range(1,5):
#     gmsh.model.mesh.setTransfiniteCurve(i,numpoint)
# meshfield_alias = gmsh.model.mesh.field
# meshfield_alias.add('Distance', 1)
# meshfield_alias.setNumber(1, "PointsList", 100)
# meshfield_alias.setNumber(1, 'CurvesList', curveloop_tag[0])
# meshfield_alias.setNumber(1, 'Sampling', 100)
# meshfield_alias.add('Threshold', 2)
# meshfield_alias.setNumber(2, 'InField', 1)
# meshfield_alias.setNumber(2, 'SizeMin', lc / 30)
# meshfield_alias.setNumber(2, 'SizeMax', lc)
# meshfield_alias.setNumber(2, 'DistMin', 0.2)
# meshfield_alias.setNumber(2, 'DistMax', 0.5)
# meshfield_alias.setAsBackgroundMesh(2)
# gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
# gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 0)
# gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# gmsh.option.setNumber('Geometry.Curves', 0)

# gmsh.option.setNumber('Mesh.Algorithm', 3)
# gmsh.option.setNumber('Mesh.ColorCarousel', 2)
# gmsh.option.setNumber('Mesh.CompoundMeshSizeFactor', 0.5)

# gmsh.option.setNumber('Mesh.ElementOrder', 1)
# gmsh.option.setNumber('Mesh.MeshSizeFactor', lc)

# gmsh.option.setNumber('Mesh.MeshSizeMin', 0.2)
# gmsh.option.setNumber('Mesh.MeshSizeMax', 1.0)
# gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 0)

# gmsh.option.setNumber('Mesh.Nodes', 1)
# gmsh.option.setNumber('Mesh.NodeLabels', 1)

# gmsh.option.setNumber('Mesh.RecombinationAlgorithm', 3)
# gmsh.option.setNumber('Mesh.RecombineAll', 1)
# gmsh.option.setNumber("Mesh.Smoothing", 100)
# gmsh.option.setNumber('Mesh.SurfaceEdges', 1)
# gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# gmsh.option.setNumber('Mesh.SurfaceLabels', 1)

# gmsh.model.mesh.setRecombine(2, 1)
# gmsh.model.mesh.setRecombine(2, surface_tag[2])
# gmsh.model.mesh.partition(3)
# gmsh.model.mesh.optimize('Netgen')
# gmsh.model.mesh.recombine()
# gmsh.model.mesh.refine()

# gmsh.option.setNumber('General.NumThreads', 8)

# gmsh.model.mesh.generate(2)
# gmshfile = meshname+'.msh'
# gmsh.write(gmshfile)

# ifdisplay = '1'
# if ifdisplay == '1':
#     # Launch the GUI to see the results:
#     if '-nopopup' not in sys.argv:
#         gmsh.fltk.run()
# gmsh.finalize()


# meshname = 'jrr'
# lc = 0.1
# numfuelplate = 20
# gmsh.initialize(sys.argv)
# gmsh.model.add(meshname)
# occ_alias = gmsh.model.occ
# geo_alias = gmsh.model.geo
# alias = occ_alias
# pointtag = 0
# linetag = 0
# curvetag = 0
# surftag = 0

# falength = 7.72
# fawidth = 7.72
# fawithoutgap = 7.62
# watergap = 0.05
# boundclad = 0.48
# alias.addRectangle(-falength/2, -fawidth/2, 0, falength, fawidth, 1)

# pointtag = 4
# templengthlist = [7.62, 6.66, 6.66]
# tempwidthlist = [7.62, 7.62, 7.372]
# for i in range(3):
#     length = templengthlist[i]
#     width = tempwidthlist[i]
#     alias.addPoint(-length/2, width/2, 0, lc, pointtag+1)
#     alias.addPoint(length/2, width/2, 0, lc, pointtag+2)
#     alias.addPoint(length/2, -width/2, 0, lc, pointtag+3)
#     alias.addPoint(-length/2, -width/2, 0, lc, pointtag+4)
#     pointtag += 4

# linetag = 4
# temppoint = 4
# alias.addLine(temppoint+1,temppoint+5,linetag+1)
# alias.addLine(temppoint+5,temppoint+9,linetag+2)
# alias.addLine(temppoint+9,temppoint+10,linetag+3)
# alias.addLine(temppoint+10,temppoint+6,linetag+4)
# alias.addLine(temppoint+6,temppoint+2,linetag+5)
# alias.addLine(temppoint+2,temppoint+3,linetag+6)
# alias.addLine(temppoint+3,temppoint+7,linetag+7)
# alias.addLine(temppoint+7,temppoint+11,linetag+8)
# alias.addLine(temppoint+11,temppoint+12,linetag+9)
# alias.addLine(temppoint+12,temppoint+8,linetag+10)
# alias.addLine(temppoint+8,temppoint+4,linetag+11)
# alias.addLine(temppoint+4,temppoint+1,linetag+12)
# linetag += 12

# watercurv = alias.addCurveLoop([5,6,7,8,9,10,11,12,13,14,15,16])

# surftag = 1
# temporiginy = 3.61
# cladlength = 6.66
# cladwidth = 0.152
# fplength = 6.16
# fpwidth = 0.076
# modelength = 6.66
# modewidth = 0.228
# cladplatelist = []
# fuelplatelist = []
# modeplatelist = []
# fuelbottom = linetag
# fuelright = linetag+1
# fueltop = linetag+2
# fuelleft = linetag+3

# tothole = [watercurv]
# for i in range(numfuelplate):
#     # alias.addRectangle(-cladlength/2, temporiginy-cladwidth/2, 0, cladlength, cladwidth, surftag+1)
#     alias.addRectangle(-fplength/2, temporiginy-fpwidth/2, 0, fplength, fpwidth, surftag+1)
#     # cladplatelist.append(surftag+1)
#     fuelplatelist.append(surftag+1)
#     surftag += 1
#     temporiginy -= 0.38  
#     linetag += 4

# modebottom = linetag
# moderight = linetag+1
# modetop = linetag+2
# modeleft = linetag+3
# temporiginy = 3.42
# for i in range(numfuelplate-1):
#     alias.addRectangle(-modelength/2, temporiginy-modewidth/2, 0, modelength, modewidth, surftag+1)
#     modeplatelist.append(surftag+1)
#     surftag += 1
#     temporiginy -= 0.38 
#     linetag += 4

# curv1 = alias.getCurveLoops(1)
# alias.addPlaneSurface([curv1[0],watercurv], surftag+1)
# surftag += 1
# modeplatelist.append(surftag)

# tothole = tothole + fuelplatelist + modeplatelist
# alias.addPlaneSurface(tothole, surftag+1)
# surftag += 1
# cladsurf = surftag

# alias.remove([(2,1)])

# # The `setTransfiniteCurve()' meshing constraints explicitly specifies the
# # location of the nodes on the curve.
# tempfueltop = fueltop
# tempfuelbottom = fuelbottom
# tempfuelright = fuelright
# tempfuelleft = fuelleft
# for i in range(numfuelplate):
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfueltop, 25)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelbottom, 25)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelright, 2)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempfuelleft, 2)
#     tempfuelbottom += 4
#     tempfuelleft += 4
#     tempfuelright +=4 
#     tempfueltop += 4

# tempmodetop    = modetop
# tempmodebottom = modebottom
# tempmoderight  = moderight
# tempmodeleft   = modeleft
# for i in range(numfuelplate):
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodetop, 27)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodebottom, 27)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmoderight, 2)
#     gmsh.model.geo.mesh.setTransfiniteCurve(tempmodeleft, 2)
#     tempmodetop += 4
#     tempmodebottom += 4
#     tempmoderight +=4 
#     tempmodeleft += 4

# alias.synchronize()

# fuelgroup = gmsh.model.addPhysicalGroup(2, fuelplatelist, -1)
# gmsh.model.setPhysicalName(2, fuelgroup, 'fuel')
# cladgroup = gmsh.model.addPhysicalGroup(2, [cladsurf], -1)  
# gmsh.model.setPhysicalName(2, cladgroup, 'clad')
# watergroup = gmsh.model.addPhysicalGroup(2, modeplatelist, -1)  
# gmsh.model.setPhysicalName(2, watergroup, 'water')