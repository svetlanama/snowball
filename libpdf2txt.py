# import PyPDF2
import re
import textract






def pdf_to_text_textract(pdf_file_path):

    
    try:
        page_text = textract.process(pdf_file_path, encoding='ascii', method='pdfminer', layout=False)    #, encoding='ascii'
        print('method=pdfminer')
        return page_text
    except:
        pass
    
    try:
        page_text = textract.process(pdf_file_path, language='eng', method='tesseract', layout=False)    #, encoding='ascii'
        print('method=tesseract')
        return page_text
    except:
        pass
    
    try:
        page_text = textract.process(pdf_file_path, layout=False)    #, encoding='ascii'
        print('method=default')
        return page_text
    except:
        pass

    return ''

def pdf_to_text_pypdf(_pdf_file_path):	
    pdf_content = PyPDF2.PdfFileReader(open(_pdf_file_path, "rb")) 
        # 'Rb' Opens a file for reading only in binary format. 
        # The file pointer is placed at the beginning of the file
    text_extracted = "" # A variable to store the text extracted from the entire PDF
	
    for x in range(0, pdf_content.getNumPages()): # text is extracted page wise
        pdf_text = ""  # A variable to store text extracted from a page
        pdf_text = pdf_text + pdf_content.getPage(x).extractText() 
        # Text is extracted from page 'x'
        text_extracted = text_extracted + "".join(i for i in pdf_text if ord(i) < 128) + "\n\n\n"
        # Non-Ascii characters are eliminated and text from each page is separated
    return text_extracted






ligatures={
   chr(0x10):'ff',
   chr(0x06):'fi',
   chr(0x02):'fi',
   chr(0x05):'ff',
   chr(0x03):'ff',
   chr(0x19):'fl',
   chr(0x0c):'fi',
   chr(0x0b):'ff',
   # chr(0x1a):' ',
   #   unichr(0xA732):'AA',
   #   unichr(0xA733):'aa',
   #   unichr(0x00C6):'AE',
   #   unichr(0x00E6):'ae',
   #   unichr(0xA734):'AO',
   #   unichr(0xA735):'ao',
   #   unichr(0xA736):'AU',
   #   unichr(0xA737):'au',
   #   unichr(0xA738):'AV',
   #   unichr(0xA739):'av',
   #   unichr(0xA73A):'AV',
   #   unichr(0xA73B):'av',
   #   unichr(0xA73C):'AY',
   #   unichr(0xA73D):'ay',
   #   unichr(0x1F670):'et',
   #   unichr(0xFB00):'ff',
   #   unichr(0xFB03):'ffi',
   #   unichr(0xFB04):'ffl',
   #   unichr(0xFB01):'fi',
   #   unichr(0xFB02):'fl',
   #   unichr(0x0152):'OE',
   #   unichr(0x0153):'OE',
   #   unichr(0xA74E):'OO',
   #   unichr(0xA74F):'oo',
   #   unichr(0x1E9E):'fs',
   #   unichr(0x00DF):'fz',
   #   unichr(0xFB06):'st',
   #   unichr(0xFB05):'ft',
   #   unichr(0xA728):'TZ',
   #   unichr(0xA729):'tz',
   #   unichr(0x1D6B):'ue',
   #   unichr(0xA760):'VY',
   #   unichr(0xA761):'vy'
}
def clean_text(rawtxt):
    '''
    
    '''
    f=open(rawtxt,'rb')
    content = f.readlines()
    f.close()
    
    # if line starts with lowercase letter, join in with previous line
    len_content=len(content)
    for i in range(1,len_content+1):
        j=len_content-i
        
        if content[j][0].islower():
            c=content[j-1].strip()
            if len(c)>0 and c[-1]=='-':
                #print(c)
                content[j-1]=c[:-1].strip()+content[j]
                content[j]=""
            #elif len(c)>0 and c[-1]=='-':
            #    content[j-1]=c[:-1].strip()+content[j]
            #    content[j]=""
            else:
                content[j-1]=c+" "+content[j]
                content[j]=""            
        else:
            c=content[j-1].strip()
            if len(c)>0 and c[-1]==',':
                content[j-1]=c+" "+content[j]
                content[j]=""
    for j in range(0,len_content):
        content[j]=content[j].strip()
    content_filtered=[s for s in content if len(s)>0]
    
    # replace ligatures here
    len_content=len(content_filtered)
    for c in ligatures:
        f=c
        t=ligatures[c]
        for j in range(0,len_content):
            content_filtered[j]=content_filtered[j].replace(f,t)
            
    content=re.sub(r'\s*-\s*\n', '', "\n".join(content_filtered))
    content=re.sub(r'\n[ ,0-9]+\]',' ', content)
    content=re.sub(r'\s*,\s*\n',', ',content)
    content=re.sub(r'\n([a-z]+)',r'\1',content)
    content=re.sub(r'\n\s*\(',r'(',content)
    content=re.sub(r'\s+\.',r'.',content)
    content=re.sub(r'\n\d+\]',' ',content)
    content=re.sub(r'\[[0-9, ]+\]',' ',content)
    content=re.sub(r'\s+\.',r'.',content)
    content=re.sub(r'\s+,',r',',content)
    content=re.sub(r'( and| or| if| of| to | over| a| the| in| between| when| where| is| The)\s*\n',r'\1 ',content)

    #content=re.sub(r'\s*,\s*\n',', ',
    #    re.sub(r'\s*-\s*\n', '', 
    #        "\n".join(content_filtered)))
    
    return content
    