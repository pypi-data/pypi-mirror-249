from setuptools import setup, find_packages
 
with open('README.md', 'r') as fh:
    long_description = fh.read()
    
setup(
    name='zsedu',                      # 模块名称
    version='0.0.1',                       # 版本号
    description='A Test Moudle',   # 模块描述
    long_description=long_description,         # README.md文件内容
    long_description_content_type='text/markdown',   # README.md格式类型
    url='https://github.com/yuanyunqiang',   # GitHub仓库地址
    author='YuanYunQiang',                        # 开发者姓名
    packages=find_packages(),                # 导入所有子包
    classifiers=[
        'Programming Language :: Python :: 3',          # 支持的Python版本
        'License :: OSI Approved :: MIT License'        # 许可证类型
    ],
)