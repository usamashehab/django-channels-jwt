from setuptools import setup

readme = open("README.md").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")


setup(
    name="django-channels-jwt",
    version="1.0.0",
    description="Secure UUID-based JWT Auth Middleware for Django Channels",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Usama Shehab",
    author_email="usama.mh.shehab@gmail.com",
    url="https://github.com/usamashehab/django-channels-jwt",
    packages=["django_channels_jwt"],
    package_dir={"django_channels_jwt": "django_channels_jwt"},
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.2",
        "channels>=4.0.0",
        "djangorestframework>=3.14.0",
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords=["django", "channels", "jwt", "auth", "middleware", "python", "authentication", "websocket", "asgi"],
)
