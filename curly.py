# curly 28/03/22
import os
from pathlib import Path
folderPath = Path(input('input full folder path > '))
fileNames = os.listdir(folderPath)


class Line():
    def __init__(self, line, lineNo) -> None:
        self._content = line.lstrip('\t').rstrip('\n')
        self._indents = 0
        for char in line:
            if char == '\t':
                self._indents += 1
            else:
                break
        self._lineNo = lineNo
        self._error = ''
        
    def printLine(self):
        return '\t'*self._indents + self._content + ' ' + self._error + '\n'
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)


def debugFile(folderPath, fileName):
    filePathName = folderPath / fileName
    file = open(str(filePathName), 'r')
    opening = 0
    closing = 0
    curlyLines = []

    unmatchedOpens = []
    # TODO unmatched close
    unmatchedClose = []


    temp = []
    for lineNo, line in enumerate(file):
        oLine = Line(line, lineNo+1)

        # counting open and closing brackets and checking for unmatched open brackets
        if '{' in oLine._content and '}' in oLine._content:
            opening += 1
            closing += 1
        elif '{' in oLine._content:
            opening += 1
            curlyLines.append(oLine)
            temp.append(oLine)
        elif '}' in oLine._content:
            closing += 1
            curlyLines.append(oLine)
            # removes matching open bracket
            for i in range(len(temp)-1,-1,-1):
                if temp[i]._indents == oLine._indents:
                    temp.pop(i)
                    if i < len(temp)-1:
                        for n in range(i, len(temp)-2):
                            # make sure any unmatched lines cant be mistakenly matched with a different closing
                            unmatchedOpens.append(temp.pop(n))
                            oLine._error = '!!UNMATCHED OPEN!!'
                    break
            else:
                unmatchedClose.append(oLine)
                oLine._error = '!!UNMATCHED CLOSE!!'
            
    print(f'\n{fileName}')
    print('\nunmatched opening brackets')
    for line in unmatchedOpens:
        print(f'line {line._lineNo}: {line._content}')
        
    print('\nunmatched closing brackets')
    for line in unmatchedClose:
        print(f'line: {line._lineNo}: {line._content}')

    out = open(f'output_({fileName[:-4]}).txt', 'w')
    out.write('{: ' + str(opening) + '\n}: ' + str(closing) + '\n')
    for line in curlyLines:
        out.write('\n' + line.printLine())
        
    file.close()
    out.close()

for fileName in fileNames:
    if fileName[-4:] == '.txt':
        debugFile(folderPath, fileName)