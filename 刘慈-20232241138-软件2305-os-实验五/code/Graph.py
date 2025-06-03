import matplotlib.pyplot as plt

# 页面访问序列
reference_string = [
    0, 1, 2, 0, 3, 4, 2, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
]
# 页面数量
num_frames = list(range(2, 22))  # 从2到21，共20个数据点

# 初始化结果存储
results = {
    'FIFO': [],
    'LFU': [],
    'MFU': [],
    'LRU': [],
    'Clock': [],
    'EClock': []
}

# FIFO算法
def fifo_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
            else:
                current_frames.pop(0)
                current_frames.append(page)
    return page_faults

# LFU算法
def lfu_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    frequency = {}
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
                frequency[page] = 1
            else:
                min_freq = float('inf')
                min_page = None
                for frame in current_frames:
                    if frequency[frame] < min_freq:
                        min_freq = frequency[frame]
                        min_page = frame
                current_frames.remove(min_page)
                del frequency[min_page]
                current_frames.append(page)
                frequency[page] = 1
        else:
            frequency[page] += 1
    return page_faults

# MFU算法
def mfu_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    frequency = {}
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
                frequency[page] = 1
            else:
                max_freq = -1
                max_page = None
                for frame in current_frames:
                    if frequency[frame] > max_freq:
                        max_freq = frequency[frame]
                        max_page = frame
                current_frames.remove(max_page)
                del frequency[max_page]
                current_frames.append(page)
                frequency[page] = 1
        else:
            frequency[page] += 1
    return page_faults

# LRU算法
def lru_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    access_order = []  # 用于记录页面的访问顺序
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
                access_order.append(page)
            else:
                # 替换最久未访问的页面
                oldest_page = access_order.pop(0)
                current_frames.remove(oldest_page)
                current_frames.append(page)
                access_order.append(page)
        else:
            # 更新访问顺序
            access_order.remove(page)
            access_order.append(page)
    return page_faults

# Clock算法
def clock_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    used = {}
    pointer = 0
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
                used[page] = False
            else:
                while used[current_frames[pointer]]:
                    used[current_frames[pointer]] = False
                    pointer = (pointer + 1) % frames
                removed_page = current_frames.pop(pointer)
                del used[removed_page]
                current_frames.insert(pointer, page)
                used[page] = False
                pointer = (pointer + 1) % frames
        else:
            used[page] = True
    return page_faults

# EClock算法
def eclock_algorithm(frames, reference_string):
    page_faults = 0
    current_frames = []
    used = {}
    modified = {}
    pointer = 0
    for page in reference_string:
        if page not in current_frames:
            page_faults += 1
            if len(current_frames) < frames:
                current_frames.append(page)
                used[page] = False
                modified[page] = False
            else:
                while used[current_frames[pointer]] or modified[current_frames[pointer]]:
                    if used[current_frames[pointer]]:
                        used[current_frames[pointer]] = False
                    elif modified[current_frames[pointer]]:
                        modified[current_frames[pointer]] = False
                        used[current_frames[pointer]] = True
                    pointer = (pointer + 1) % frames
                removed_page = current_frames.pop(pointer)
                del used[removed_page]
                del modified[removed_page]
                current_frames.insert(pointer, page)
                used[page] = False
                modified[page] = False
                pointer = (pointer + 1) % frames
        else:
            used[page] = True
            modified[page] = True
    return page_faults

# 计算每种算法在不同页面帧数量下的页面置换次数
for frames in num_frames:
    results['FIFO'].append(fifo_algorithm(frames, reference_string))
    results['LFU'].append(lfu_algorithm(frames, reference_string))
    results['MFU'].append(mfu_algorithm(frames, reference_string))
    results['LRU'].append(lru_algorithm(frames, reference_string))
    results['Clock'].append(clock_algorithm(frames, reference_string))
    results['EClock'].append(eclock_algorithm(frames, reference_string))

# 绘制曲线图
plt.figure(figsize=(14, 7))
for algorithm, page_faults in results.items():
    plt.plot(num_frames, page_faults, marker='o', linestyle='-', label=algorithm)

plt.title('Page Faults Comparison (FIFO, LFU, MFU, LRU, Clock, EClock)')
plt.xlabel('Number of Frames')
plt.ylabel('Number of Page Faults')
plt.legend()
plt.grid(True)
plt.show()