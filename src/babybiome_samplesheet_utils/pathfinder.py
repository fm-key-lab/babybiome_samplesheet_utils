import re
from collections import defaultdict
from pathlib import Path


class PathFinder:
    def __init__(self, directory):
        self.directory = Path(directory)
        self._check_directory()

    def _check_directory(self):
        if not self.directory.is_dir():
            raise DataDirectoryError(
                self.directory.as_posix() + ' does not exist.'
            )

    def find_paths(self, IDs) -> dict:
        """Find paths."""
        if isinstance(IDs, str):
            IDs = [IDs]
        
        ID_path_key = {
            ID: self.find_path(ID) for ID in IDs
        }
        
        # TODO: Should return full key for all none (not just top-level keys)
        missing_IDs = [k for k, v in ID_path_key.items() if not v]
        
        # TODO: Log these IDs
        print(
            'No paths were found for the following IDs:\n'
            + ',\n'.join(missing_IDs)
        )
        
        return ID_path_key

    def find_path(self, ID):
        matches = self.directory.glob(f'*{ID}*')
        return [str(path_obj) for path_obj in matches]

class FASTQPathFinder(PathFinder):
    def __init__(self, directory, fastq_substr='fastq', read_pattern=r'\d+_R([12])_\d+'):
        self.fastq_substr = fastq_substr
        self.read_pattern = read_pattern
        super().__init__(directory)
        
    def _check_directory(self):
        super()._check_directory()
        if len(list(self.directory.glob(f'*{self.fastq_substr}*'))) == 0:
            raise DataDirectoryError(
                self.directory.as_posix() 
                + ' contains no files matching '
                + '"' + self.fastq_substr + '"'
            )

    def find_path(self, ID):
        """Find FASTQ paths."""
        def find_reads(paths):
            read_paths = defaultdict(list)
            
            def find_read(path):
                return re.findall(self.read_pattern, path)[0]

            for path in paths:
                read_paths[f'fastq_{find_read(path)}'].append(path)

            return dict(read_paths)

        return find_reads(super().find_path(ID))