class DatasetMetadata:
    """Represents a data science dataset in the platform."""
    def __init__(self, dataset_id: int, dataset_name: str, file_size_mb: float, source: str, record_count: int, last_updated: str, created_at: str):
        self.__id = dataset_id
        self.__name = dataset_name
        self.__file_size_mb = file_size_mb
        self.__source = source
        self.__record_count = record_count
        self.__last_updated = last_updated
        self.__created_at = created_at

    def get_id(self) -> int:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name

    def get_size_mb(self) -> float:
        return self.__file_size_mb if  self.__file_size_mb is not None else 0.0
    
    def get_source(self) -> str:
        return self.__source
    
    def __str__(self) -> str:
        return( f"Dataset {self.__id}: {self.__name}"
                f"({self.__file_size_mb:.2f} MB, "
                f"records: {self.__record_count}, "
                f"source: {self.__source})")
