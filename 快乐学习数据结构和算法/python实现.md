###  list和tuple
参考文章：
- python列表和元组：https://www.jianshu.com/p/24090fb63968
- python实现单链表，看看就行屁用没有：https://m.yisu.com/zixun/158827.html
- python list原理：https://zhuanlan.zhihu.com/p/143223943


问题：
- 1、python内部的数组是如何实现的？

```
# cpython中list的定义
typedef struct {
    PyObject_VAR_HEAD
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;
```
首先python中的数组是`动态数组`，基本由cpython实现，PyObject是指向列表元素的指针列表，allocated是在内存中分配的插槽数，一般插槽数大于len，这样添加元素时，如果插槽数还剩余就不用申请空间；一旦超过，就需要申请新的空间，每次申请的插槽数不一样，以某种规律增长。
```
# resize
arguments: list object, new size
returns: 0 if OK, -1 if not
list_resize:
    new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6) = 3
    new_allocated += newsize = 3 + 1 = 4
    resize ob_item (list of pointers) to size new_allocated
    return 0
# >>：移位运算符
# condition ? value1: value2: 条件判断府，如果符合就是value1，不然value2
```
其次复杂度分析，Appand 操作的时间复杂度 O(1)，Insert 操作的复杂度为O(n)，Pop 操作的复杂度为 O(1)，Remove操作的复杂度为O(n)，都挺好理解的，但是值得注意的是`当删除元素导致列表元素数量小于插槽数一半的时候，插槽数也会减少，即预设的内存会减少`

- 2、python可以实现内存申请吗，像c语言中的数组一样？

在python中tuple很像c语言的数组，创建后不可删除，修改；但是可以实现两个元组的合并，逻辑也很简单，新创建一个元组，读取已有元组中的元素复制到新元组中；元组相较于数组，除了保证数据安全外， 是更加内存友好的结构，即`占用内存更少、创建速度更快、与python普通回收不同，元组删除后，内存不会立刻返回给os暂留，可避免频繁与os交互`（这应该是优势吧？暂留真的不会影响效率吗？）

list各种操作的时间复杂度
```
index O(1)
pop O(1)
max/min O(k)
in O(n)
len O(1)
sort O(nlogn)
```
