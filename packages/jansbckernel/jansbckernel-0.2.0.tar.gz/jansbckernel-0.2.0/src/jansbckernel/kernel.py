#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""bc kernel class module"""

import os
import shutil
import subprocess
from ipykernel.kernelbase import Kernel

version = subprocess.run('bc -v', shell= True, capture_output=True).stdout.decode('utf-8').split('\n')[0]

workingdir = "/tmp/bckernel/"

class jansbckernel(Kernel):
    """bc kernel uses ipykernel to run bc"""
    implementation = 'IPython'
    implementation_version = '8.19.0'
    language = 'bc'
    language_version = version.split(" ")[1]
    language_info = {
        'name': 'GNU bc',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }

    banner = version

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            if "read" in code:
                solution = "read is not allowed in bc kernel."
            else:
                if os.path.exists(workingdir):
                    shutil.rmtree(workingdir)
                os.mkdir(workingdir)
                with open(workingdir + 'calculation.txt', 'w', encoding='utf-8') as file:
                    file.write(code + '\nquit')
                solution = subprocess.run('bc -ql ' + workingdir + 'calculation.txt', shell=True, capture_output=True).stdout.decode('utf-8')
                solution = solution.replace('\\', '')
            stream_content = {'name': 'stdout', 'text': solution}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def do_shutdown(self, restart):
        if os.path.exists(workingdir):
            shutil.rmtree(workingdir)
