---
layout: default
title: Lab 2
nav_order: 3
---

# CSCI 3212 Lab 2: Sorting Logic and Implementation

In this lab, you will trace Bubble Sort and Insertion Sort, implement Lomuto
partitioning, practice the merge step of Merge Sort, and use an array-based
min-heap to implement Heapsort.

Bubble Sort and Insertion Sort are **trace exercises only**. Their code is
provided below; you do not need to implement either algorithm. This lab uses
Lomuto partitioning only.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `quicksort_practice.py` | Implement `lomuto_partition`; Quicksort is provided |
| `mergesort_practice.py` | Implement `merge`; recursive Merge Sort is provided |
| `heapsort_practice.py` | Implement `min_heapify_down` and complete `heap_sort`; heap construction is provided |
| `lab_checks.py` | Provided checks; do not edit |

- [ ] Part 1: Bubble Sort and Insertion Sort traces and short answers.
- [ ] Part 2: Lomuto trace, partition implementation, and short answers.
- [ ] Part 3: Merge Sort trace, merge implementation, and short answer.
- [ ] Part 4: Heap representation, sift-down trace, and Heapsort implementation.
- [ ] Run all three practice files and resolve all failed checks.

Keep the function names and parameters unchanged. Do not use `sorted`,
`list.sort`, or `heapq` to implement the required functions. The provided checks
use `sorted` only to verify results.

## Part 1: Bubble Sort and Insertion Sort

Count only **comparisons between element values**. Do not count loop bounds or
index checks such as `j >= 0`. Count a failed element comparison when it is
actually evaluated. Count each adjacent exchange as one swap and each move of
an existing element one position right as one shift. Placing the saved key is
not a shift.

### 1.1 Bubble Sort: trace only

Each pass compares neighboring elements. If they are out of order, it swaps
them. After each completed pass, the largest remaining unsorted element is in
its final position. After `k` passes, the last `k` positions form a sorted suffix.
If a pass makes no swaps, the entire array is sorted and the algorithm stops.

```python
def bubble_sort(arr):
  n = len(arr)
  for i in range(n):
    swapped = False
    for j in range(0, n - i - 1):
      if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        swapped = True
    if not swapped:
      break
  return arr
```

#### Key Mechanics:
1. **The "Bubbling" Effect**: In each pass $i$ (from $0$ to $n-1$), the largest unsorted element "bubbles up" to its correct final position at index $n - 1 - i$.
2. **Loop Invariant**: After pass $k$, the suffix `arr[n-k .. n-1]` consists of the $k$ largest elements in the array in their final, sorted positions.
3. **Early-Stopping Optimization**: The `swapped` boolean flag detects if an entire pass completed without a single swap. If no swaps occurred, the array is already sorted, allowing Bubble Sort to terminate in $O(n)$ time on pre-sorted input.

> ### Task 1.1: Trace Bubble Sort Logic
> 
> Trace Bubble Sort manually on the array: `arr = [5, 2, 9, 1, 5, 6]` ($n = 6$).
> 
> Pass 1 is filled in below as a worked example. **Fill in the remaining passes (Pass 2, Pass 3, and Pass 4)** in the table below:
> 
> | Pass | Scanning Range | Comparison ($arr[j]$ vs $arr[j+1]$) | Action | Array State | Sorted Suffix |
> |---|---|---|---|---|---|
> | **1 (Example)** | $j=0 \dots 4$ | $5 > 2$ | SWAP | `[2, 5, 9, 1, 5, 6]` | |
> | | | $5 \le 9$ | KEEP | `[2, 5, 9, 1, 5, 6]` | |
> | | | $9 > 1$ | SWAP | `[2, 5, 1, 9, 5, 6]` | |
> | | | $9 > 5$ | SWAP | `[2, 5, 1, 5, 9, 6]` | |
> | | | $9 > 6$ | SWAP | `[2, 5, 1, 5, 6, 9]` | `[9]` |
> | **2 (TODO)** | $j=0 \dots 3$ | $arr[0]$ vs $arr[1]$: | | | |
> | | | $arr[1]$ vs $arr[2]$: | | | |
> | | | $arr[2]$ vs $arr[3]$: | | | |
> | | | $arr[3]$ vs $arr[4]$: | | `[                      ]` | `[       ]` |
> | **3 (TODO)** | $j=0 \dots 2$ | $arr[0]$ vs $arr[1]$: | | | |
> | | | $arr[1]$ vs $arr[2]$: | | | |
> | | | $arr[2]$ vs $arr[3]$: | | `[                      ]` | `[          ]` |
> | **4 (TODO)** | $j=0 \dots 1$ | $arr[0]$ vs $arr[1]$: | | | |
> | | | $arr[1]$ vs $arr[2]$: | | `[                      ]` | `[             ]` |
> | **Exit** | Did any swaps occur in Pass 4? Explain early stopping: | | | `[                      ]` | **Sorted!** |
> 
> ```text
> Total Comparisons performed: 
> Total Swaps performed: 
> ```
> *(Tip: You can verify your trace by running `python sorting_trace.py`)*

