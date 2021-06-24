import pandas as pd


#file: archivo para reordenar que fue generado en DCaLinescanCSV
file = 'Linescan_nro 38 label WALHALLA_295_P1_201902011156_MGA94_55.csv'
df = pd.read_csv(file)


df.head()

df.columns #estructura columnas


df.linescan.mean() #Verifico que haya datos !=0, o sea, que haya mínimo de datos



df.target.mean() #Verifico que haya datos !=0, ídem anterior


df['id'] = df.index #Agrego columna con id para identificación correcta


cols = ['id','label', 'x','y','dateTimeLocal', 'linescan','target'] #Orden de columnas correcto


df = df[cols]
df.head()

df.to_csv(f'Reordered {file}',index = False)


print("ok")


