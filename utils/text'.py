'''
在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。
数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。
```python
   输入：
    [2, 3, 1, 0, 2, 5, 3]
   输出：2 或 3

```

'''


class Solution:
    def findNumberIn2DArray(self, matrix, target):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == target:
                    return True
        else:
            return False


'''
  <div class="pg-header">
        <div class="logo left">后台管理</div>
        <div class="rmenus right">
            <div class="right userss" style="position: relative">
                <a><i class="uuu fa fa-user-circle fa-2x" aria-hidden="true" ></i></a>
                <div class="userinfo" >
                    <a>个人资料</a>
                    <a>注销</a>
                </div>
            </div>
            <a><i class="fa fa-bell" aria-hidden="true"></i>&nbsp;通知</a>
            <a><i class="fa fa-commenting-o" aria-hidden="true"></i>&nbsp;消息</a>
            <a><i class="fa fa-envelope-open" aria-hidden="true"></i>&nbsp;通知</a>

        </div>
    </div>
    <div class="pg-body">
        <div class="menus">
            <a><i class="fa fa-cog" aria-hidden="true"></i>&nbsp;班级管理</a>
            <a><i class="fa fa-cog" aria-hidden="true"></i>&nbsp;学生管理</a>
            <a><i class="fa fa-cog" aria-hidden="true"></i>&nbsp;老师管理</a>


        </div>
        <div class="content">
           <ol class="breadcrumb">
               <li><a href="#">首页</a></li>
               <li><a href="#">班级管理</a></li>
               <li class="active">添加班级</li>
           </ol>
        </div>
    </div>
    
    
    
    
    <div style="width: 900px;margin: auto;">
    <h1>班级列表</h1>
    <div style="margin: 10px">
        <a href="/add_class/" class="btn btn-primary">添加</a>
        <a onclick="showModal() " class="btn btn-default">对话框添加</a>

    </div>
    {# 班级信息表 #}
    <table class="table table-striped table-hover table-bordered" >
        <thead>
            <tr>
                <th>ID</th>
                <th>班级名称</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for row in class_list %}
            <tr>
                <td>{{ row.id }}</td>
                <td>{{ row.title }}</td>
                <td>

                    <a href="/edit_class/?nid={{ row.id }}" class="glyphicon glyphicon-pencil"></a>
                    &nbsp;&nbsp;&nbsp;&nbsp;|
                    <a onclick="return  modelEdit(this)">对话框编辑</a>
                    |&nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="/del_class/?nid={{ row.id }}" class="glyphicon glyphicon-trash"></a>



                </td>
            </tr>

            {% endfor %}
        </tbody>
    </table>