---

### 1.2 Insertion Sort: trace only

At the start of iteration `i`, positions `0` through `i - 1` are sorted.
Save `arr[i]` as `key`, shift larger elements right, and place `key` into the
gap. Saving `key` matters because shifting can overwrite its original slot.

```python
def insertion_sort(arr):
  for i in range(1, len(arr)):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
      arr[j + 1] = arr[j]
      j -= 1
    arr[j + 1] = key
  return arr
```

#### Key Mechanics:
1. **Loop Invariant**: At the start of iteration $i$, the prefix `arr[0 .. i-1]` contains the original elements from those positions, but in sorted order.
2. **Inversion Sensitivity**: An inversion is a pair $(i, j)$ such that $i < j$ and $arr[i] > arr[j]$. The total number of shifts in Insertion Sort is **exactly equal** to the number of inversions in the array.
3. **Adaptive**: If the array is already sorted, each `key` is compared once ($arr[i-1] \le arr[i]$) and 0 shifts occur, yielding an $O(n)$ best-case runtime without needing an extra flag.

> ### Task 1.2: Trace Insertion Sort Logic
> 
> Trace Insertion Sort manually on the array: `arr = [7, 3, 5, 8, 2]` ($n = 5$).
> 
> Step $i=1$ is filled in below as a worked example. **Complete Steps $i=2$, $i=3$, and $i=4$**:
> 
> | Step $i$ | Key ($arr[i]$) | Comparisons & Shifts | Insertion Action | Resulting Array State | Sorted Prefix |
> |---|---|---|---|---|---|
> | **Init** | - | - | Prefix of length 1 is sorted | `[7, 3, 5, 8, 2]` | `[7]` |
> | **$i=1$ (Example)** | `3` | $7 > 3 \to$ shift $7$ right | Place `3` at index 0 | `[3, 7, 5, 8, 2]` | `[3, 7]` |
> | **$i=2$ (TODO)** | `5` | | | `[               ]` | `[         ]` |
> | **$i=3$ (TODO)** | `8` | | | `[               ]` | `[            ]` |
> | **$i=4$ (TODO)** | `2` | | | `[               ]` | `[               ]` |
> 
> ```text
> Total Comparisons performed: 
> Total Shifts performed: 
> ```

---

### 1.3 Algorithm Stability & Inversions

A sorting algorithm is **stable** if elements with equal keys appear in the output in the same relative order as in the initial input.
* **Bubble Sort is Stable**: We swap only when `arr[j] > arr[j + 1]`. When `arr[j] == arr[j + 1]`, no swap occurs. Equal elements never cross each other.
* **Insertion Sort is Stable**: The inner shift loop continues while `arr[j] > key`. When `arr[j] == key`, shifting stops, placing `key` immediately to the right of its equal predecessor.
* **Breaking Stability**: If either comparison is changed to `>=` instead of `>`, equal elements will swap past each other, destroying stability!

> ### Task 1.3: Sorting Analysis Questions
> 
> Answer the following in your lab notes or submission:
> 
> ```text
> TODO 1.3A (Inversions & Shifts):
> List all inversions (pairs of indices (i, j) where i < j and arr[i] > arr[j])
> in the initial array [7, 3, 5, 8, 2]:
> - Inversions: 
> - Total number of inversions: 
> - Does this total exactly equal the number of shifts you counted in Task 1.2? (Yes/No): 
> 
> TODO 1.3B (Early Stopping Flag):
> Why does Bubble Sort require an explicit boolean flag (`swapped`) to achieve
> O(N) best-case time on sorted data, whereas Insertion Sort naturally achieves O(N) without any flag?
> A: 
> 
> TODO 1.3C (Stability):
> If a programmer changes line 33 of Bubble Sort to `if arr[j] >= arr[j + 1]:`,
> does the algorithm still produce a sorted array? Does it remain stable? Explain why or why not.
> A: 
> ```

---

## Part 2: Lomuto Partition Scheme

