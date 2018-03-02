from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Victor
from .forms import LoginForm, RegisterForm
import hashlib
# Create your views here.


# 哈希加密函数
def hash_code(s, salt='MyBlog'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# 打开主页
def index(request):
    article_lists = Article.objects.all()
    paginator = Paginator(article_lists, 4)
    page = request.GET.get('page', '1')
    try:
        articles = paginator.get_page(page)
    except PageNotAnInteger:
        articles = paginator.get_page(1)
    except EmptyPage:
        articles = paginator.get_page(paginator.num_pages)
    return render(request, 'blog/index.html', locals())


# 登陆界面
def login(request):
    # 不允许用户重复登陆
    if request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('index'))
    # 当用户点击登陆按钮确认登陆时，由于登陆页面中form的设置，request的方法就为 GET
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data['user_name']
            input_password = form.cleaned_data['user_password']
            try:
                db_user = Victor.objects.get(user_name=input_name)
                if db_user.user_password == hash_code(input_password):
                    # 设定登录状态
                    request.session['is_login'] = True
                    request.session['user_name'] = input_name
                    request.session['user_id'] = db_user.id
                    return HttpResponseRedirect(reverse('index'))
                else:
                    error_message = "密码错误"
            except Exception as e:
                    error_message = "帐号错误"
        # 如果帐号，密码，验证码有一样不正确，则重新跳转回登陆界面
        return render(request, 'blog/login.html',  locals())
    # 当用户点击首页登陆按钮跳转到登陆界面的时候，request的方法就为 GET
    else:
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})


# 登出
def logout(request):
    if not request.session.get("is_login", None):
        return HttpResponseRedirect(reverse('index'))
    request.session.flush()
    return HttpResponseRedirect(reverse('index'))


# 注册页面
def register(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['user_password']
            re_password = request.POST['re_password']
            if password == re_password:
                request.session['is_login'] = True
                request.session['user_name'] = form.cleaned_data['user_name']
                db_user = form.save()
                db_user.user_password = hash_code(password)
                db_user.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                error_message = '两次密码不一致'
        return render(request, 'blog/register.html', locals())
    # 如果不是登陆状态，或者不是POST请求，则建立一个空表单
    form = RegisterForm()
    return render(request, 'blog/register.html', locals())


# 展示文章详细内容
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'blog/detail.html', locals())


# 编辑文章页面
def article_edit(request, article_id):
    if article_id == 0:
        return render(request, 'blog/edit.html')
    else:
        article = Article.objects.get(pk=article_id)
        return render(request, 'blog/edit.html', {'article': article})


# 提交文章修改/写新的文章
def article_submit(request, article_id):
    title = request.POST.get('title', 'Title')
    context = request.POST.get('context', 'Context')
    # 从session中获取当前作者名字
    author = request.session.get('user_name', '宋科儒')
    if article_id == 0:
        Article.objects.create(title=title, context=context, author=author)
        return HttpResponseRedirect(reverse('index'))
    else:
        amend_article = Article.objects.get(pk=article_id)
        amend_article.title = title
        amend_article.context = context
        amend_article.save()
        return HttpResponseRedirect(reverse('index'))


# 删除一篇文章
def article_delete(request, article_id):
    # 如果没登陆就不允许删除
    if not request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('index'))
    else:
        Article.objects.get(pk=article_id).delete()
        return HttpResponseRedirect(reverse('index'))