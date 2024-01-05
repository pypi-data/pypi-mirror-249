from os import environ

import pytest

import greenplumpython as gp
from greenplumpython.builtins.functions import generate_series
from tests import db


@pytest.fixture
def t(db: gp.Database):
    t = db.assign(id=lambda: generate_series(0, 9))
    return t


def test_const_dataframe_columns(db: gp.Database):
    columns = {"a": [1, 2, 3], "b": [1, 2, 3]}
    t = db.create_dataframe(columns=columns)
    t = t.save_as(column_names=["a", "b"], temp=True)
    assert sorted([tuple(row.values()) for row in t]) == [(1, 1), (2, 2), (3, 3)]

    assert list(next(iter(t)).keys()) == ["a", "b"]


def test_const_dataframe_rows(db: gp.Database):
    rows = [(1,), (2,), (3,)]
    t = db.create_dataframe(rows=rows, column_names=["id"])
    t = t.save_as(column_names=["id"], temp=True)
    assert sorted([tuple(row.values()) for row in t]) == sorted(rows)

    assert len(next(iter(t)).keys()) == 1
    for row in next(iter(t)).keys():
        assert row == "id"


def test_dataframe_save_drop(db: gp.Database):
    rows = [(1,), (2,), (3,)]
    t = db.create_dataframe(rows=rows, column_names=["id"])
    t.save_as("test_dataframe_save_drop", schema="test", column_names=["id"])
    t.save_as("test_dataframe_save_drop", schema="test", column_names=["id"], drop_if_exists=True)
    with pytest.raises(Exception) as exc_info:
        t.save_as("test_dataframe_save_drop", schema="test", column_names=["id"])
    assert 'relation "test_dataframe_save_drop" already exists\n' in str(exc_info.value)
    t.save_as(
        "test_dataframe_save_drop",
        schema="test",
        column_names=["id"],
        drop_if_exists=True,
        drop_cascade=True,
    )


def test_dataframe_getitem_str(db: gp.Database):
    rows = [(1,), (2,), (3,)]
    t = db.create_dataframe(rows=rows, column_names=["id"])
    c = t["id"]
    assert str(c) == f'{t._name}."id"'


def test_dataframe_getitem_sub_columns(db: gp.Database):
    # fmt: off
    rows = [(1, 2,), (1, 3,), (2, 2,), (3, 1,), (3, 4,)]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "num"])
    t_sub = t[["id", "num"]]
    for row in t_sub:
        assert "id" in row and "num" in row


def test_dataframe_getitem_slice_limit(db: gp.Database, t: gp.DataFrame):
    assert len(list(t[:2])) == 2


def test_dataframe_getitem_slice_offset(db: gp.Database, t: gp.DataFrame):
    assert len(list(t[7:])) == 3


def test_dataframe_getitem_slice_off_limit(db: gp.Database, t: gp.DataFrame):
    assert len(list(t[2:5])) == 3


def test_dataframe_getitem_slice_off_limit(db: gp.Database, t: gp.DataFrame):
    query = t[:]._serialize()
    assert len(list(t[:])) == 10
    assert "LIMIT" in query


