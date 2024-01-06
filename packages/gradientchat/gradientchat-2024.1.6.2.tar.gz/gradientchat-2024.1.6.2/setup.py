import setuptools
import gradientchat

with open("README.md") as readIO:
	with open("test.py") as testbIO:
		setuptools.setup(
			name="gradientchat",
			version=gradientchat.__version__,
			author="RixTheTyrunt",
			description="Bot Client for GradientChat",
			packages=["gradientchat"],
			python_requires=">=3",
			long_description=readIO.read().replace("%testbot%", testbIO.read()),
			long_description_content_type="text/markdown",
			install_requires=["python-socketio"]
		)