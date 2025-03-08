#### [搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)

* 编写一个高效的算法来搜索 `*m* x *n*` 矩阵 `matrix` 中的一个目标值 `target` 。该矩阵具有以下特性：

  - 每行的元素从左到右升序排列。

  - 每列的元素从上到下升序排列。

    ```java
    class Solution {
        public boolean searchMatrix(int[][] matrix, int target) {
            //从最后一排比较即可，只要最后一排小于他，左边全部排除掉
            //不小于他，意味着最后竖列比他大，擦除下面的竖列
            //移动至右边第二排，按照第一个逻辑再判断
            //控制列
            int index=matrix[0].length-1;
            //控制行
            int i = 0;
            while (i< matrix.length && index>=0){
                if (matrix[i][index]==target){
                    return true;
                }
                //左边全不行
                if (matrix[i][index]<target){
                    i++;
                }
                //竖列全部不行，往左移动
                else {
                    index--;
                }
            }
            return false;
        }
    }
    ```

    