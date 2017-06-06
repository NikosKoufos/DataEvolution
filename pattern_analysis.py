import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt

# Read the data files
data = pd.read_csv("tables.txt")
metrics = pd.read_csv("metrics.txt")
stats = pd.read_csv("table_stats.txt")

attributes = []
tables = []
total_changes = []

for i in range(data.shape[1]-2):
    attributes.append(sum(data[str(i)]))
    tmp = [x for x in data[str(i)] if x != 0]
    tables.append(len(tmp))

for i in range(metrics.shape[0]):
    total_changes.append(sum(metrics.ix[i,'tIns':]))

# Count the percentage in 10x10 box for comet pattern
counter = 0
for i in range(stats.shape[0]):
    if stats.ix[i,'s@s'] <=10 and stats.ix[i,'chngs'] <=10:
        counter +=1

# Count the dead tables
# does not double-count revived tables
counter_dead = 0
for i in range(data.shape[0]-2):
    zero_pos = -1
    tmp = list(data.iloc[i, 1:-1])
    for j in range(len(tmp)):
        if tmp[j] != 0:
            zero_pos = j
        else:
            if zero_pos != -1:
                zero_pos = -1
                counter_dead += 1

#Plots for the patterns, replace x, y and data to your will
plot = sb.regplot(x='birth', y='dur', data=stats, fit_reg=False)
plot.set(xlim=(-1.5, None), ylim=(-1.5, None))
plot.set_xlabel('Birth', fontsize=15)
plot.set_ylabel('Duration', fontsize=15)
plot.axes.set_title("Empty Triangle Pattern", fontsize=25)
sb.plt.show()

# Statistics for the activity
zero = 0
quiet = 0
mid = 0
high = 0
for change in total_changes:
    if change == 0:
        zero += 1
    elif change <= 5:
        quiet += 1
    elif change <= 15:
        mid += 1
    else:
        high += 1

print(zero, quiet, mid, high)
print(zero/len(total_changes), quiet/len(total_changes), mid/len(total_changes), high/len(total_changes))

# Plot for Tables, Attributes and Changes over Versions
# Replace the y_val with either tables, attributes or total_changes for the respective plot
plt.style.use('ggplot')
x_val = range(0,len(total_changes))
y_val = total_changes
plt.plot(x_val, y_val)
plt.xlabel('Versions', fontsize=15)
plt.ylabel('Sum of Changes', fontsize=15)
plt.title('Changes Over Versions', fontsize=25)
plt.show()