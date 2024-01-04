import os

from rich import print

key = os.getenv("NEXON_OPEN_API_KEY")
print(key)

from pydantic import BaseModel


class DefaultModel(BaseModel):
    def __str__(self) -> str:
        return self.__repr__()


class Character(DefaultModel):
    """캐릭터 식별자(ocid)

    ocid(str): 캐릭터 식별자
    """

    ocid: str


class Character2(BaseModel):
    """캐릭터 식별자(ocid)

    ocid(str): 캐릭터 식별자
    """

    ocid: str


# def __repr__(self) -> str:
#     return f'{self.__repr_name__()}({self.__repr_str__(", ")})'

# # take logic from `_repr.Representation` without the side effects of inheritance, see #5740
# __repr_name__ = _repr.Representation.__repr_name__
# __repr_str__ = _repr.Representation.__repr_str__
# __pretty__ = _repr.Representation.__pretty__
# __rich_repr__ = _repr.Representation.__rich_repr__

# def __str__(self) -> str:
#     return self.__repr_str__(' ')

# fmt: off
d = DefaultModel()
print(f"d = {d}")               # d = DefaultModel()
print(f"{d = }")                # d = DefaultModel()
print(d)                        # DefaultModel()
print(repr(d.__repr__()))       # 'DefaultModel()'
print(list(d.__repr_args__()))  # []
print(repr(d.__str__()))        # 'DefaultModel()'
# fmt: on


print("------------------")


# fmt: off
c = Character(ocid="test_id")
print(f"c = {c}")               # c = Character(ocid='test_id')
print(f"{c = }")                # c = Character(ocid='test_id')
print(c)                        # Character(ocid='test_id')
print(repr(c.__repr__()))       # "Character(ocid='test_id')"
print(list(c.__repr_args__()))  # [('ocid', 'test_id')]
print(repr(c.__str__()))        # "Character(ocid='test_id')"
# fmt: on


print("------------------")
# fmt: off
c = Character2(ocid="test_id2")
print(f"c = {c}")               # c = ocid='test_id2'
print(f"{c = }")                # c = Character2(ocid='test_id2')
print(c)                        # Character2(ocid='test_id2')
print(repr(c.__repr__()))       # "Character2(ocid='test_id2')"
print(list(c.__repr_args__()))  # [('ocid', 'test_id2')]
print(repr(c.__str__()))        # "ocid='test_id2'"
# fmt: on
