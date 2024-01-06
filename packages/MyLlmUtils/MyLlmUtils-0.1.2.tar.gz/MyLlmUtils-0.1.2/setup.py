from distutils.core import setup
setup(
  name = 'MyLlmUtils',         # How you named your package folder (MyLib)
  packages = ['MyLlmUtils'],   # Chose the same as "name"
  version = '0.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Personal utility package to make using LLM more easily',   # Give a short description about your library
  author = 'Ken Hu',                   # Type in your name
  author_email = 'ken.hu@hwacom.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kenhutaiwan/MyLlmUtils/archive/refs/tags/0.1.2.tar.gz',    # I explain this later on
  keywords = ['LLM', 'OpenAI', 'Azure'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        'langchain',
        'openai',
        'pytest'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
  ],
)
