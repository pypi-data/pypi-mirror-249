from setuptools import setup, find_packages
excluded_packages = [
    'core', 'core.*', 
    'linkzone', 'linkzone.*', 
]
setup(
    name='stela_control_publishing',
    version='0.1.36',
    packages=find_packages(exclude=excluded_packages),
    include_package_data=True,
    license='MIT',
    description='All apps in one for business.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'aiohttp==3.8.3',
        'aiosignal==1.3.1',
        'annotated-types==0.6.0',
        'anyio==3.7.1',
        'asgiref==3.7.0',
        'asn1crypto==1.5.1',
        'async-timeout==4.0.2',
        'attrs==22.2.0',
        'Babel==2.12.1',
        'beautifulsoup4==4.12.2',
        'bleach==6.0.0',
        'boto3==1.24.36',
        'botocore==1.27.36',
        'cachetools==5.3.1',
        'certifi==2021.10.8',
        'cffi==1.15.1',
        'charset-normalizer==2.0.12',
        'click==8.1.3',
        'colorama==0.4.5',
        'cryptography==38.0.3',
        'cssselect2==0.6.0',
        'curlify==2.2.1',
        'distro==1.8.0',
        'Django==5.0',
        'django-admin-thumbnails==0.2.6',
        'django-autoslug==1.9.8',
        'django-cities-light==3.9.2',
        'django-compat==1.0.15',
        'django-crispy-forms==1.14.0',
        'django-cron==0.6.0',
        'django-csp==3.7',
        'django-environ==0.7.0',
        'django-hosts==5.1',
        'django-htmx==1.12.0',
        'django-js-asset==2.0.0',
        'django-mailjet==0.3.1',
        'django-model-utils==4.3.1',
        'django-mptt==0.13.4',
        'django-phonenumber-field==7.1.0',
        'django-sass-processor==1.2.2',
        'django-storages==1.12.3',
        'exceptiongroup==1.1.3',
        'facebook-business==17.0.0',
        'frozenlist==1.3.3',
        'future==0.18.2',
        'google-api-core==2.11.0',
        'google-auth==2.19.1',
        'google-cloud-monitoring==2.15.0',
        'googleapis-common-protos==1.59.0',
        'grpcio==1.54.2',
        'grpcio-status==1.54.2',
        'gunicorn==20.1.0',
        'h11==0.14.0',
        'html5lib==1.1',
        'httpcore==1.0.1',
        'httpx==0.25.1',
        'idna==3.3',
        'jmespath==1.0.1',
        'lxml==4.9.1',
        'mailjet-rest==1.3.4',
        'MarkupSafe==2.1.2',
        'multidict==6.0.4',
        'openai==1.2.2',
        'oscrypto==1.3.0',
        'paypal-checkout-serversdk==1.0.1',
        'paypalhttp==1.0.1',
        'google-api-core==2.11.0',
        'google-api-python-client==2.108.0',
        'google-auth==2.19.1',
        'google-auth-httplib2==0.1.1',
        'google-auth-oauthlib==1.1.0',
        'google-cloud-monitoring==2.15.0',
        'googleapis-common-protos==1.59.0',
        'python-amazon-paapi==5.0.1',
        'paypalrestsdk==1.13.1',
        'phonenumbers==8.13.13',
        'Pillow==9.0.0',
        'progressbar2==4.0.0',
        'proto-plus==1.22.2',
        'protobuf==4.23.2',
        'pyasn1==0.5.0',
        'pyasn1-modules==0.3.0',
        'pycountry==22.3.5',
        'pycparser==2.21',
        'pycryptodome==3.14.1',
        'pydantic==2.4.2',
        'pydantic_core==2.10.1',
        'pyHanko==0.13.2',
        'pyhanko-certvalidator==0.19.5',
        'pyOpenSSL==22.1.0',
        'PyPDF3==1.0.6',
        'python-bidi==0.4.2',
        'python-dateutil==2.8.2',
        'python-utils==3.1.0',
        'pytz==2021.3',
        'pytz-deprecation-shim==0.1.0.post0',
        'PyYAML==6.0',
        'qrcode==7.3.1',
        'reportlab==3.6.11',
        'requests==2.27.1',
        'rsa==4.9',
        's3transfer==0.6.0',
        'six==1.16.0',
        'sniffio==1.3.0',
        'soupsieve==2.4.1',
        'sqlparse==0.4.2',
        'stripe==2.68.0',
        'svglib==1.4.1',
        'swapper==1.3.0',
        'tinycss2==1.1.1',
        'tqdm==4.64.0',
        'typing_extensions==4.8.0',
        'tzdata==2022.1',
        'tzlocal==4.2',
        'Unidecode==1.3.2',
        'uritools==4.0.0',
        'urllib3==1.26.9',
        'webencodings==0.5.1',
        'whois==0.9.13',
        'xhtml2pdf==0.2.8',
        'yarl==1.8.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)