import marcuslion as ml


def test():
    print(__name__)

    project = ml.projects.get_project_metadata("f31e1eef-20f6-3733-a18c-538073e78396")
    print(project)

