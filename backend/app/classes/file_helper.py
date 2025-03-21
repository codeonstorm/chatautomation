from pathlib import Path
from typing import List, Dict, Union

class FileHelper:
    """Helper class to retrieve file details from a given folder."""
    
    def __init__(self, folder_path: str):
        self.folder = Path(folder_path)
    
    def validate_folder(self) -> bool:
        """Checks if the folder path is valid."""
        return self.folder.exists() and self.folder.is_dir()
    
    def create_folder(self) -> Dict[str, str]:
        """Creates the folder if it does not exist."""
        if not self.folder.exists():
            self.folder.mkdir(parents=True, exist_ok=True)
            return {"success": "Folder created successfully."}
        return {"error": "Folder already exists."}
    
    def get_file_details(self) -> Union[List[Dict[str, Union[str, float]]], Dict[str, str]]:
        """Returns details of all files in the specified folder."""
        
        if not self.validate_folder():
            return {"error": "Invalid folder path!"}
        
        files_info = []
        
        for file in self.folder.iterdir():
            if file.is_file():
                files_info.append({
                    "name": file.name,
                    # "path": str(file.resolve()),
                    "extension": file.suffix,
                    "size_kb": round(file.stat().st_size / 1024, 2),  # Size in KB
                    "created_at": file.stat().st_birthtime,  # Creation timestamp
                    "modified_at": file.stat().st_mtime  # Last modified timestamp
                })
        return files_info

    def delete_file(self, file_name: str) -> Dict[str, str]:
        """Deletes a specified file in the folder."""
        file_path = self.folder / file_name
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return {"success": f"File '{file_name}' deleted successfully."}
        return {"error": f"File '{file_name}' not found."}
    
    def delete_folder(self) -> Dict[str, str]:
        """Deletes the entire folder and its contents."""
        if self.validate_folder():
            for file in self.folder.iterdir():
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    FileHelper(str(file)).delete_folder()  # Recursively delete subfolders
            self.folder.rmdir()
            return {"success": "Folder deleted successfully."}
        return {"error": "Invalid folder path!"}
    


if __name__ == "__main__":
    folder_path = "../uploads"  # Change to your directory
    file_helper = FileHelper(folder_path)
    file_metadata = file_helper.get_file_details()
    
    for file in file_metadata:
        print(file)
