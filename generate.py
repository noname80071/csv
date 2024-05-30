import pandas

data = [i for i in range(0, 100000)]

pd_data = pandas.DataFrame(data)
pd_data.to_csv('b.csv', index=False, header=False, sep=':')
