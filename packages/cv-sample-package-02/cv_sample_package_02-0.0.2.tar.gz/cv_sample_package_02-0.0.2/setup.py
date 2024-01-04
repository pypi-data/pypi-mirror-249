import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="cv_sample_package_02", 
    version="0.0.2", 
    author="Arulvadivel", 
    author_email="arulvadivel@cloudvalleytech.com.com", 
    packages=[""], 
    description="A sample test package", 
    long_description=description, 
    long_description_content_type="text/markdown",
    python_requires='>=3.8', 
    install_requires=[] 
)