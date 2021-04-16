from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

def parsePdfName(name):
    if len(name)<4:
        return name + '.pdf'
    if '.pdf'!=name[-4:]:
        return name + '.pdf'
    return name


'''This other function would be more elegant if it used the merge() attribute, but it doesn't work well on my computer'''


def concatFiles():
    i = 0
    names = []
    writer = PdfFileWriter()
    while i != -1 :
        print('\nInput the name of the ', i+1, 'th file, otherwise press E to end: ')
        names.append(input())
        i = i + 1
        if names[-1] == 'E':
            names.pop()
            i = -1
    
    for j in range(0, len(names), 1):
        inputs = open(str(parsePdfName(names[j])), 'rb')
        reader = PdfFileReader(parsePdfName(names[j]))
        for page in range(0, reader.getNumPages()):
            writer.addPage(reader.getPage(page))
        inputs.close()
    
    newPdfName = input('Input the name of the new Pdf: ')
    output = open(str(parsePdfName(newPdfName)), 'wb')
    writer.write(output)
    output.close()

def slicePdf():
    i = 0
    slices = [[]]
    inPdfName = input('Insert the pdf\'s name: ')
    inPdfName = parsePdfName(inPdfName)
    print('Insert the lower and the upper page of the slice in the order you want in the new file')
    while (i != -1):
        ch = input('New slice? Press Y for yes, N for no ')
        if ch == 'Y':
            print('Slice from:') 
            slices[i].append(int(input())) 
            print('to: ') 
            slices[i].append(int(input()))
            slices.append([])
            i = i + 1
        elif ch == 'N':
            i = -1
            slices.pop()
        else:
            print('Error in the input, try again')
    inputfile = open(str(inPdfName), 'rb')
    reader = PdfFileReader(inputfile)
    writer = PdfFileWriter()
    for j in range(0, len(slices)):
        for page in range(slices[j][0], slices[j][1]+1):
            if page <= reader.getNumPages():
                writer.addPage(reader.getPage(page-1))
            else:
                print('Slice excedes file size')
    
    outPdfName = input('New file name: ')
    outPdfName = parsePdfName(outPdfName)
    print(str(outPdfName))
    output = open(str(outPdfName), 'wb')
    writer.write(output)
    output.close()
    inputfile.close()

class fileAndSlice():

    def __init__(self):
        self.fileNames = []
        self.slices = []

# These methods are redundant but safer
    def newFileName(self, fileName):
        self.fileNames.append(fileName)
        
    def newSlice(self, first, last):
        self.slices.append([first, last])

    def getSlice(self, index):
        if index < len(self.slices):
            return self.slices[index]
        

def sliceAndMerge():
    i = 0
    writer = PdfFileWriter()
    data = fileAndSlice()
    while(i!=-1):
        fileName = input('Enter file name. Digit 42 to end: ')
        if fileName == '42':
            print('Thank you')
            i = -1
        else:
            data.newFileName(parsePdfName(fileName))
            first = int(input("First page of the slice: "))
            last = int(input("Last page of the slice: "))
            data.newSlice(first, last)
    for j in range(0, len(data.fileNames)):
        reader = PdfFileReader(str(data.fileNames[j]))
        for page in range(data.slices[j][0], data.slices[j][1]+1):
            writer.addPage(reader.getPage(page-1))
    outfilename = input("New file name: ")
    output = open(parsePdfName(outfilename), "wb")
    writer.write(output)
    output.close()


        
        


    

'''Simple menu to choose the activity'''
print('For concatenating multiple pdfs press 1',
      'For slicing a pdf press 2',
      'For slicing and merging multiple pdfs press 3',
      'Else press E', sep = '\n')
choice = input()
if choice not in ['1', '2', '3', 'E']:
    print('Invalid input')
    exit()

if choice == '1':
    concatFiles()
elif choice == '2':
    slicePdf()
elif choice == '3':
    sliceAndMerge()
else:
    print('Thank you for using me')
