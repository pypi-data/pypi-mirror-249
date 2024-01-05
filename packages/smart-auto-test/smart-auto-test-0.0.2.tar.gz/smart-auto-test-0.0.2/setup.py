# setup.py

import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="smart-auto-test",     # Required 项目名称
    version="0.0.2",            # Required 发布版本号
    author="lixiang3117",       # Optional 作者
    author_email="goodtime521@163.com",   # Optional 作者邮箱
    description="autotest",     # Optional 项目简单描述
    long_description=long_description,  # Optional 详细描述
    long_description_content_type="text/markdown",  # 内容类型
    url="https://github.com/PhinWilber/smart-test/tree/master",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    classifiers=[   # Optional 分类器通过对项目进行分类来帮助用户找到项目, 以下除了python版本其他的 不需要改动
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    keywords="codepay, codepay_python", # Optional 搜索关键字
)