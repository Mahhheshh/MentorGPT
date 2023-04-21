import json


class FileManager:
    """This class is used to read and write data to a json file"""
    file = "store/data.json"

    @classmethod
    async def read_json(cls) -> dict:
        """read data from the file use  to read the file"""
        with open(cls.file, "r") as f:
            data = json.load(f)
        return data

    @classmethod
    async def write_json(cls, data: dict) -> str:
        """write data to the file use  to write the file"""
        # read the file
        file_data = await cls.read_json()
        data = {len(file_data)+1: data}
        # update the file
        file_data.update(data)

        # write the file
        with open(cls.file, "w") as f:
            json.dump(file_data, f, indent=4)

        return "Data written to file"

    def __repr__(self):
        return f"FileManager(file={self.file})"