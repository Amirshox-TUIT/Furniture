
def get_pk(request):
    paths = request.path.split('/')
    return int(paths[4])
