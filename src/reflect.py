import os

def parseHash(line, begin):
    start = line.find(begin) + len(begin) + 1
    return line[start:line.find(' ', start + 1)]

def parseKeyword(source, keyword):
    data = {}
    hash = None
    capture = False
    beginKeyword = f"__{keyword}_BEGIN__"
    endKeyword = f"__{keyword}_END__"
    for line in source.splitlines():
        if beginKeyword in line:
            capture = True
            hash = parseHash(line, beginKeyword)
            if(hash in data):
                print("Error: Hash already in data: %s" % hash)
                exit(1)
            data[hash] = []
        elif endKeyword in line:
            capture = False
            endHash = parseHash(line, endKeyword)
            if hash != endHash:
                print("Error: Hash mismatch: %s vs %s" % (hash, endHash))
                exit(1)
        elif capture:
            data[hash].append(line)
    return data

def updateFiles(directory, sourceModified, data, persist=False):
    for d in data:
        pth = os.path.join(directory, f"{d}.def")
        #if len(data[d]) == 1:
            #print("Skipping because")
        if not os.path.exists(pth):
            print("Warning: Missing file: " + pth)
            continue
        lastModified = os.path.getmtime(pth) # seconds since e.g. 1970
        indentation = len(data[d][0])
        for i in range(indentation):
            if data[d][0][i] != " ":
                indentation = i
                break
        #print(f"indentation={indentation}")
        if sourceModified > lastModified:
            content = "\n".join([x[indentation:] for x in data[d]])
            if persist:
                with open(pth, 'w') as f:
                    f.write(content)
            else:
                print(content)
            print("File updated: " + pth)

def reflectFile(dataDir, genFile):
    if not os.path.exists(genFile):
        return False
    pragmasDir = os.path.join(dataDir, 'pragmas')
    definitionsDir = os.path.join(dataDir, 'definitions')
    lastModified = os.path.getmtime(genFile) # seconds since e.g. 1970
    source = ""
    with open(genFile, 'r') as f:
        source = f.read()
    pragmas = parseKeyword(source, 'PRAGMA')
    definitions = parseKeyword(source, 'DEFINITION')
    updateFiles(pragmasDir, lastModified, pragmas, True)
    updateFiles(definitionsDir, lastModified, definitions, True)
    return True

def reflectSource(dataDir, genDir):
    # genDir = 'gen'
    # dataDir = 'data'
    if not os.path.exists(genDir):
        return False

    rval = True
    for file in os.listdir(genDir): # Only when change is detected.
        if not file.endswith(".cpp") and not file.endswith(".tsx") and not file.endswith(".ts"):
            continue
        filePath = os.path.join(genDir, file)
        if not reflectFile(dataDir, filePath):
            rval = False
            break
    return rval