from django.shortcuts import render, redirect, HttpResponse
import pymysql
from utils import sqlhelper
import json
from  utils import sqlhelpers
import datetime
from datetime import timedelta
from django.db import models
def classes(request):
    '''
    先去请求的cookie中找凭证
    显示数据库中所有的班级
    :param request:
    :return:
    '''
    tk = request.get_signed_cookie('ticket',salt='sadsaddsasdsasd')
    print(tk)
    if not tk:
        return redirect('/login/')
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'classes.html', {'class_list': class_list})


def add_class(request):
    if request.method == 'GET':
        return render(request, 'add_class.html')
    if request.method == 'POST':
        v = request.POST.get('title')
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert class(title) values(%s)", [v, ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')


def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')


def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id = %s", [nid, ])
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.POST.get('id')
        title = request.POST.get('title')
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title =%s where id=%s", [title, nid])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')


def students(request):
    '''
    学生列表
    :param request: 封装了请求相关的所有信息
    :return:
    select student.name,class.title from student left join class ON student.classid=class.id
    '''
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        " select student.id,student.classid,student.name,class.title from student left join class ON student.classid=class.id", )
    student_list = cursor.fetchall()
    print(student_list)
    cursor.close()
    conn.close()

    classlist = sqlhelper.get_list('select id,title from class', [])
    return render(request, 'students.html', {'student_list': student_list, 'classlist': classlist})


def text(request):
    student_list = models.student.objects.all()
    return render(request,'text,html',{'student_list':student_list})








def add_student(request):
    if request.method == 'GET':
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        class_list1 = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'add_student.html', {'class_list': class_list1})
    else:
        name = request.POST.get("name")
        id = request.POST.get("class_id")
        print(id)
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='db2', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name,classid) values (%s,%s)", [name, id, ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')


def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list2 = sqlhelper.get_list('select id,title from class', [])
        current_student_info = sqlhelper.get_one('select id,name,classid from student where id=%s', [nid, ])
        return render(request, 'edit_student.html',
                      {'class_list': class_list2, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        classid = request.POST.get('class_id')
        print(name, classid)
        sqlhelper.modify('update student set name=%s,classid=%s where id =%s ', [name, classid, nid])
        return redirect('/students/')


def del_student(request):
    nid = request.GET.get('nid')
    sqlhelper.modify('delete from student where id=%s', [nid])
    return redirect('/students/')


# ############################################ 对话框 ####################################################
def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        sqlhelper.modify('insert into class(title) values(%s)', [title, ])
        return HttpResponse('ok')

    else:
        # 页面不刷新，提示错误信息
        return HttpResponse('不能为空！')


def model_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlhelper.modify('update class set title=%s where id=%s', [content, nid, ])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"

    return HttpResponse(json.dumps(ret))


def model_add_students(request):
    ret = {'status': True, 'message': None}

    try:
        classid = request.POST.get('classid')
        classname = request.POST.get('name')
        if len(classname) > 0:
            sqlhelper.modify('insert into student(name,classid) values (%s,%s)', [classname, classid, ])
        else:
            ret['status'] = False
            ret['message'] = str('输入为空')

    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


def model_edit_student(request):
    ret = {'status': True, 'message': None}

    try:
        nid = request.POST.get('nid')
        classid = request.POST.get('classid')
        name = request.POST.get('name')
        if len(name) > 0:
            sqlhelper.modify('update student set name=%s,classid=%s where id=%s', [name, classid, nid])
        else:
            ret['status'] = False
            ret['message'] = str('输入为空')

    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


def teacher(request):
    conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8', db='db2')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        'select teacher.id as tid,teacher.name,class.title from teacher left join teacher2class on teacher.id=teacher2class.teacherid left join class on class.id=teacher2class.classid')
    teacher_list = cursor.fetchall()
    cursor.close()
    conn.close()
    class_list = sqlhelper.get_list('select id,title from class',[])
    res = {}
    for i in teacher_list:
        tid = i['tid']
        if tid in res:
            res[tid]['titles'].append(i['title'])
        else:
            res[tid] = {'tid': i['tid'], 'name': i['name'], 'titles': [i['title'], ]}

    return render(request, 'teacher.html', {'teacher_list': res.values(),'class_list':class_list})


def del_name(request):
    nid = request.GET.get('nid')
    classid = sqlhelper.get_list('select id from teacher2class where teacherid=%s', [nid, ])
    for i in classid:
        sqlhelper.modify('delete from teacher2class where id=%s', [int(i['id'])])
    conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8', db='db2')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from teacher where id=%s', [nid, ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/teacher/')


def add_teacher(request):
    if request.method == 'GET':
        class_list = sqlhelper.get_list('select id,title from class', [])
        return render(request, 'add.html', {'classlist': class_list})
    else:
        name = request.POST.get('name')
        classname_list = request.POST.getlist('classname')
        conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8', db='db2')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('insert into teacher(name) values(%s)', [name, ])
        conn.commit()
        cursor.close()
        conn.close()
        teacher_id = sqlhelper.get_one('select id from teacher where name=%s', [name, ])

        for i in classname_list:
            sqlhelper.modify('insert into teacher2class(teacherid,classid) values(%s,%s)', [teacher_id['id'], int(i)])

        return redirect('/teacher/')


def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8', db='db2')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select id,name from teacher where id=%s', [nid, ])
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit.html', {'result': res})
    else:
        nid = request.POST.get('id')
        name = request.POST.get('name')
        conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8', db='db2')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update teacher set name =%s where id=%s", [name, nid, ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/teacher/')
def model_add_teachers(request):
    ret = {'status': True, 'message': None}

    try:
        name = request.POST.get('name')
        classid = request.POST.getlist('class_list')
        print(name,classid)
        if len(name) > 0:
            sqlhelper.modify('insert into teacher(name) values(%s)',[name,])
            teacher_id = sqlhelper.get_one('select id from teacher where name=%s',[name])
            for i in classid:
                sqlhelper.modify('insert into teacher2class(teacherid,classid) values(%s,%s)',[int(teacher_id['id']),int(i)])
        else:
            ret['status'] = False
            ret['message'] = str('输入为空')
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))
def get_all_class(request):
    obj = sqlhelpers.SqlHelper()
    obj.connect()
    class_list = obj.get_list('select id,title from class',[])
    obj.close()
    return HttpResponse(json.dumps(class_list))

def latout(request):
    return render(request,'layout.html')

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('passwd')
        print(user,pwd)
        if user == 'alex' and pwd =='123':
            obj = redirect('/classes/')
            ct = datetime.datetime.utcnow()
            v = timedelta(seconds=10000)
            value = ct+v
            obj.set_signed_cookie('ticket','123123',salt='sadsaddsasdsasd',expires=value )
            return obj
        else:
            return render(request,'login.html')