</div>
    {# 对话框添加 #}
    <div id="shadow" class="shadow hide"></div>
    <div id="model" class="modallll hide">
            <p>
                <input  id="title" type="text" name="title">
            </p>
            <input  type="button" value="提交" onclick="AjaxSend();"><span id="errormsg"></span>
            <input type="button" value="取消" onclick="cancelModel();">
    </div>

    {# 对话框编辑 #}
    <div id="editmodel" class="modallll  hide">
            <h2>编辑框</h2>
            <p>
                <input id="editid" type="text" name="id" style="display: none">
                <input  id="edittitle" type="text" name="title">
            </p>
            <input  type="button" value="提交" onclick="editAjaxSend();"><span id="errormsg"></span>
            <input type="button" value="取消" onclick="cancelModelEdit();">
    </div>


    <script src="/static/jquery-3.6.0.js"> {# 导入jquery #}

    </script>
    <script>
        function showModal(){
            document.getElementById('shadow').classList.remove('hide');
            document.getElementById('model').classList.remove('hide');
        }


        function AjaxSend(){
            $.ajax({
                url:'/modal_add_class/',
                type:'POST',
                data:{'title':$('#title').val()},
                success: function (data){
                    // 当服务端处理完成后，返回数据时该函数自动调用
                    // data=服务端返回的值
                    console.log(data);
                    if(data == "ok"){
                        location.href="/classes/";
                    }else{
                        $("#errormsg").text(data);
                    }
                }
            })
        }


        function cancelModel(){
            document.getElementById('shadow').classList.add('hide');
            document.getElementById('model').classList.add('hide');
        }
        function cancelModelEdit(){
            document.getElementById('shadow').classList.add('hide');
            document.getElementById('editmodel').classList.add('hide');
        }



        function modelEdit(self){
            document.getElementById('shadow').classList.remove('hide');
            document.getElementById('editmodel').classList.remove('hide');
            /*
            1. 获取当前点击标签
            2. 当前标签父标签，再找其上方标签
            3. 获取班级当前行班级名称，复制到对话框中
            */
            var row = $(self).parent().prevAll();
            var content = $(row[0]).text();
            $('#edittitle').val(content);
            var contentid = $(row[1]).text();
            $('#editid').val(contentid);
        }
        function editAjaxSend(){
            var nid = $('#editid').val();
            var content = $('#edittitle').val();
            console.log(nid,content);
            $.ajax({
                url: "/model_edit_class/",
                type: "POST",
                data: {'nid':nid,'content':content},
                success:function (arg){
                    // arg是字符串类型
                    // JSON.parse(arg) => 对象
                    // JSON.stringify(对象) => 字符串
                    arg = JSON.parse(arg);
                    if(arg.status){
                        location.reload();
                    }else{
                        alert(arg.message)
                    }
                    console.log(arg);
                }
            })
        }
    </script>






<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/plugins/bootstrap-3.4.1-dist/css/bootstrap.css">
    <style>
        .hide {
            display: none;
        }

        .shadow {
            position: fixed;
            background-color: black;
            opacity: 0.4;
            z-index: 998;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;

        }

        .modelll {
            background-color: white;
            z-index: 1001;
            width: 440px;
            height: 400px;
            position: fixed;
            margin-top: -180px;
            margin-left: 180px;


        }
        .loading{
            position: fixed;
            height: 150px;
            width: 150px;
            top: 50%;
            left: 50%;
            margin-left: -25px;
            margin-top: -25px;
            background-image: url("/static/imgs/loading.gif");
            background-size: 100% 80%;
            background-repeat: no-repeat;
            background-color: grey;
            z-index: 999;
            
        }
    </style>
</head>
<body>
<div style="width: 900px;margin: auto;">
    <h1>老师列表</h1>
    <div style="margin: 10px">
        <a href="/add_teacher/" class="btn btn-primary">添加</a>
        <a class="btnAdd">对话框添加</a>
    </div>
    <table class="table table-striped table-hover table-bordered">
        <thead>
        <tr>
            <th>ID</th>
            <th>老师姓名</th>
            <th>任教班级</th>
            <th>操作</th>
        </tr>

        </thead>
        <tbody>
        {% for i in teacher_list %}
            <tr>
                <td>{{ i.tid }}</td>
                <td>{{ i.name }}</td>
                <td>
                    {% for iq in i.titles %}
                        <a>{{ iq }}</a>


                    {% endfor %}
                </td>

                <td><a href="/del/?nid={{ i.tid }}">删除</a>
                    <a href="/edit/?nid={{ i.tid }}">编辑</a>
                    <a>对话框编辑</a></td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    {#对话框编辑#}
    <div id="shadow" class="shadow hide"></div>
    <div id="modalll" class="modelll hide">
        <div class="loading "></div>
        <h3>添加老师</h3>
        <p>
            老师姓名：<input name="teacher_name" type="text" placeholder="老师姓名" id="addName">
        </p>
        <p>
          <select id="classIds" multiple size="10"  >


          </select>
        </p>
{##}
{#        <span>#}
{#        {% for row in class_list %}#}
{#            <input name="class_name" type="checkbox" value="{{ row.id }}" id="class_id"> {{ row.title }}#}
{#        {% endfor %}#}
{#    </span>#}
        <p>
            <input type="submit" value="提交" id="add_submit">
             <span id="editError" style="color: red;"></span>
        </p>

    </div>

</div>
<script src="/static/jquery-3.6.0.js"></script>
<script>
    $(function () {
        bindAdd();
        bindSubmit();
    });

    function bindAdd() {
        $('.btnAdd').click(function () {
            $('#shadow,#modalll').removeClass('hide');
            $.ajax({
                url: '/get_all_class/',
                type: 'GET',
                dataType: 'JSON',
                success:function (arg){

                    // 将所有的数据加入到option中
                    $.each(arg,function (i,row){
                        var tag = document.createElement('option');
                        tag.innerHTML = row.title;
                        tag.setAttribute('value',row.id);
                        $('#classIds').append(tag);
                    })
                }
            })

        })

    };
    function bindSubmit() {
        $('#add_submit').click(function () {
            var name = $('#addName').val();
            var class_id_list = $('#classIds').val();

            console.log(name,class_id_list);
            $.ajax({
                url: '/model_add_teachers/',
                type: 'POST',

                data: {'name':name,'class_list':class_id_list},
                dataType: 'JSON',
                traditional:true,
                success: function (arg) {
                    $.each(arg,function (i,row){
                        var tag = document.createElement('checkbox');
                    })
                    if(arg.status){
                        console.log(this.data);
                        location.reload();
                    } else {
                        $('editError').text(arg.message);
                    }
                }
            })
        })

    };
</script>

</body>
</html>
'''


def a(head):
    stack = []
    while head:
        stack.append(head.val)
        head = head.next
    return stack[::-1]


class ListNode(object):
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


class Solution:
    def reversePrint(self, head):
        stack = []
        while head:
            stack.append(head.val)
            head = head.next
        return stack[::-1]


# Definition for a binary tree node.

# class Solution:
#     def buildTree(self, preorder, inorder):
#         if preorder==[]:
#             return None
#         i=inorder.index(preorder[0])  #中序遍历根节点的位置，左子树的长度
#         root=TreeNode(inorder[i])
#         root.left=self.buildTree(preorder[1:i+1],inorder[:i])
#         root.right=self.buildTree(preorder[i+1:],inorder[i+1:])
#         return root

#
#
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#
# class Solution:
#     def buildTree(self, preorder, inorder) :
#         if not preorder or not inorder:
#             return None
#         root = TreeNode(preorder[0])
#         root.left = self.buildTree(preorder[1:inorder.index(preorder[0])+1], inorder[:inorder.index(preorder[0])])
#         root.right = self.buildTree(preorder[inorder.index(preorder[0])+1:], inorder[inorder.index(preorder[0])+1:])
#         return root.val,root.left,root.right
# preorder = [3,9,20,15,7]
#
# inorder = [9,3,15,20,7]
# obj = Solution()
# res = obj.buildTree(preorder,inorder)
# print(res)
class CQueue:

    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def appendTail(self, value: int) -> None:
        return self.stack1.append(value)

    def deleteHead(self) -> int:
        return


# Your CQueue object will be instantiated and called as such:
# obj = CQueue()
# obj.appendTail(value)
# param_2 = obj.deleteHead()

class Solution:
    def fib(self, n: int) -> int:
        list1 = [0, 1]
        if n < 0:
            return -1
        if n == 0:
            return 0
        if n == 1:
            return 1
        else:
            for i in range(2, n + 1):
                list1.append((list1[i - 1] + list1[i - 2]) % 1000000007)
        return list1[n]


class Solution:
    def minArray(self, numbers: [int]) -> int:
        i, j = 0, len(numbers) - 1
        while i < j:
            m = (i + j) // 2
            if numbers[m] > numbers[j]:
                i = m + 1
            elif numbers[m] == numbers[j]:
                j -= 1
            else:
                j = m
        return numbers[i]