def test_dataframe_display_repr(db: gp.Database):
    # fmt: off
    rows = [(1, 1, "Lion",), (2, 2, "Tiger",), (3, 3, "Wolf",), (4, 4, "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "idd", "animal"])
    t = t.order_by("id")[:]
    print(t)
    expected = (
        "-------------------\n"
        " id | idd | animal \n"
        "----+-----+--------\n"
        "  1 |   1 | Lion   \n"
        "  2 |   2 | Tiger  \n"
        "  3 |   3 | Wolf   \n"
        "  4 |   4 | Fox    \n"
        "-------------------\n"
        "(4 rows)\n"
    )
    assert str(t) == expected


def test_dataframe_display_repr_zero(db: gp.Database):
    # fmt: off
    rows = [(0, "Lion",), (2, "Tiger",), (3, "Wolf",), (4, "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "animal"])
    t = t.order_by("id")[:]
    print(t)
    expected = (
        "-------------\n"
        " id | animal \n"
        "----+--------\n"
        "  0 | Lion   \n"
        "  2 | Tiger  \n"
        "  3 | Wolf   \n"
        "  4 | Fox    \n"
        "-------------\n"
        "(4 rows)\n"
    )
    assert str(t) == expected


def test_dataframe_display_repr_long_content(db: gp.Database):
    # fmt: off
    rows = [(1, "Lion",), (2, "Tigerrrrrrrrrrrr",), (3, "Wolf",), (4, "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["iddddddddddddddddddd", "animal"])
    t = t.order_by("iddddddddddddddddddd")[:]
    print(t)
    expected = (
        "-----------------------------------------\n"
        " iddddddddddddddddddd | animal           \n"
        "----------------------+------------------\n"
        "                    1 | Lion             \n"
        "                    2 | Tigerrrrrrrrrrrr \n"
        "                    3 | Wolf             \n"
        "                    4 | Fox              \n"
        "-----------------------------------------\n"
        "(4 rows)\n"
    )
    assert str(t) == expected


def test_dataframe_display_repr_html(db: gp.Database):
    # fmt: off
    rows = [(1, "Lion",), (2, "Tiger",), (3, "Wolf",), (4, "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "animal"])
    expected = (
        "<table>\n"
        "\t<tr>\n"
        "\t\t<th>id</th>\n"
        "\t\t<th>animal</th>\n"
        "\t</tr>\n"
        "\t<tr>\n"
        "\t\t<td>1</td>\n"
        "\t\t<td>Lion</td>\n"
        "\t</tr>\n"
        "\t<tr>\n"
        "\t\t<td>2</td>\n"
        "\t\t<td>Tiger</td>\n"
        "\t</tr>\n"
        "\t<tr>\n"
        "\t\t<td>3</td>\n"
        "\t\t<td>Wolf</td>\n"
        "\t</tr>\n"
        "\t<tr>\n"
        "\t\t<td>4</td>\n"
        "\t\t<td>Fox</td>\n"
        "\t</tr>\n"
        "</table>"
    )
    assert (t.order_by("id")[:]._repr_html_()) == expected


def test_dataframe_display_repr_zero_rows(db: gp.Database):
    # fmt: off
    rows = [(1, "Lion",), (2, "Tiger",), (3, "Wolf",), (4, "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "animal"])
    t = t[lambda t: t["id"] == 0]
    print(t)
    assert str(t) == "----\n" "----\n" "----\n" "(0 rows)\n"
    assert (t._repr_html_()) == ""


def test_dataframe_display_result_null(db: gp.Database):
    # fmt: off
    rows = [([1,1,1], None,), ([2,2,2], "Tiger",), ([3,3,3], None,), ([4,None,4], "Fox")]
    # fmt: on
    t = db.create_dataframe(rows=rows, column_names=["id", "animal"])
    t = t.order_by("id")[:]
    print(t)
    expected = (
        "-----------------------\n"
        " id           | animal \n"
        "--------------+--------\n"
        " [1, 1, 1]    |        \n"
        " [2, 2, 2]    | Tiger  \n"
        " [3, 3, 3]    |        \n"
        " [4, None, 4] | Fox    \n"
        "-----------------------\n"
        "(4 rows)\n"
    )
    assert str(t) == expected


def test_dataframe_assign_const(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    results = nums.assign(x=lambda _: "hello")
    for row in results:
        assert "num" in row and "x" in row and row["x"] == "hello"


@gp.create_function
def add_one(num: int) -> int:
    return num + 1


def test_dataframe_assign_expr(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    # FIXME: How to remove the intermdeiate variable `nums`?
    # FIXME: How to support functions returning more than one column?
    results = nums.assign(result=lambda nums: add_one(nums["num"]))
    for row in results:
        assert row["result"] == row["num"] + 1


def test_dataframe_assign_same_column_name(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    results = nums.assign(num=lambda nums: add_one(nums["num"]))
    with pytest.raises(Exception) as exc_info:
        next(iter(results))
    assert "Duplicate column name(s) found" in str(exc_info.value)


def test_table_assign_composite_type(db: gp.Database):
    class rank_label:
        val: int
        label: str

    @gp.create_function
    def my_rank_label(val: int) -> rank_label:
        return {"val": val, "label": "label"}

    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    results = nums.assign(result=lambda nums: my_rank_label(nums["num"]))
    results = results.assign(result2=lambda nums: my_rank_label(nums["num"]))
    results = results.assign(next_val=lambda nums: add_one(nums["num"]))
    for row in results:
        assert row["num"] == row["result"]["val"] and row["result"]["label"] == "label"
        assert (
            row["result2"]["val"] == row["result"]["val"]
            and row["result2"]["label"] == row["result"]["label"]
        )
        assert row["next_val"] == row["num"] + 1


def test_table_assign_same_base(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    nums2 = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    with pytest.raises(Exception) as exc_info:
        nums.assign(num2=lambda _: nums2["num"])
    assert "Newly included columns must be based on the current dataframe" in str(exc_info.value)


def test_table_assign_multiple_col(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    results = nums.assign(a=lambda t: t["num"], b=lambda t: t["num"])
    for row in results:
        assert row["num"] == row["a"] == row["b"]


def test_iter_break(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(3)], column_names=["num"])
    results = []
    for row in nums:
        results.append(row["num"])
        break
    for row in nums:
        results.append(row["num"])
    assert results == [0, 0, 1, 2]


def test_table_refresh_add_rows(db: gp.Database):
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    t = nums.save_as(column_names=["num"], temp=True)
    assert len(list(t)) == 10

    db._execute(f"INSERT INTO {t._qualified_table_name}(num) VALUES (10);", has_results=False)

    assert len(list(t)) == 10
    t.refresh()
    assert len(list(t)) == 11


def test_table_refresh_add_columns(db: gp.Database):
    # Initial DataFrame
    nums = db.create_dataframe(rows=[(i,) for i in range(10)], column_names=["num"])
    t = nums.save_as(column_names=["num"], temp=True)
    assert list(next(iter(t)).keys()) == ["num"]
    assert sorted(row["num"] for row in t) == sorted(list(range(10)))

    # Add a new column
    db._execute(f"ALTER TABLE {t._qualified_table_name} ADD num_copy int;", has_results=False)
    assert len(next(iter(t)).keys()) == 1
    for row in next(iter(t)).keys():
        assert row == "num"
    # Refresh DataFrame contents
    t.refresh()
    assert list(next(iter(t)).keys()) == ["num", "num_copy"]
    for row in t:
        assert row["num_copy"] is None

    # Update column
    db._execute(f"UPDATE {t._qualified_table_name} SET num_copy=num;", has_results=False)
    for row in t:
        assert row["num_copy"] is None
    # Refresh DataFrame contents
    t.refresh()
    for row in t:
        assert row["num_copy"] is not None and row["num_copy"] == row["num"]


def test_table_distinct(db: gp.Database):
    rows = [(i, 1) for i in range(10)]
    t = db.create_dataframe(rows=rows, column_names=["i", "j"])

    result = list(t.distinct_on("i", "j"))
    assert len(result) == len(rows)
    for row in result:
        assert "i" in row and "j" in row

    result = list(t.distinct_on("j"))
    assert len(result) == 1
    for row in result:
        assert "i" in row and "j" in row


def test_table_non_default_schema(db: gp.Database):
    pg_class = db.create_dataframe(table_name="pg_class", schema="pg_catalog")
    assert len(list(pg_class)) > 0


def test_save_as_non_default_schema(db: gp.Database):
    columns = {"a": [1, 2, 3], "b": [1, 2, 3]}
    t = db.create_dataframe(columns=columns)
    t.save_as("const_dataframe", column_names=["a", "b"], schema="test")
    t = db.create_dataframe(table_name="const_dataframe", schema="test")
    assert sorted([tuple(row.values()) for row in t]) == [(1, 1), (2, 2), (3, 3)]


def test_table_with_ao(db: gp.Database):
    result = db._execute("SELECT VERSION();")

    if not result:
        return

    version: str = result[0]["version"]

    if "Greenplum" not in version:
        return

    columns = {"a": [1, 2, 3], "b": [1, 2, 3]}
    t = db.create_dataframe(columns=columns)
    # pass if no error
    t.save_as(
        "ao_dataframe", column_names=["a", "b"], temp=True, storage_params={"appendoptimized": True}
    )


def test_table_with_aoco(db: gp.Database):
    result = db._execute("SELECT VERSION();")

    if not result:
        return

    version: str = result[0]["version"]

    if "Greenplum" not in version:
        return

    columns = {"a": [1, 2, 3], "b": [1, 2, 3]}
    t = db.create_dataframe(columns=columns)
    # pass if no error
    t.save_as(
        "aoco_dataframe",
        column_names=["a", "b"],
        temp=True,
        storage_params={"appendoptimized": True, "orientation": "column"},
    )


def test_table_distributed_randomly(db: gp.Database):
    result = db._execute("SELECT VERSION();")

    if not result:
        return

    version: str = result[0]["version"]

    if "Greenplum" not in version:
        return

    t = db.assign(id=lambda: generate_series(0, 9))
    # pass if no error
    t.save_as(
        "randomly_dataframe",
        column_names=["id"],
        temp=True,
        distribution_type="randomly",
    )
    query = f"""select pg_get_table_distributedby('"pg_temp"."randomly_dataframe"'::regclass) distributedby"""
    result = db._execute(query)
    for row in result:
        assert row["distributedby"] == "DISTRIBUTED RANDOMLY"
    db._execute("DROP TABLE pg_temp.randomly_dataframe", has_results=False)


def test_table_distributed_replicated(db: gp.Database):
    result = db._execute("SELECT VERSION();")

    if not result:
        return

    version: str = result[0]["version"]

    if "Greenplum" not in version:
        return

    t = db.assign(id=lambda: generate_series(0, 9))
    # pass if no error
    t.save_as(
        "replicated_dataframe",
        column_names=["id"],
        temp=True,
        distribution_type="replicated",
    )
    query = f"""select pg_get_table_distributedby('"pg_temp"."replicated_dataframe"'::regclass) distributedby"""
    result = db._execute(query)
    for row in result:
        assert row["distributedby"] == "DISTRIBUTED REPLICATED"


def test_table_distributed_hash(db: gp.Database):
    result = db._execute("SELECT VERSION();")

    if not result:
        return

    version: str = result[0]["version"]

    if "Greenplum" not in version:
        return

    t = db.assign(id=lambda: generate_series(0, 9))
    # pass if no error
    t.save_as(
        "hash_dataframe",
        column_names=["id"],
        temp=True,
        distribution_type="hash",
        distribution_key={"id"},
    )
    query = f"""select pg_get_table_distributedby('"pg_temp"."hash_dataframe"'::regclass) distributedby"""
    result = db._execute(query)
    for row in result:
        assert row["distributedby"] == "DISTRIBUTED BY (id)"


import pandas as pd


def test_table_to_pandas_dataframe(db: gp.Database):
    data = {"num": [1, 2, 3], "text": ["x", "y", "z"]}
    df = pd.DataFrame(data)
    df_from_gp = pd.DataFrame.from_records(iter(db.create_dataframe(columns=data)))
    assert df.equals(df_from_gp)


def test_table_from_pandas_dataframe(db: gp.Database):
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # TODO: support db.create_dataframe(columns=df) after introduce numpy as
    # a dependency
    gp_df = db.create_dataframe(columns=df.to_dict("list"))
    assert len(list(gp_df)) == 3

    gp_df = db.create_dataframe(rows=df.to_dict("records"))
    assert len(list(gp_df)) == 3


def test_dataframe_from_table(db: gp.Database):
    t = db.create_dataframe(table_name="pg_class")[:1]
    assert len(list(t)) == 1


def test_const_non_ascii(db: gp.Database):
    df = db.create_dataframe(columns={"Ø": ["Ø"]})
    for row in df[["Ø"]]:
        assert row["Ø"] == "Ø"
