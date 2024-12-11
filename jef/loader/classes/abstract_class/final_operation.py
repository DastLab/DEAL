from abc import ABC, abstractmethod

from loader.classes.json_class.discovery_info import DiscoveryInfo


class FinalOperation(ABC):
    @abstractmethod
    def edit(self, discovery_info:DiscoveryInfo) -> DiscoveryInfo:
        pass