from setuptools import setup, find_packages

str_version = '1.0.4'

setup(name='UCToolsZD',
      version=str_version,
      description='UCToolsZD',
      author='xiejunwei',
      author_email='xiejunwei@qq.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires= ['pypinyin', 'opencv-python'],
      python_requires='>=3')

