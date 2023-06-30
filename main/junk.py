@login_required
def download_rdp(request, pk):
    # try:
    #     instance = VPS.objects.get(id=pk)
    # except VPS.DoesNotExist as e:
    #     messages.error(request, "Instance Doesnot Exist")
    #     return redirect(reverse('user_dashboard'))


    try:
        obj = RDPFile.objects.get(id=1)
    except RDPFile.DoesNotExist as e:
        messages.error(request, "Resource Doesnot Exist")
        return redirect(reverse('user_dashboard'))

    try:
        print(obj.rdp_file.path)
        file_ = open(obj.rdp_file.path,'rb')
        lines = file_.readlines()
        from django.conf import settings
        import os
        output_path = os.path.join(settings.BASE_DIR, "media/oiiro.rdp")

        # lines[2] = b'full address:s:s' + b'hellotheremneti.com'
        my_str =  u'full address:s:' + u'ertyytew\n'
        # my_str_as_bytes = str.encode(my_str)
        my_str = bytes(my_str, encoding='utf-16')
        print(my_str)
        lines[1] = my_str
        # print(type(lines[1]))
        # f = open(output_path, "wb")
        f = io.open("testfile.txt", "wb")
        for lin in range(len(lines)):
            print(lines[lin])
            # print(lines[lin].decode('utf-8'))
            # print(type(lines[lin]))
            f.write(lines[lin])
        f.close()
        filename = "my-file.rdp"
        data = None
        with open(output_path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong. Please contact the administrator")
        return redirect(reverse('user_dashboard'))