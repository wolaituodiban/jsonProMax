import jsonpromax as jpm


def test_relationship():
    rs = jpm.Relationship(
        left_name='haha', right_name='hehe', right_fields=['c', 'd'], on='d', left_on=['e'], right_on='g',
        time_conds=[
            ('e', 'f', 7, None),
            ('e', 'g', 1, -8)
        ]
    )
    print(rs.gen_sql(['a']))


def test_entity_set():
    es = jpm.EntitySet()
    es.add_entity('haha', 'b')
    es.add_entity('hehe', 'c')
    es.add_entity('hihi', 'd')
    es.add_rs('haha', 'hehe', 'b', on='d')
    es.add_rs('hehe', 'hihi', 'b', on='d')
    print(es._gen_sql('haha'))


if __name__ == '__main__':
    # test_relationship()
    test_entity_set()