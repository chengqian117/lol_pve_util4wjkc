import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# 生成随机二维点
def generate_random_points(num_points, xlim, ylim):
    np.random.seed(0)
    x = np.random.uniform(xlim[0], xlim[1], num_points)
    y = np.random.uniform(ylim[0], ylim[1], num_points)
    return np.vstack((x, y)).T

# 绘制点和簇
def plot_clusters(points, labels, cluster_centers):
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

    plt.figure(figsize=(12, 8))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # 用黑色表示噪声点
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = points[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        if k != -1:
            center = cluster_centers[k]
            plt.plot(center[0], center[1], 'o', markerfacecolor=tuple(col),
                     markeredgecolor='k', markersize=18)
            circle = plt.Circle((center[0], center[1]), 5, color=col, fill=False, linestyle='--')
            plt.gca().add_artist(circle)

    plt.title('估计的簇数量: %d' % len(unique_labels))
    plt.xlabel('X轴')
    plt.ylabel('Y轴')
    plt.show()

# 主函数
def main():
    num_points = 50
    xlim = (0, 100)
    ylim = (0, 100)

    points = generate_random_points(num_points, xlim, ylim)

    # DBSCAN 聚类
    clustering = DBSCAN(eps=5, min_samples=1).fit(points)
    labels = clustering.labels_

    # 计算簇中心
    unique_labels = set(labels)
    cluster_centers = np.array([points[labels == k].mean(axis=0) for k in unique_labels if k != -1])

    plot_clusters(points, labels, cluster_centers)

if __name__ == "__main__":
    main()
