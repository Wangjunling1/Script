# -*- coding: utf-8 -*-
from win32com import client as wc
import os
def main(path):
    '''
    Convert 'doc' to 'docx'
    :param path:The path where the script is currently located
    :return:None
    '''
    for root,folder,files in os.walk(path):
        for file in files:
            if file[-1:]=='c':
                print(file)
                w = wc.DispatchEx('Word.Application')
                doc=w.Documents.Open(os.path.join(root,file))
                doc.SaveAs(str(os.path.join(root,file))+'x',16)
                doc.Close()
                w.Quit()
if __name__ == '__main__':
    path=os.getcwd()
    main(path)