Quicksort relies on a **partition function** that picks a pivot element $x$ and rearranges `arr[low .. high]` such that:
- All elements $\le x$ are placed to the left of $x$.
- All elements $> x$ are placed to the right of $x$.
- The pivot $x$ is placed at its final sorted index $p$.

The **Lomuto Partition Scheme** (introduced by Nico Lomuto and featured in the CLRS textbook) uses the last element `arr[high]` as the pivot.

```text
LOMUTO-PARTITION(arr, low, high)
  pivot = arr[high]
  i = low - 1
  for j from low through high - 1
    if arr[j] <= pivot
      increment i
      swap arr[i] with arr[j]
  swap arr[i + 1] with arr[high]
  return i + 1
```

### 2.1 Trace partitioning

**TODO 2.1:** Use `[2, 8, 7, 1, 3, 5, 6, 4]`, `low = 0`, `high = 7`.
The pivot is 4. Each row records the state **after** processing `j`.
A swap with the same index is allowed and leaves the array unchanged.

| `j` | Value examined | <= 4? | Swap indices, or none | `i` afterward | Array afterward |
|---|---|---|---|---|---|
| Initial | N/A | N/A | None | -1 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 0 | 2 | Yes | 0 and 0 | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 1 | TODO | TODO | TODO | TODO | TODO |
| 2 | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO |
| 4 | TODO | TODO | TODO | TODO | TODO |
| 5 | TODO | TODO | TODO | TODO | TODO |
| 6 | TODO | TODO | TODO | TODO | TODO |
| Final pivot swap | N/A | N/A | TODO | N/A | TODO |

Record the returned pivot index and the left and right subarrays.

### 2.2 Implement partitioning

**TODO 2.2:** Complete `lomuto_partition` in `quicksort_practice.py`.
Modify the supplied list in place, touch only positions `low` through `high`,
and return the pivot's final index. Use the supplied pseudocode.

The provided `quick_sort` calls your function, then sorts `low` through `p - 1`
and `p + 1` through `high`. The pivot is excluded because it is already placed.

```bash
python3 quicksort_practice.py
```

### 2.3 Short answers

**TODO 2.3A:** Why is the pivot excluded from the scanning loop? Why do we need
the final swap?

**TODO 2.3B:** For `[5, 5, 5, 5, 5]`, find the final `i`, returned pivot index,
and sizes of the two recursive subproblems. Explain why repeating this split
leads to O(n²) Quicksort time. What split occurs on ascending, distinct values
when the last element is always chosen as pivot?

## Part 3: Merge Sort

Merge Sort splits a list into two smaller lists, recursively sorts them, and
merges the sorted results. A list with zero or one element is already sorted.
The split makes the problems smaller; the merge step puts values in order.

```text
MERGE-SORT(arr)
  if length(arr) <= 1
    return a copy of arr
  mid = length(arr) // 2
  left = MERGE-SORT(elements before mid)
  right = MERGE-SORT(elements from mid onward)
  return MERGE(left, right)

MERGE(left, right)
  create an empty result list
  i = 0, j = 0
  while i < length(left) and j < length(right)
    if left[i] <= right[j]
      append left[i] to result; increment i
    otherwise
      append right[j] to result; increment j
  append all remaining elements of left, starting at i
  append all remaining elements of right, starting at j
  return result
```

### 3.1 Trace splitting and merging

**TODO 3.1A:** Start with `[7, 2, 6, 3]`. Write the two halves, the single-element
lists, the two sorted pairs, and the final sorted list.

Worked merge example: merging `[2, 7]` and `[3, 6]` takes 2, then 3, then 6.
The right list is exhausted, so the remaining 7 is appended.

**TODO 3.1B:** Trace merging `[2, 5, 8]` and `[1, 5, 9]`. Choose from the left
list on equal values. `i` and `j` below are their values before the comparison.

| `i` | `j` | Values compared | Take from left or right? | Result so far |
|---|---|---|---|---|
| 0 | 0 | 2 and 1 | Right | `[1]` |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |

Which list has elements remaining, and what is appended after the loop?

### 3.2 Implement merging

**TODO 3.2:** Complete `merge` in `mergesort_practice.py`. Inputs are already
sorted. Return a new sorted list containing every input element, including
duplicates. Do not modify either input. Use indices to advance through the
lists, and take from the left when values are equal.

The recursive `merge_sort` function is provided. In Python, `arr[:mid]` creates
a list of elements before `mid`; `arr[mid:]` creates a list from `mid` to the
end. You do not need to rewrite this function.

```bash
python3 mergesort_practice.py
```

