from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField("标题", max_length=30)
    context = models.TextField("内容", null=True)
    author = models.CharField("作者", max_length=15)
    pub_date = models.DateTimeField("发布时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"


class Victor(models.Model):

    gender = (
        # male为数据库实际存储的值，男为显示出来的值
        ('male', "男"),
        ('female', "女")
    )
    user_name = models.CharField("用户名", max_length=15, unique=True)
    # 密码设定位数那么大是为了之后采用哈希加密
    user_password = models.CharField("密码", max_length=256)
    user_email = models.EmailField("电子邮箱", unique=True)
    sex = models.CharField("性别", max_length=32, choices=gender, default="男")

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ["-user_name"]
        # 设置人类可读的模型名称，底下设置模型的复数名称
        verbose_name = "用户"
        verbose_name_plural = "用户"