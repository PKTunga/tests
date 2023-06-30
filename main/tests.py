# from django.test import TestCase

# # Create your tests here.
# from django.http import HttpResponse, HttpResponseNotFound

# def download_rdp(request, pk):
#     # try:
#     #     instance = VPS.objects.get(instance_id=id)
#     # except VPS.DoesNotExist as e:
#     #     messages.error(request, "Instance Doesnot Exist")
#     #     return redirect(reverse('user_dashboard'))
#     try:
#         obj = RDPFile.objects.get(id=1)
#     except RDPFile.DoesNotExist as e:
#         messages.error(request, "Resource Doesnot Exist")
#         return redirect(reverse('user_dashboard'))

#     from django.conf import settings
#     import os
#     output_path = os.path.join(settings.BASE_DIR, "connect.rdp") 
#     # read file
#     # try:
#     file_ = open(obj.rdp_file.path, mode='r')
#     print(obj.rdp_file.path)
#     lines = file_.readlines()
#     print(lines)
#     #     with open(output_path, 'w',encoding = 'utf-8') as f:
#     #     # output =  open(output_path, mode='wa', encoding = 'utf-8')
#     #         print("Opened File")
#     #         for line in lines:
#     #             if "full address" in line:
#     #                 line = "full address:s:s" + "hellotheremneti.com"
#     #             f.write(line)

#     #         response = HttpResponse(f, content_type='application/rdp')
#     #         response['Content-Disposition'] = 'attachment; filename="connect.rdp"'
#     # except Exception as e:
#     #     print(e)
#     #     response = HttpResponseNotFound('<h1>File not exist</h1>')
#     # return response