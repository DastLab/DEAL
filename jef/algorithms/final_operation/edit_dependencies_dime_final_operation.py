from abc import ABC, abstractmethod

from loader.classes.abstract_class.final_operation import FinalOperation
from loader.classes.json_class.discovery_info import DiscoveryInfo
from loader.classes.json_class.execution_result.result.data.attribute import Attribute
from loader.classes.json_class.execution_result.result.data.data import Data


class EditDependenciesDimeFinalOperation(FinalOperation):

    def edit(self, discovery_info:DiscoveryInfo) -> DiscoveryInfo:
        dependencies=discovery_info.execution_result.result.data
        header=discovery_info.dataset.header
        thrs=discovery_info.execution_result.result.additional_info.others["comparison_values"]
        thrs=thrs.replace("[","").replace("]","").strip()
        thrs = thrs.split(", ")
        if len(thrs)==1:
            thrs=[thrs[0]]*len(header)
        to_add=[]
        to_remove=[]
        i=0
        for dependency in dependencies:
            if dependency.lhs[0].column=="*":
                to_remove.append(i)
                j=0
                for h in header:
                    if h!=dependency.rhs.column:
                        to_add.append(Data([Attribute(h,thrs[j])],dependency.rhs,None))
                    j+=1
            i+=1
        for j in to_remove:
            dependencies[j]=None
        dependencies=list(filter(lambda x:x is not None,dependencies))
        dependencies.extend(to_add)
        discovery_info.execution_result.result.data=dependencies
        return discovery_info


