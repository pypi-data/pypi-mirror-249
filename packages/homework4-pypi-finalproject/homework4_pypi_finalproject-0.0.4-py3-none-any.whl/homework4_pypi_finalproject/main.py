#task 1 load data
import csv
my_data = []
rows = []

with open("orcl.csv", "r") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        my_data.append(row)



#task 2 calculate sma and rsi
#calculate sma
windows_size = 5
i = 0 
sma_values = []
while i < len(my_data) - windows_size + 1:
        window = [float(row[4]) for row in my_data[i: i + windows_size]]
        sma = sum(window) / len(window)
        sma_values.append(sma)
        i += 1



#calculate rsi
window_size_rsi = 14
change_price = []
gain = []
loss = []
for a in range(1, len(my_data)):    
        current_change_price = [float(my_data[a][5]) - float(my_data[a-1][5])]
        change_price.append(current_change_price)

for price in change_price:
      for b in price:
            if float(b) > 0:
                  gain.append(float(b))
            else:
                  gain.append(0)

for price in change_price:
      for b in price:
            if float(b) < 0:
                  loss.append(-float(b))
            else:
                  loss.append(0)

gain_sum = 0
for i in range(0,14):
      gain_sum += gain[i]
      

average_gain = gain_sum / 14

loss_sum = 0
for i in range(0,14):
      loss_sum += loss[i]

average_loss = loss_sum / 14

average_gain_data = []
average_loss_data = []
average_gain_data.append(average_gain)
average_loss_data.append(average_loss)


for i in range(14, len(my_data)):
    if len(gain) > i:
        next_avg_gain = ((average_gain_data[-1] * 13) + gain[i]) / 14
        average_gain_data.append(next_avg_gain)
    else:
        break
       
for i in range(14, len(my_data)):
      if len(loss) > i:
            next_avg_loss = ((average_loss_data[-1] * 13) + loss[i]) / 14
            average_loss_data.append(next_avg_loss)
      else:
            break

rs = []
rsi_values = []          
for i in range(0, len(my_data)-14):
      rs = (average_gain_data[i] / average_loss_data[i]) if average_loss_data[i] != 0 else float('inf')
      rsi = 100 - (100 / (1 + rs))
      rsi_values.append(rsi)
      
   
#task 3
with open("orcl-sma.csv", "w", newline="") as sma_file:
      sma_writer = csv.writer(sma_file, delimiter=';')
      sma_writer.writerow(["Date", "SMA"])

      for i in range(len(sma_values)):
            date = my_data[i + windows_size - 1][0]
            sma_value = sma_values[i]
            sma_writer.writerow([date, sma_value])


with open("orcl-rsi.csv", "w", newline="") as rsi_file:
      rsi_writer = csv.writer(rsi_file, delimiter=';')
      rsi_writer.writerow(["Date", "RSI"])

      for i in range(14, len(rsi_values)+14):
            date = my_data[i][0]
            rsi_value = rsi_values[i - 14]
            rsi_writer.writerow([date, rsi_value])


