from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from Admin import tasks


def deme_view(request):
    # 用delay方法运行函数，这里两个函数可以同时被调用，也就是并行
    result_one = tasks.send_sms.delay()
    result_two = tasks.send_sms2.delay()

    # 用get方法拿到返回的结果
    print(result_one.get())
    print(result_two.get())
    final_result = result_one.get() + result_two.get()

    return JsonResponse(
        {
            'code': 200,
            'message': 'success',
            'data': {
                'result': final_result
            }
        }
    )
