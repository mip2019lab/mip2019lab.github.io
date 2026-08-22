import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 数据
dates = ['2022-03', '2022-11', '2024-03', '2024-11', '2025-03', '2025-11']
values = [0.7, 0.56, 0.44, 0.38, 0.37, 0.33]

# 转换日期格式
date_objects = [datetime.strptime(d, '%Y-%m') for d in dates]

# 创建图表
plt.figure(figsize=(10, 6))
plt.plot(date_objects, values, marker='>', markersize=10, linewidth=2.5, color='#FF7F0E')

# 添加数据标签
for i, (date, value) in enumerate(zip(date_objects, values)):
    plt.annotate(f'{value}', 
                xy=(date, value),
                xytext=(5, 0),
                textcoords='offset points',
                fontsize=12,
                color='red' if i == len(values)-1 else 'black')

# 设置坐标轴
plt.ylim(0.2, 0.8)
plt.yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])

# 格式化x轴
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 11)))

# 添加标题和标签
plt.title('ESI排名情况', fontsize=20, pad=20)
plt.grid(True, linestyle='-', alpha=0.3)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()
