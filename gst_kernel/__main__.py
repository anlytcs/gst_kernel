from ipykernel.kernelapp import IPKernelApp
from .kernel import GSTKernel
IPKernelApp.launch_instance(kernel_class=GSTKernel)
