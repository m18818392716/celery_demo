from celery import Celery
from celery.schedules import crontab

app = Celery()


@app.on_after_configure.connect  # 装饰器作用：只要脚本一启动便立刻自动执行被装饰的函数
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')  # 每隔十秒钟，执行test函数，传入参数‘hello’,

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)  # expires任务结果保存十秒钟

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),  # 每周一早上十点半执行test函数
    )


@app.task
def test(arg):
    print(arg)