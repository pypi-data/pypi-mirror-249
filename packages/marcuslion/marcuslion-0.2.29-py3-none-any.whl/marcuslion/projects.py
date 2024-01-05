import pandas as pd

from marcuslion.config import api_version
from marcuslion.restcontroller import RestController


class Projects(RestController):
    """
    MarcusLion Projects class
        # $ curl 'https://qa1.marcuslion.com/core/projects'
    """

    def __init__(self, datasets):
        super().__init__(api_version + "/projects")
        self.datasets = datasets

    def list(self) -> pd.DataFrame:
        """
        Projects.list()
        """
        return super().verify_get_df("", {})

    def get_project_metadata(self, project_id) -> any:
        """
        Projects.get_project_metadata(id)
        """

        return super().verify_get(project_id)

    def __download_dataset_files(self, project_datasets: list, output_path=None) -> None:
        # Download dataset files
        if project_datasets is None:
            return
        for dataset in project_datasets:
            try:
                self.datasets.download(dataset["source"], dataset["refId"], dataset["file"], output_path)
            except ValueError as e:
                print(f"Failed to download dataset file {dataset['file']} for {dataset['refId']}")

    def download_project_metadata(self, project_id, output_path=None) -> any:
        """
        Projects.download_project_metadata(id)
        """
        try:
            metadata = self.get_project_metadata(project_id)
            self.__download_dataset_files(metadata["datasets"], output_path)
            return metadata
        except ValueError as e:
            print(f"Failed to download project metadata for project {project_id}")
