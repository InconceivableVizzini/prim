from setuptools import setup

setup(name='prim',
      version='0.0.1',
      packages=['prim'],
      entry_points={
        'console_scripts':[
          'primc = prim.compiler:main',
          'prim = prim.interpreter:main'
        ],
      },
      description='A prototype programming language for symbolic mathematics and numeric analysis.',
      author='Derek Ford',
      author_email='inconceivablevizzini@gmail.com',
      license='MIT',
      zip_safe=False,
)
