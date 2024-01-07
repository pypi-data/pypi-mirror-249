from distutils.core import setup
setup(
    # How you named your package folder (MyLib)
    name='dev_tools_supporter',
    packages=['dev_tools_supporter'],   # Chose the same as "name"
    version='1.2.0',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Methods for supportively coding MMO tools',
    author='2uanDM',                   # Type in your name
    author_email='hokage321xxx@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/2uanDM/dev_tools-supporter',
    # I explain this later on
    download_url='https://github.com/2uanDM/dev_tools-supporter/archive/refs/tags/v.1.1.0.tar.gz',
    # Keywords that define your package best
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[            # I get to this in a second
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
