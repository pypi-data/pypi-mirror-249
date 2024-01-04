import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
# Seasalt.ai@2020
setuptools.setup(
    name="seavoice-sdk-test",
    version="2.0.7",
    author="Seasalt.ai",
    author_email="info@seasalt.ai",
    description="SeaVoice SDK: Client for Seasalt speech recognition and speech synthesis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["websockets==10.3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

# browser notification
# confirm that
# if a new message comes in, change current tab to bulk-sms page.

# conversation (where is_unread is true) -> phone_id -> phone_id_user_mapping
# user COUNT(phone_id) group by workspace_id, user

# user
#  workspace_id 1
#    there is 3 unread messages.
#  workspace_id 2
#    there is 2 unread messages.

#
