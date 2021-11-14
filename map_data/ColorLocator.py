from PIL import Image
import math

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    name2 = ""
    other_info = ""
    lastKnownY = -1



colorFile = open("Input\\colorList.txt")
colorsList = []


def getColors():
    prov = ProvinceDefinition()
    colorStarted = False
    for line in colorFile:
        word = line.split(" ")
        for w in word:
            if "(" in w and not colorStarted:
                prov.red = int(w.replace("(",""))
                colorStarted = True
            elif colorStarted and ")" in w:
                prov.blue = int(w.replace(")",""))
                colorStarted = False
                colorsList.append(prov)
                prov = ProvinceDefinition()
            elif colorStarted:
                prov.green = int(w)

    pass

def draw_UpdatedProvinces(colorList):
    MNRMapProvinces = Image.open("Input\\provinces.png")
    MNRMapProvinces.putalpha(255)
    pixMNR = MNRMapProvinces.load()
    img = Image.new(MNRMapProvinces.mode, MNRMapProvinces.size, 'white')
    pixNew = img.load()
    x1,y1=0,0
    x2,y2=MNRMapProvinces.size[0],MNRMapProvinces.size[1]
    counter = math.ceil((y2-y1)/50)
    tupleList = []
    lastY = []
    for prov in colorList:
        tupleList.append((prov.red,prov.green,prov.blue,255))
        lastY.append(-1)

    tmpTotal = len(tupleList)
    count = 0

    tmpMapColor = []
    ColorLength = []
    for y in range(y1,y2):
        mapLine = []
        ColorlengthLine = []
        length = 1
        color = pixMNR[x1,y]
        for x in range(x1+1,x2):
            if pixMNR[x,y] == color:
                length+=1
            else:
                mapLine.append(color)
                ColorlengthLine.append(length)

                length=1
                color = pixMNR[x,y]
        mapLine.append(color)
        ColorlengthLine.append(length)

        tmpMapColor.append(mapLine)
        ColorLength.append(ColorlengthLine)

    #print(tupleList)
    #print(counter)
    for y in range(y1,y2):
        if y%counter == 0:
            #print("%i%%"%((y*5)/counter))
            for i, prov in enumerate(lastY):
                if prov>-1 and prov<y-(MNRMapProvinces.size[1]/40):
                    #print(tupleList[i])
                    del lastY[i]
                    del tupleList[i]
                    i-=1
                    count+=1
            if (count*1000/tmpTotal)/10 > (y*2)/counter:
                print("%i%%"%((count*1000/tmpTotal)/10))
            else:
                print("%i%%"%((y*2)/counter))
            if(len(tupleList)==0):
                break
        tx=0
        for x in range(0,len(tmpMapColor[y])):
            if tmpMapColor[y][x] in tupleList:
                for i in range(0,ColorLength[y][x]):
                    pixNew[tx+i,y] = (tupleList[tupleList.index(tmpMapColor[y][x])])
                #pixNew[x,y] = (titleList[i].color[0],titleList[i].color[1],titleList[i].color[2],255)
                lastY[tupleList.index(tmpMapColor[y][x])] = y
            tx+=ColorLength[y][x]
    img.show()
    img.save("Output\\province_Output.png")
    img.close()

getColors()
draw_UpdatedProvinces(colorsList)