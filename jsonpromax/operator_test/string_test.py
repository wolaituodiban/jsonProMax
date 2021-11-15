import jsonpromax as jpm
import traceback


def test_rename():
    op = jpm.Rename('a', 'b')

    def test_not_dict():
        try:
            op([1])
        except Exception:
            traceback.print_exc()
            print('success')

    test_not_dict()


if __name__ == '__main__':
    test_rename()
    print('aha')
