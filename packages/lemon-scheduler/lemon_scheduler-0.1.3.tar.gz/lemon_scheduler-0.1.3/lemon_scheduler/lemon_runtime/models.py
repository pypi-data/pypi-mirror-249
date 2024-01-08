from datetime import datetime
from decimal import Decimal
from typing import Union, TypeVar, Generic, Iterator, Optional, TypedDict
import peewee

CharField = Union[peewee.CharField, str]
DatetimeField = Union[peewee.DateTimeField, datetime]
TextField = Union[peewee.TextField, str]
IntegerField = Union[peewee.IntegerField, int]
BooleanField = Union[peewee.BooleanField, bool]
FloatField = Union[peewee.FloatField, float]
DoubleField = Union[peewee.DoubleField, float]
DateField = Union[peewee.DateField, str]
DateTimeField = Union[peewee.DateTimeField, str]
TimeField = Union[peewee.TimeField, str]
DecimalField = Union[peewee.DecimalField, Decimal]
PrimaryKeyField = Union[peewee.PrimaryKeyField, int]

T = TypeVar('T')


class ModelSelect(peewee.ModelSelect, Generic[T]):
    def __iter__(self) -> Iterator[T]:
        pass

    def where(self, *expressions) -> 'ModelSelect[T]':
        pass

    def limit(self, value: Optional[int] = None) -> 'ModelSelect[T]':
        pass

    def offset(self, value: Optional[int] = None) -> 'ModelSelect[T]':
        pass


class BackrefAccessor(peewee.BackrefAccessor, Generic[T]):
    pass


class ModelUpdate(peewee.ModelUpdate, Generic[T]):
    def where(self, *expressions) -> 'ModelUpdate[T]':
        pass

    def execute(self, database=None) -> int:
        pass


class BaseModel(peewee.Model):
    id: PrimaryKeyField

class ScheduleTaskTab(BaseModel):
    task_id: IntegerField
    expected_execute_time: IntegerField
    executed: BooleanField
    execution_result: CharField
    execution_output: CharField
    task_function: CharField
    task_arguments: CharField
    real_execution_time: IntegerField
    execution_finish_time: IntegerField
    priority: CharField

    class __InnerFields(TypedDict):
        task_id: int
        expected_execute_time: int
        executed: bool
        execution_result: str
        execution_output: str
        task_function: str
        task_arguments: str
        real_execution_time: int
        execution_finish_time: int
        priority: str

    @classmethod
    def select(cls, *fields) -> ModelSelect['ScheduleTaskTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['ScheduleTaskTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'ScheduleTaskTab':
        pass


class SchedulerSettingsTab(BaseModel):
    min_delay: IntegerField

    class __InnerFields(TypedDict):
        min_delay: int

    @classmethod
    def select(cls, *fields) -> ModelSelect['SchedulerSettingsTab']:
        pass

    @classmethod
    def update(cls, __data=..., **update: __InnerFields) -> ModelUpdate['SchedulerSettingsTab']:
        pass

    @classmethod
    def create(cls, **query: __InnerFields) -> 'SchedulerSettingsTab':
        pass

