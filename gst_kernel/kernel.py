# TODO:  remember to set python.defaultInterpreterPath 



from ipykernel.kernelbase import Kernel
from ipykernel.kernelbase import Kernel

import pexpect
from pexpect import EOF
from pexpect.replwrap import REPLWrapper

import os.path
import uuid
import random
import string

import re
import signal

__version__ = '0.1.0'

version_pat = re.compile(r'version (\d+(\.\d+)+)')

class GSTKernel(Kernel):
    implementation = 'gst'
    implementation_version = '0.1'
    language = 'Smalltalk'
    language_version = '0.1'
    language_info = {'name': 'gst',
                     'codemirror_mode': 'Smalltalk',
                     'mimetype': 'text/x-stsrc' ,   # 'text/plain' ??
                     'file_extension': '.st'}
    banner = "GNU Smalltalk Kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)   # init on super class
        self.gst_wrapper = REPLWrapper("gst", "st> ", None)


    def process_output(self, output):
        stream_content = {'name': 'stdout', 'text': output}
        self.send_response(self.iopub_socket, 'stream', stream_content)



    """def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }"""
    
    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.silent = silent

        # No code found
        if not code.strip():
            process_output(" ")
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            self.gst_wrapper.run_command(code.rstrip(), timeout=None)
        except KeyboardInterrupt:
            self.gst_wrapper.child.sendintr()
            interrupted = True
        
        output = self.gst_wrapper.child.before
        self.process_output(output)


        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}
        else:
            return {'status': 'ok', 'execution_count': self.execution_count,'payload': [], 'user_expressions': {}}





if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=GSTKernel)
