import csv

#Task-1: Load the historical data from the file orcl.csv into a list of dictionaries
with open('orcl.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = [row for row in csv_reader]

#print(data[0]['Date'])

#Task-2: Calculate two technical indicators:
sma = []
close = []

for i in range(len(data)):

    if i % 5 == 0 and i != 0:
        sma.append(sum(close)/5)
        close.clear()
        current_element = float(data[i]['Close'])
        close.append(current_element)
    else:
        current_element = float(data[i]['Close'])
        close.append(current_element)

close.clear()

pc = []  # Price changes
rsi = []
gain = []
loss = []

for i in range(len(data)):

    if i == 5786:
        break
    else:
        c_price = float(data[i+1]['Close']) - float(data[i]['Close'])
        if c_price < 0:
            loss.append(c_price)
            gain.append(0)
        else:
            gain.append(c_price)
            loss.append(0)


avg_gain = []
gain_list = []
avg_loss = []
for i in range(len(gain)):
    if i % 14 == 0 and i != 0:
        avg_gain.append(sum(gain_list)/14)
        gain_list.clear()
        gain_list.append(gain[i])
    else:
        gain_list.append(gain[i])


loss_list = []
for i in range(len(loss)):
    if i % 14 == 0 and i != 0:
        avg_loss.append(sum(loss_list)/14)
        loss_list.clear()
        loss_list.append(loss[i])
    else:
         loss_list.append(loss[i])


rsi = 100-(100 / (1 + ( sum(avg_gain) / sum(avg_loss) )))
print(rsi)


#Task-3: Write each indicatortoafile: Moving Averages to the file orcl-sma.csvand RSIto the file orcl-rsi.csv
with open ('orcl-sma.csv','w') as f:
    write = csv.writer(f)

    write.writerow(sma)

with open ('orcl-rsi.csv','w') as f:
    write = csv.writer(f)
    write.writerow([rsi])