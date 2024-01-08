import csv

file_path = "C:/Users/EMRE/Downloads/csv_file/orcl.csv"

with open(file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        historical_data = list(csv_reader)  # I converted it into a list.

len(historical_data)

print(historical_data)

sum_close = 0.0
for elements in historical_data:
    close_data = float(elements["Close"])
    sum_close += close_data # found the total close numbers and I know the days (5787)

SMA = (sum_close / 5787) * 5 # found the Simple Moving Averages for a 5-day window.

print(SMA)

total_gain = 0.0
total_loss = 0.0

for element in historical_data:
    if float(element["Open"]) == float(element["Close"]):
        pass
    elif float(element["Open"]) < float(element["Close"]):
        total_gain += float(element["Close"]) - float(element["Open"])
    elif float(element["Open"]) > float(element["Close"]):  
        total_loss += float(element["Open"]) - float(element["Close"])
print(total_gain)
print(total_loss)

average_gain_14 = (total_gain / 5787) * 14 # actually I watched many videos about RSI but NONE of them mentioned past and current average.
average_loss_14 = (total_loss / 5787) * 14
print(average_gain_14)
print(average_loss_14)

RSI = 100 - (100 / ( 1 + (average_gain_14 / average_loss_14 )))  # found the RSI

print(RSI)

with open("orcl-sma.csv","w") as write_file:
    write_file.write("Simple Moving Averages for a 5-day window is : " + str(SMA))
with open("orcl-rsi.csv.", "w") as write_file:
    write_file.write("Relative Strength Index (RSI) for a 14-day window is : " + str(RSI))