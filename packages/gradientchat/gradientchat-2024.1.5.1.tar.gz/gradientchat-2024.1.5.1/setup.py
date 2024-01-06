import setuptools
import gradientchat

setuptools.setup(
	name="gradientchat",
	version=gradientchat.__version__,
	author="RixTheTyrunt",
	description="Bot Client for GradientChat",
	packages=["gradientchat"],
	python_requires=">=3",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=["python-socketio"]
)