import uuid
from typing import TypedDict

import pytest as pytest
from _pytest.fixtures import SubRequest
from typing_extensions import Annotated

from integration.conftest import CollectionFactory, CollectionFactoryGet
from integration.conftest import _sanitize_collection_name
from weaviate.collections.classes.config import (
    Configure,
    Property,
    DataType,
    ReferenceProperty,
    ReferencePropertyMultiTarget,
)
from weaviate.collections.classes.data import DataObject, DataReference, DataReferenceOneToMany
from weaviate.collections.classes.grpc import (
    FromReference,
    FromReferenceMultiTarget,
    MetadataQuery,
    QueryReference,
)
from weaviate.collections.classes.internal import CrossReference, Reference, ReferenceAnnotation


def test_reference_add_delete_replace(collection_factory: CollectionFactory) -> None:
    ref_collection = collection_factory(
        name="Target", vectorizer_config=Configure.Vectorizer.none()
    )
    uuid_to = ref_collection.data.insert(properties={})
    collection = collection_factory(
        references=[ReferenceProperty(name="ref", target_collection=ref_collection.name)],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    uuid_from1 = collection.data.insert({}, uuid=uuid.uuid4())
    uuid_from2 = collection.data.insert(
        {}, references={"ref": Reference.to(uuids=uuid_to)}, uuid=uuid.uuid4()
    )
    collection.data.reference_add(
        from_uuid=uuid_from1, from_property="ref", to=Reference.to(uuids=uuid_to)
    )

    collection.data.reference_delete(
        from_uuid=uuid_from1, from_property="ref", to=Reference.to(uuids=uuid_to)
    )
    assert (
        len(
            collection.query.fetch_object_by_id(
                uuid_from1, return_references=FromReference(link_on="ref")
            )
            .references["ref"]
            .objects
        )
        == 0
    )

    collection.data.reference_add(
        from_uuid=uuid_from2, from_property="ref", to=Reference.to(uuids=uuid_to)
    )
    obj = collection.query.fetch_object_by_id(
        uuid_from2, return_references=FromReference(link_on="ref")
    )
    assert obj is not None
    assert len(obj.references["ref"].objects) == 2
    assert uuid_to in [x.uuid for x in obj.references["ref"].objects]

    collection.data.reference_replace(
        from_uuid=uuid_from2, from_property="ref", to=Reference.to(uuids=[])
    )
    assert (
        len(
            collection.query.fetch_object_by_id(
                uuid_from2, return_references=FromReference(link_on="ref")
            )
            .references["ref"]
            .objects
        )
        == 0
    )


def test_mono_references_grpc(collection_factory: CollectionFactory) -> None:
    A = collection_factory(
        name="A",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    uuid_A1 = A.data.insert(properties={"Name": "A1"})
    uuid_A2 = A.data.insert(properties={"Name": "A2"})

    a_objs = A.query.bm25(query="A1", return_properties="name").objects
    assert a_objs[0].properties["name"] == "A1"

    B = collection_factory(
        name="B",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="a", target_collection=A.name),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuid_B = B.data.insert({"Name": "B"}, references={"a": Reference.to(uuids=uuid_A1)})
    B.data.reference_add(from_uuid=uuid_B, from_property="a", to=Reference.to(uuids=uuid_A2))

    b_objs = B.query.bm25(
        query="B",
        return_references=FromReference(
            link_on="a",
            return_properties=["name"],
        ),
    ).objects
    assert b_objs[0].references["a"].objects[0].properties["name"] == "A1"
    assert b_objs[0].references["a"].objects[0].uuid == uuid_A1
    assert b_objs[0].references["a"].objects[1].properties["name"] == "A2"
    assert b_objs[0].references["a"].objects[1].uuid == uuid_A2

    C = collection_factory(
        name="C",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="b", target_collection=B.name),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    C.data.insert({"Name": "find me"}, references={"b": Reference.to(uuids=uuid_B)})

    c_objs = C.query.bm25(
        query="find",
        return_properties="name",
        return_references=FromReference(
            link_on="b",
            return_properties="name",
            return_metadata=MetadataQuery(last_update_time=True),
            return_references=FromReference(
                link_on="a",
                return_properties="name",
            ),
        ),
    ).objects
    assert c_objs[0].properties["name"] == "find me"
    assert c_objs[0].references["b"].objects[0].properties["name"] == "B"
    assert c_objs[0].references["b"].objects[0].metadata.last_update_time is not None
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].properties["name"] == "A1"
    )
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].properties["name"] == "A2"
    )


