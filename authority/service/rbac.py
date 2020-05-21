import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from app01.models import UserInfo


class ValidPermission(MiddlewareMixin):

    def process_request(self, request):
        current_path = request.path_info
        # # 白名单
        # valid_url_list = ["/login/", "/reg/", "/admin/.*"]
        # for valid_url in valid_url_list:
        #     ret = re.match(valid_url, current_path)
        #     if ret:
        #         # 匹配上白名单，返回None
        #         return None

        # 需要检查用户名的路径列表
        need_valid_url_list = ['/stark/', ]
        for uri in need_valid_url_list:
            ret = re.match(uri, current_path)
            if ret:
                # 校验是否登陆
                if not request.user:
                    return redirect("/login/")
                else:
                    is_super = UserInfo.objects.filter(username=str(request.user)).values("is_superuser")\
                        .first().get("is_superuser")
                    if not is_super:
                        return HttpResponse("该用户非超级管理员")


        # 校验权限, 暂时没有这个需求
        # permission_list = request.session.get("permission_list", [])
        return None