**TODO 3.2A:** Why must `merge` copy the remaining elements after one input is
exhausted? What goes wrong if the function returns immediately after its main
comparison loop?

For context, merging n total elements takes O(n) time. Merge Sort has O(log n)
splitting levels and O(n) merging work per level, giving O(n log n) time.
The provided list-based version uses O(n) peak auxiliary space.

## Part 4: Array-Based Heaps and Heapsort

A binary heap is a **complete binary tree**: every level except possibly the
last is full, and the last level fills from left to right. In a **min-heap**,
each parent is at most as large as its children. The root is therefore a
minimum, but the array itself need not be sorted.

Store the tree in level order in a list. This lab uses 0-based indices only.

| Relationship | Index |
|---|---|
| Root | `0` |
| Left child of `i` | `2 * i + 1` |
| Right child of `i` | `2 * i + 2` |
| Parent of `i`, for `i > 0` | `(i - 1) // 2` |

A child exists in the active heap only if its index is less than `heap_size`.
The root has no parent; do not apply the parent formula to it.

### 4.1 Read an array as a heap

For `[4, 10, 8, 30, 15, 20, 16]`, the levels are:

| Level | Indices | Values |
|---|---|---|
| 0 | 0 | 4 |
| 1 | 1, 2 | 10, 8 |
| 2 | 3, 4, 5, 6 | 30, 15, 20, 16 |

**TODO 4.1:** Find the child indices and values of index 1, the parent index and
value of index 6, and all leaf indices. Is this a min-heap? Explain using the
parent-child comparisons, not whether the list looks sorted.

### 4.2 Restore the heap with sift-down

Sift-down repairs a node that may be larger than one of its children.
**Its child subtrees must already be min-heaps.** Compare the current node
with its existing children. If a child is smaller, swap with the smaller child
and continue from that child's index. Stop when no swap is needed.

```text
MIN-HEAPIFY-DOWN(arr, i, heap_size)
  repeat
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < heap_size and arr[left] < arr[smallest]
      smallest = left
    if right < heap_size and arr[right] < arr[smallest]
      smallest = right
    if smallest == i
      stop
    swap arr[i] with arr[smallest]
    i = smallest
```

**TODO 4.2A:** Trace sift-down on `[25, 10, 8, 30, 15, 20, 16]`, starting at
`i = 0`, with `heap_size = 7`. Record each swap and resulting array. Explain
why the smaller child must be chosen, and why the process stops.

**TODO 4.2B:** Implement `min_heapify_down` in `heapsort_practice.py`. Modify the
list in place and return `None`. The suffix starting at `heap_size` is outside
the heap and must remain unchanged.

### 4.3 Build the heap and sort

Leaves are already one-node heaps. The last internal node has index
`len(arr) // 2 - 1`. The provided `build_min_heap` works backward from that node
to the root, using your sift-down function. That order ensures each node's
child subtrees are already heaps when it is processed.

Heapsort first builds a min-heap, then repeatedly moves the minimum into its
final position at the end of the active heap. **This version produces
descending order:** the smallest value goes into the last position, the next
smallest goes immediately before it, and so on.

```text
HEAP-SORT(arr)
  BUILD-MIN-HEAP(arr)
  for end from length(arr) - 1 down through 1
    swap arr[0] with arr[end]
    MIN-HEAPIFY-DOWN(arr, 0, end)
  return arr
```

After the swap, `end` is the new heap size: active indices are `0` through
`end - 1`. The sorted suffix begins at `end`. **The list length does not
shrink.** Do not remove elements from the list.

**TODO 4.3A:** Complete the loop body in `heap_sort`. It should sort the original
list in descending order and return that same list object.

```bash
python3 heapsort_practice.py
```

**TODO 4.3B:** Starting with the min-heap `[4, 10, 8, 30, 15, 20, 16]`, perform
one Heapsort extraction: swap the root with the last active element, reduce
the active heap size, and sift down. Record the full array, active heap size,
and sorted suffix afterward. Why must sift-down exclude that suffix?

Heap construction takes O(n) time. Each extraction uses at most O(log n)
sift-down work, so Heapsort takes O(n log n) time overall. The iterative
implementation here uses O(1) auxiliary space.

## Final check

Run all three practice files. Unfinished functions report `[TODO]`; incorrect
results report `[FAIL]`; completed checks report `[PASS]`. Each command exits
with a nonzero status while any check is unfinished or failing. These checks
are examples, so also review your code against the function contracts.

```bash
python3 quicksort_practice.py
python3 mergesort_practice.py
python3 heapsort_practice.py
```