@pytest.mark.parametrize("level", ["col-col", "col-query", "query-col", "query-query"])
def test_mono_references_grpc_typed_dicts(
    collection_factory: CollectionFactory,
    collection_factory_get: CollectionFactoryGet,
    level: str,
) -> None:
    class AProps(TypedDict):
        name: str

    class BProps(TypedDict):
        name: str

    class BRefs(TypedDict):
        a: Annotated[
            CrossReference[AProps, None],
            ReferenceAnnotation(metadata=MetadataQuery(creation_time=True)),
        ]

    class CProps(TypedDict):
        name: str

    class CRefs(TypedDict):
        b: Annotated[CrossReference[BProps, BRefs], ReferenceAnnotation(include_vector=True)]

    dummy_a = collection_factory(
        name="a",
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    A = collection_factory_get(dummy_a.name, AProps)
    uuid_A1 = A.data.insert(AProps(name="A1"))
    uuid_A2 = A.data.insert(AProps(name="A2"))

    dummy_b = collection_factory(
        name="B",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="a", target_collection=A.name),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
    )
    B = collection_factory_get(dummy_b.name, BProps)
    uuid_B = B.data.insert(properties={"name": "B"}, references={"a": Reference.to(uuids=uuid_A1)})
    B.data.reference_add(
        from_uuid=uuid_B,
        from_property="a",
        to=Reference.to(uuids=uuid_A2),
    )

    b_objs = B.query.bm25(query="B", return_references=BRefs).objects
    assert b_objs[0].references["a"].objects[0].properties["name"] == "A1"
    assert b_objs[0].references["a"].objects[0].uuid == uuid_A1
    assert b_objs[0].references["a"].objects[0].references is None
    assert b_objs[0].references["a"].objects[1].properties["name"] == "A2"
    assert b_objs[0].references["a"].objects[1].uuid == uuid_A2
    assert b_objs[0].references["a"].objects[1].references is None

    dummy_c = collection_factory(
        name="C",
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
            Property(name="Age", data_type=DataType.INT),
        ],
        references=[
            ReferenceProperty(name="b", target_collection=B.name),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
    )
    C = collection_factory_get(dummy_c.name, CProps)
    C.data.insert(properties={"name": "find me"}, references={"b": Reference.to(uuids=uuid_B)})

    if level == "col-col":
        c_objs = (
            collection_factory_get(C.name, CProps, CRefs)
            .query.bm25(query="find", include_vector=True)
            .objects
        )
    elif level == "col-query":
        c_objs = (
            collection_factory_get(C.name, CProps)
            .query.bm25(
                query="find",
                include_vector=True,
                return_references=CRefs,
            )
            .objects
        )
    elif level == "query-col":
        c_objs = (
            collection_factory_get(C.name, data_model_refs=CRefs)
            .query.bm25(
                query="find",
                include_vector=True,
                return_properties=CProps,
            )
            .objects
        )
    else:
        c_objs = (
            collection_factory_get(C.name)
            .query.bm25(
                query="find",
                include_vector=True,
                return_properties=CProps,
                return_references=CRefs,
            )
            .objects
        )
    assert (
        c_objs[0].properties["name"] == "find me"
    )  # happy path (in type and in return_properties)
    assert c_objs[0].uuid is not None
    assert c_objs[0].vector is not None
    assert (
        c_objs[0].properties.get("not_specified") is None
    )  # type is str but instance is None (in type but not in return_properties)
    assert c_objs[0].references["b"].objects[0].properties["name"] == "B"
    assert c_objs[0].references["b"].objects[0].uuid == uuid_B
    assert c_objs[0].references["b"].objects[0].vector is not None
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].properties["name"] == "A1"
    )
    assert c_objs[0].references["b"].objects[0].references["a"].objects[0].uuid == uuid_A1
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].metadata.creation_time
        is not None
    )
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].properties["name"] == "A2"
    )
    assert c_objs[0].references["b"].objects[0].references["a"].objects[1].uuid == uuid_A2
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].metadata.creation_time
        is not None
    )


