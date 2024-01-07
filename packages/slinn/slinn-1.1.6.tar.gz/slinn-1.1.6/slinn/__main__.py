import sys, venv
from slinn.default import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'create':
            args = get_args(['path'], ' '.join(sys.argv[2:]))
            apppath = (args['path']+'?').replace('/?', '').replace('?', '') if 'path' in args.keys() else '.'
            import os, slinn, shutil, platform
            modulepath = os.path.abspath(slinn.__file__).replace('__init__.py', '')
            if not os.path.isdir(apppath):
                os.mkdir(apppath)
            else:
                print(f'Warning: {apppath} exists')
            shutil.copyfile(modulepath+'default/manage.py', f'{apppath}/manage.py')
            shutil.copyfile(modulepath+'default/project.json.py', f'{apppath}/project.json')
            venv.create(f'{apppath}/venv')
            packages_dir = ''
            if platform.system() == 'Windows':
                packages_dir = f'{apppath}/venv/Lib/site-packages'
            else:
                packages_dir = f'{apppath}/venv/lib/python{".".join(sys.version.split(" ")[0].split(".")[:-1])}/site-packages'
            try:
                os.makedirs(packages_dir)
            except FileExistsError:
                pass
            shutil.copytree(modulepath, packages_dir+'/slinn')
            print('Project created')