from abc import ABC, abstractmethod
from typing import Any, Optional, Union, List



SampleType = Any


class ProcessItem(ABC):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.process(*args, **kwds)

class ProcessFilter(ProcessItem):
    @abstractmethod
    def process(self, data: SampleType) -> bool:
        pass

class ProcessMap(ProcessItem):
    @abstractmethod
    def process(self, data: SampleType) -> SampleType:
        pass

class ProcessReduce(ProcessItem):
    @abstractmethod
    def process(self, lhs: SampleType, rhs: SampleType) -> SampleType:
        pass

class ProcessConversion(ProcessItem):
    @abstractmethod
    def process(self, data: SampleType) -> Any:
        pass


class PipelineBase(ABC):
    @abstractmethod
    def run(self, data: List[SampleType]) -> List[SampleType]:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run(*args, **kwds)


class Pipeline(PipelineBase):
    def __init__(self, steps: Optional[List[ProcessItem]]=None, num_proc: Optional[int]=None):
        if steps is None:
            self.steps: List[ProcessItem] = []
        else:
            self.steps: List[ProcessItem] = steps
        self.num_proc = num_proc
    
    def add_step(self, step: Union[ProcessFilter, ProcessMap]):
        self.steps.append(step)

    def run(self, data: SampleType):
        for step in self.steps:
            if isinstance(step, ProcessFilter):
                print(f"Starting Filter- {type(step)}")
                data = data.filter(step, num_proc=self.num_proc)
            elif isinstance(step, ProcessMap):
                print(f"Starting Map - {type(step)}")
                data = data.map(step, num_proc=self.num_proc)
            else:
                raise ValueError("Step must be either a ProcessFilter or ProcessMap.")
        return data
