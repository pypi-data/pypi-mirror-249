import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="cv_sample_package_03", 
    version="0.0.4", 
    author="Arulvadivel S", 
    author_email="arulvadivel@cloudvalleytech.com", 
    description="A sample test package", 
    long_description=description, 
    long_description_content_type="text/markdown",
    packages=[""],
    python_requires='>=3.8', 
    install_requires=[
        'pycryptodome>=3.19.1',
    ] 
)