---
title: Java面试算法基础
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [Java, 基础, 面试]
difficulty: 进阶
---

# Java 面试算法基础

> **一句话**:Java 面试算法不考 LeetCode Hard，常考的是排序、查找、链表、二叉树和基本数据结构的思想——能讲清楚原理比手写更重要。

## 排序算法（面得最多）

### 快速排序 ★★★★★

```java
// 核心思想：选 pivot → 小的放左边，大的放右边 → 递归
public void quickSort(int[] arr, int left, int right) {
    if (left >= right) return;
    int pivot = partition(arr, left, right);
    quickSort(arr, left, pivot - 1);
    quickSort(arr, pivot + 1, right);
}

int partition(int[] arr, int left, int right) {
    int pivot = arr[left];  // 选最左为基准
    int i = left, j = right;
    while (i < j) {
        while (i < j && arr[j] >= pivot) j--;  // 从右找比 pivot 小的
        while (i < j && arr[i] <= pivot) i++;  // 从左找比 pivot 大的
        if (i < j) swap(arr, i, j);             // 交换
    }
    swap(arr, left, i);  // pivot 归位
    return i;
}
// 时间：O(n log n) 平均，O(n²) 最坏（逆序数组）
// 空间：O(log n) 递归栈
// 不稳定排序
```

### 归并排序 ★★★★

```java
// 核心思想：分治 → 递归拆到单个元素 → 合并有序数组
public void mergeSort(int[] arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;  // 防溢出
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

void merge(int[] arr, int left, int mid, int right) {
    int[] temp = new int[right - left + 1];
    int i = left, j = mid + 1, k = 0;
    while (i <= mid && j <= right) {
        temp[k++] = arr[i] <= arr[j] ? arr[i++] : arr[j++];
    }
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    System.arraycopy(temp, 0, arr, left, temp.length);
}
// 时间：O(n log n) 稳定
// 空间：O(n) — 需要临时数组
// 稳定排序
```

### 排序对比速查

| 算法 | 时间(平均) | 时间(最坏) | 空间 | 稳定 | 场景 |
|------|:--:|:--:|:--:|:--:|------|
| **快排** | O(n log n) | O(n²) | O(log n) | ❌ | **最常用**，内存中排序首选 |
| **归并** | O(n log n) | O(n log n) | O(n) | ✅ | 外部排序、链表排序 |
| 堆排 | O(n log n) | O(n log n) | O(1) | ❌ | Top K 问题 |
| 冒泡 | O(n²) | O(n²) | O(1) | ✅ | 教学用 |
| 插入 | O(n²) | O(n²) | O(1) | ✅ | 小数据量、基本有序时很快 |

## 查找算法

### 二分查找 ★★★★★

```java
// 前提：数组有序
public int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // 防溢出，不用 (left+right)/2
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
// 时间：O(log n)
```

### 变体 — 找第一个等于 target 的位置

```java
// 数组有重复元素时
while (left < right) {
    int mid = left + (right - left) / 2;
    if (arr[mid] >= target) right = mid;  // 往左收缩
    else left = mid + 1;
}
return arr[left] == target ? left : -1;
```

## 链表

### 反转链表 ★★★★★

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;  // 暂存下一个
        curr.next = prev;            // 反转指针
        prev = curr;                 // prev 前进
        curr = next;                 // curr 前进
    }
    return prev;
}
```

### 检测环（快慢指针）★★★★

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;  // 追上了 → 有环
    }
    return false;
}
```

## 二叉树

### 三种遍历（递归 + 迭代我都要会）

```java
// 前序：根 → 左 → 右
void preOrder(TreeNode root) {
    if (root == null) return;
    System.out.print(root.val + " ");
    preOrder(root.left);
    preOrder(root.right);
}

// 中序：左 → 根 → 右  （BST 中序遍历是有序的！）
void inOrder(TreeNode root) {
    if (root == null) return;
    inOrder(root.left);
    System.out.print(root.val + " ");
    inOrder(root.right);
}

// 后序：左 → 右 → 根
void postOrder(TreeNode root) {
    if (root == null) return;
    postOrder(root.left);
    postOrder(root.right);
    System.out.print(root.val + " ");
}
```

### 层序遍历（BFS）★★★★

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

## 常用数据结构的选择

| 场景 | 选什么 | 原因 |
|------|--------|------|
| 频繁增删 | **LinkedList** | 插入 O(1)，ArrayList 要搬数据 |
| 频繁随机访问 | **ArrayList** | 下标访问 O(1) |
| 需要排序+快速查找 | **TreeMap/TreeSet** | 红黑树，O(log n) 有序 |
| 只需快速查找 | **HashMap/HashSet** | 哈希，O(1) |
| 线程安全 Map | **ConcurrentHashMap** | CAS+synchronized，比 HashTable 快 |
| LIFO | **Deque(Stack 已废弃)** | push/pop |
| FIFO | **Queue(LinkedList 实现)** | offer/poll |
| 有界阻塞 | **ArrayBlockingQueue** | 线程池标配 |

## 常见算法思想

| 思想 | 核心 | 典型题 |
|------|------|--------|
| **双指针** | 一快一慢、一左一右 | 链表环检测、两数之和、接雨水 |
| **滑动窗口** | 窗口右扩左缩维持条件 | 最长无重复子串 |
| **二分** | 每次排除一半，不一定要有序 | 旋转数组找最小值 |
| **分治** | 拆成子问题，合并结果 | 归并排序、快排 |
| **贪心** | 每步选最优，不回溯 | 跳跃游戏、分发饼干 |
| **DP** | 状态+转移方程+base case | 背包、最长公共子序列 |
| **回溯** | 试探→失败→回退 | 全排列、N 皇后 |

## 面试话术

「算法部分我主要准备的是快排、归并、二分、链表反转、二叉树遍历——这些是 Java 面试出现频率最高的。我的策略是先讲清楚思路，再写代码。比如快排，核心就是 partition 把 pivot 归位然后分治——讲明白了思路，代码是水到渠成的。」

### 追问：Arrays.sort() 底层用的什么？

「Java 对基本类型用的是双轴快排（Dual-Pivot QuickSort），对对象类型用的是 TimSort（归并+插入的混合）。选快排是因为基本类型不需要稳定性，TimSort 是对对象需要稳定性且利用了部分有序的特点。」
