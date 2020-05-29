1、pdf文件中的表格数据提取保存至excel中

```python
import pdfplumber
import pandas as pd
def extractTable(pdfpath,savepath,pageindexs = None):
    pdf = pdfplumber.open(pdfpath)
    if pageindexs:#规定提取哪几页的表格
        for index in pageindexs:
            page = pdf.pages[index]
            table = page.extract_tables()#提取页面的表格
            df = pd.DataFrame(table[1:],columns=table[0])
            df.to_csv(savepath, index=False, mode='a',encoding='utf-8')
            print(table[0])
    else:
        for page in pdf.pages:
            table = page.extract_tables()
            # print(table[0][1:])
            df = pd.DataFrame(table[0][1:],columns=table[0][0])
            print(df)
            df.to_csv(savepath,index=False)

extractTable('test.pdf','test.csv')
```