def test_multi_references_grpc(collection_factory: CollectionFactory) -> None:
    A = collection_factory(
        name="A",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    uuid_A = A.data.insert(properties={"Name": "A"})

    B = collection_factory(
        name="B",
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuid_B = B.data.insert({"Name": "B"})

    C = collection_factory(
        name="C",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferencePropertyMultiTarget(name="ref", target_collections=[A.name, B.name]),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    C.data.insert(
        {
            "Name": "first",
        },
        references={
            "ref": Reference.to_multi_target(uuids=uuid_A, target_collection=A.name),
        },
    )
    C.data.insert(
        {
            "Name": "second",
        },
        references={
            "ref": Reference.to_multi_target(uuids=uuid_B, target_collection=B.name),
        },
    )

    objects = C.query.bm25(
        query="first",
        return_properties="name",
        return_references=FromReferenceMultiTarget(
            link_on="ref",
            target_collection=A.name,
            return_properties=["name"],
            return_metadata=MetadataQuery(last_update_time=True),
        ),
    ).objects
    assert objects[0].properties["name"] == "first"
    assert len(objects[0].references["ref"].objects) == 1
    assert objects[0].references["ref"].objects[0].properties["name"] == "A"
    assert objects[0].references["ref"].objects[0].metadata.last_update_time is not None

    objects = C.query.bm25(
        query="second",
        return_properties="name",
        return_references=FromReferenceMultiTarget(
            link_on="ref",
            target_collection=B.name,
            return_properties=[
                "name",
            ],
            return_metadata=MetadataQuery(last_update_time=True),
        ),
    ).objects
    assert objects[0].properties["name"] == "second"
    assert len(objects[0].references["ref"].objects) == 1
    assert objects[0].references["ref"].objects[0].properties["name"] == "B"
    assert objects[0].references["ref"].objects[0].metadata.last_update_time is not None


def test_references_batch(collection_factory: CollectionFactory) -> None:
    ref_collection = collection_factory(
        name="To",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[Property(name="num", data_type=DataType.INT)],
    )
    num_objects = 10

    uuids_to = ref_collection.data.insert_many(
        [DataObject(properties={"num": i}) for i in range(num_objects)]
    ).uuids.values()
    collection = collection_factory(
        name="From",
        properties=[
            Property(name="num", data_type=DataType.INT),
        ],
        references=[ReferenceProperty(name="ref", target_collection=ref_collection.name)],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuids_from = collection.data.insert_many(
        [DataObject(properties={"num": i}) for i in range(num_objects)]
    ).uuids.values()

    batch_return = collection.data.reference_add_many(
        [
            *[
                DataReferenceOneToMany(
                    from_property="ref",
                    from_uuid=list(uuids_from)[i],
                    to=Reference.to(list(uuids_to)[i]),
                )
                for i in range(num_objects)
            ],
            *[
                DataReference(
                    from_property="ref",
                    from_uuid=list(uuids_from)[i],
                    to_uuid=list(uuids_to)[i],
                )
                for i in range(num_objects)
            ],
        ]
    )

    assert batch_return.has_errors is False

    objects = collection.query.fetch_objects(
        return_properties=[
            "num",
        ],
        return_references=[
            FromReference(link_on="ref"),
        ],
    ).objects

    for obj in objects:
        assert obj.properties["num"] == obj.references["ref"].objects[0].properties["num"]


def test_insert_many_with_refs(collection_factory: CollectionFactory) -> None:
    collection = collection_factory(
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    collection.config.add_reference(
        ReferenceProperty(name="self", target_collection=collection.name)
    )

    uuid1 = collection.data.insert({"name": "A"})
    uuid2 = collection.data.insert({"name": "B"})

    batch_return = collection.data.insert_many(
        [
            DataObject(
                properties={"name": "C"},
                references={"self": Reference.to(uuids=uuid1)},
            ),
            DataObject(
                properties={"name": "D"},
                references={"self": Reference.to(uuids=uuid2)},
            ),
        ]
    )
    assert batch_return.has_errors is False

    for obj in collection.query.fetch_objects(
        return_properties=["name"], return_references=FromReference(link_on="self")
    ).objects:
        if obj.properties["name"] in ["A", "B"]:
            assert obj.references is None
        else:
            assert obj.references is not None


def test_references_batch_with_errors(collection_factory: CollectionFactory) -> None:
    to = collection_factory(
        name="To",
        vectorizer_config=Configure.Vectorizer.none(),
    )

    collection = collection_factory(
        name="From",
        properties=[
            Property(name="num", data_type=DataType.INT),
        ],
        references=[ReferenceProperty(name="ref", target_collection=to.name)],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    batch_return = collection.data.reference_add_many(
        [DataReference(from_property="doesNotExist", from_uuid=uuid.uuid4(), to_uuid=uuid.uuid4())],
    )
    assert batch_return.has_errors is True
    assert 0 in batch_return.errors


# commented out due to mypy failures since it is stale code
# @pytest.mark.skip(reason="string syntax has been temporarily removed from the API")
# def test_references_with_string_syntax(client: weaviate.WeaviateClient):
#     name1 = "TestReferencesWithStringSyntaxA"
#     name2 = "TestReferencesWithStringSyntaxB"
#     client.collections.delete(name1)
#     client.collections.delete(name2)

#     client.collections.create(
#         name=name1,
#         vectorizer_config=Configure.Vectorizer.none(),
#         properties=[
#             Property(name="Name", data_type=DataType.TEXT),
#             Property(name="Age", data_type=DataType.INT),
#             Property(name="Weird__Name", data_type=DataType.INT),
#         ],
#     )

#     uuid_A = client.collections.get(name1).data.insert(
#         properties={"Name": "A", "Age": 1, "Weird__Name": 2}
#     )

#     client.collections.get(name1).query.fetch_object_by_id(uuid_A)

#     client.collections.create(
#         name=name2,
#         properties=[
#             Property(name="Name", data_type=DataType.TEXT),
#         ],
#         references=[ReferenceProperty(name="ref", target_collection=name1)],
#         vectorizer_config=Configure.Vectorizer.none(),
#     )

#     client.collections.get(name2).data.insert(
#         {"Name": "B"}, references={"ref": Reference.to(uuids=uuid_A)}
#     )

#     objects = (
#         client.collections.get(name2)
#         .query.bm25(
#             query="B",
#             return_properties=[
#                 "name",
#                 "__ref__properties__Name",
#                 "__ref__properties__Age",
#                 "__ref__properties__Weird__Name",
#                 "__ref__metadata__last_update_time_unix",
#             ],
#         )
#         .objects
#     )

#     assert objects[0].properties["name"] == "B"
#     assert objects[0].references["ref"].objects[0].properties["name"] == "A"
#     assert objects[0].references["ref"].objects[0].properties["age"] == 1
#     assert objects[0].references["ref"].objects[0].properties["weird__Name"] == 2
#     assert objects[0].references["ref"].objects[0].uuid == uuid_A
#     assert objects[0].references["ref"].objects[0].metadata.last_update_time_unix is not None


def test_warning_refs_as_props(
    collection_factory: CollectionFactory, request: SubRequest, recwarn: pytest.WarningsRecorder
) -> None:
    collection_factory(
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
            ReferenceProperty(name="ref", target_collection=_sanitize_collection_name(request.node.name)),  # type: ignore
        ],
    )

    assert len(recwarn) == 1
    w = recwarn.pop()
    assert issubclass(w.category, DeprecationWarning)
    assert str(w.message).startswith("Dep007")


def test_object_without_references(collection_factory: CollectionFactory) -> None:
    to = collection_factory(name="To", vectorizer_config=Configure.Vectorizer.none())

    source = collection_factory(
        name="From",
        references=[
            ReferenceProperty(name="ref_partial", target_collection=to.name),
            ReferenceProperty(name="ref_full", target_collection=to.name),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    uuid_to = to.data.insert(properties={})

    uuid_from1 = source.data.insert(
        references={"ref_partial": Reference.to(uuid_to), "ref_full": Reference.to(uuid_to)},
        properties={},
    )
    uuid_from2 = source.data.insert(references={"ref_full": Reference.to(uuid_to)}, properties={})

    obj1 = source.query.fetch_object_by_id(
        uuid_from2,
        return_references=[
            QueryReference(link_on="ref_full"),
            QueryReference(link_on="ref_partial"),
        ],
    )
    assert "ref_full" in obj1.references and "ref_partial" not in obj1.references

    obj2 = source.query.fetch_object_by_id(
        uuid_from1,
        return_references=[
            QueryReference(link_on="ref_full"),
            QueryReference(link_on="ref_partial"),
        ],
    )
    assert "ref_full" in obj2.references and "ref_partial" in obj2.references
