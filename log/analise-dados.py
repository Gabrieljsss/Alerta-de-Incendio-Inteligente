import matplotlib
import matplotlib.pyplot as plt
import numpy as np

nome_do_arquivo = "log-temp-1.txt" 


file = open(nome_do_arquivo, "r")
data = file.readlines()

c = 0
xaxis = []
for i in data:
	xaxis.append(c)
	data[c] = int(i.strip("\n"))
	c+=1
s = data
t = xaxis

print data 

titulo = 'Temperatura ao longo do tempo'
ylabel = 'Temp'

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel=ylabel,
       title=titulo)
ax.grid()

fig.savefig("test.png")
plt.show()
