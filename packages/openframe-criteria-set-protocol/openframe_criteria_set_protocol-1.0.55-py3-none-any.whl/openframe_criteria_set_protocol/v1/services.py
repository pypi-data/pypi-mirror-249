# Interface for services which implement the v1 protocol
from abc import ABC, abstractmethod
from typing import Optional, Any, Generic
from typing import TypeVar
from .types import CriteriaTree, Metadata, TaskItemValueMap, StreamMatrixResponse

ParametersType = TypeVar("ParametersType", bound=dict)


"""
A class representing a specific version of a specific criteria set
"""
class ICriteriaSetService(Generic[ParametersType], ABC):
    # ID of the criteria set
    id: str

    # Specific version of the criteria set this class represents, SemVer-formatted
    version: str

    # Validate the given parameters
    @abstractmethod
    def validate_parameters(self, parameters: ParametersType):
        pass

    # Get the metadata for this criteria set version
    @abstractmethod
    def get_metadata(self) -> Metadata:
        pass

    # Get the criteria tree for the given parameters
    @abstractmethod
    def get_criteria_tree(
            self,
            parameters: Optional[ParametersType] = None,
            values: Optional[TaskItemValueMap] = None,
            locale: Optional[str] = None
    ) -> CriteriaTree:
        pass

    # Stream the matrix for the given parameters
    @abstractmethod
    def stream_matrix(
            self,
            parameters: Optional[ParametersType] = None,
            values: Optional[TaskItemValueMap] = None,
            locale: Optional[str] = None
    ) -> StreamMatrixResponse:
        pass


class IManagerService(ABC):
    # Get the criteria sets and versions available to this service
    @abstractmethod
    def get_criteria_sets_and_versions(self) -> dict[str, list[Metadata]]:
        pass

    # Get the criteria set with the given ID. If no version is requested, return the latest version
    @abstractmethod
    def get_service_for_criteria_set(self, criteria_set_id: str, version: Optional[str] = None) -> ICriteriaSetService:
        pass
