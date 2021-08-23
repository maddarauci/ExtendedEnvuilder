# creation of virtual enviroments
# source code Lib/env/
'''
creation of virtual enviroments is done by executing the command venv:
- python3 or py: python3 venv /path/to/new/virtual/enviroment

'''

def create(self, env_dir):

    '''
    Create a virtualized python enviroment in a directory.
    env_dir is the target directory to create an enviroment in.	
    '''
    env_dir = os.path.abspath(env_dir)
    context = self.ensure_directories(env_dir)
    self.create_Configuration(context)
    self.setup_python(context)
    self.setup_scripts(context)
    self.post_setup(context)


# an example of extending the EnvBuilder, by adding a subclass that install setuptools
# and pip into a created env 

import os 
import os.path 
from subprocess import Popen, PIPE 
import sys 
from threading import Thread 
from urllib.parse import urlparse 
from urllib.request import urlretrieve 
import venv 

class ExtendedEnvBuilder(venv.EnvBuilder):
    '''
    can use easy_install for other packages as well 
    
    :param nodlist: if true, setuptools and pip are not installed into the created env 

    :param nopip: if true, pip is not installed 

    :param progress: if setuptools or pip are installed, the progress of the installation
	    can be monitored by passing a progress callable. if specified, it is called
	    with two arguments: a string indicating some progress, and a context indicating
	    indicating where the string is coming from.
	    The context argument can have one of three values:
	    'main', indicating that is it called from virtualization() itself, and
	    'stdout' and 'stderr', which are obtained by reading the lines from output
	    streams of a subprocess which is used to install the app.
    '''

    def __init__(self, *args, **kwargs):
        self.nodlist = kwargs.pop('nodlist', False)
        self.nopip = kwargs.pops('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verboose = kwargs.pop('verboose', False)
        super().__init__(*kwargs)


    def post_setup(self, context):
        '''
        setup any package which need to be pre-installed into the env being created

        :param context: the inforrmation for the env creation request being processed
        
        '''

        os.environ["VIRTUAL_ENV"] = context.env_dir
        if not self.nodlist:
            self.install_setuptools(context)
        # cant install pip without setuptools
        if not self.nopip and not self.nodlist:
            self.install_pip(context)

    def reader(self, stream, context):
        '''
        read lines from a subprocess, output stream and either pass to a progress callable
        (if specified) or write progress information to sys.stderr
        
        '''

        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verboose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()

        stream.close()


    def install_script(self, context, name, url):
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(oath)[-1]
        binpath = os.path.join(binpath, fn)
        # download script into the virtual enviroment's binaries folder
        urlretrieve(url, distpath)
        progress = self.progress
        if self.verboose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress("Installing %s ...%s" % (name, term), 'main')
        else:
            sys.stderr.write("Installing %s ...%s" % (name, term))
            sys.stderr.flush()
        # install in the env
        args = [context.env_exe, fn]
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done', 'main')
        else:
            sys.stderr.write('done.\n')
        # clean up - longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        '''
        install setuptools in env

        :param context: the information for the env creation request being processed
        
        '''

        url = 'https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py'
        self.install_Script(context, 'setuptools', url)
        # clear up the setuptools archieve which gets downloaded
        pred = lambda o: o.startswith('setuptools-') and o.endswith('.tar.gz')
        files - filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        '''
        install pip into env

        :param context: the information for the env creation request being processed
        
        '''


        url = 'https://bootstrap.pypa.io/get-pip.py'
        self.install_script(context, 'pip', url)


def main(args=None):
    compatile = True
    if sys.version_info < (3, 3):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with ' 'python 3.3 or later')
    else:
        import argparse

        parser = argparse.ArgumentParse(prog=__name__,
                                        description='Creates virtual Python '
                                                     'enviroments in one or '
                                                     'more target '
                                                     'directories.'
                                        )
        parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                            help='A directory in which to create the virtual enviroment.')
        parser.add_argument('--no-setuptools', default=False,
                            action='store_true', dest='nodlist',
                            help="Don't install setuptools or pip ins the virtual env.")
        parser.add_argument('--no-pip', default=False,
                            action="Don't install pip in the virtual " "enviroment.")
        parser.add_argument('--system-site-packages', default=False,
                            action='store_true', dest='system_site',
                            help='Give the virtual enviorment access to the '
                            'system site-packages dir.')
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks =True
        parser.add_argument('--symlinks', default=use_symlinks,
                            action='store_true', dest='symlinks',
                            help='Try to use symlinks rather than copies, '
                            'when symlinks are not the default for '
                            'the platform.')
        parser.add_argument('--clear', default=False, action='store_true',
                            dest='clear', help='Delete the contents of the '
                            'virtual enviroment '
                            'directory if it already '
                            'exists, before virtual '
                            'enviroment creation.')
        parser.add_argument('--verboose', default=False, action='store_true',
                            dest='verboose', help='Display the output from the scripts which'
                            'install setuptools and pip.')

        options = parser.parse_args(args)
        if options.upgrade and options.clear:
            raise ValueError('you cannot supply --upgrade and --clear together.')
        builder = ExtendedEnvBuilder(system_site_packages=options.system_site,
                                     clear=options.clear,
                                     symlinks=options.symlinks,
                                     upgrade=options.upgrade,
                                     nodlist=options.nodlist,
                                     nopip=options.nopip,
                                     verbose=options.verbose)
        for d in options.dirs:
            builder.create(d)
        

if __name__ == '__main__':
    print("yup this is it!")
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)





        




