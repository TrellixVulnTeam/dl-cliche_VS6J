import unittest
from dlcliche.utils import *

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_folder = Path('_tmp')
        ensure_folder(cls.tmp_folder)

    @classmethod
    def tearDownClass(cls):
        ensure_delete(cls.tmp_folder)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flatten_list(self):
        X = [
            [[[1.0,0.0,0.0]]],
            [[[0.8,0.0,0.1]]],
            [[[0.5,0.5,0.0]]],
            [[[0.4,0.4,0.0]]],
            [[[0.6,0.7,0.0]]],
            [[[0.1,0.5,0.5]]],
        ]
        y1 = [
            [[1.0,0.0,0.0]],
            [[0.8,0.0,0.1]],
            [[0.5,0.5,0.0]],
            [[0.4,0.4,0.0]],
            [[0.6,0.7,0.0]],
            [[0.1,0.5,0.5]],
        ]

        self.assertEqual(y1, flatten_list(X))

    def make_folder_for_sure(self, folder):
        ensure_folder(folder)
        self.assertTrue(folder.is_dir())

    def make_src_files_for_copy_tests(self, src_folder):
        self.make_folder_for_sure(src_folder)
        for i in range(5):
            sub_folder = src_folder/('sub%d' % i)
            self.make_folder_for_sure(sub_folder)
        for i in range(5):
            sub_file = src_folder/('file%d.txt' % i)
            f = sub_file.open('w')
            f.write('abcde%d' % i)
            f.close()
        return sorted(list(src_folder.iterdir()))

    def test_1_make_copy_to(self):
        self.assertTrue(self.tmp_folder.is_dir())
        copy_src = self.tmp_folder/'src'
        dst = self.tmp_folder/'dst'
        ensure_delete(copy_src)
        ensure_delete(dst)

        src_all = self.make_src_files_for_copy_tests(copy_src)

        make_copy_to(dst, src_all, operation=symlink_file)
        for i in range(5):
            sub_folder = dst/('sub%d' % i)
            self.assertTrue(sub_folder.is_symlink())
        for i in range(5):
            sub_file = dst/('file%d.txt' % i)
            self.assertTrue(sub_file.is_symlink())
        ensure_delete(dst)

        make_copy_to(dst, src_all, operation=copy_any)
        for i in range(5):
            sub_folder = dst/('sub%d' % i)
            self.assertTrue(sub_folder.is_dir())
        for i in range(5):
            f = (dst/('file%d.txt' % i)).open()
            text = f.read()
            f.close()
            self.assertEqual('abcde%d' % i, text)

    def test_2_copy_move(self):
        self.assertTrue(self.tmp_folder.is_dir())
        copy_src = self.tmp_folder/'src'
        dst = self.tmp_folder/'dst'
        ensure_delete(copy_src)
        src_all = self.make_src_files_for_copy_tests(copy_src)

        self.assertTrue(dst.is_dir())

        # move/copy single file
        for shift, fn in zip([0, 1], [copy_any, move_file]):
            # clean up
            ensure_delete(dst)
            ensure_folder(dst)
            # test
            fn(src_all[5+shift], str(dst))
            self.assertTrue((dst/src_all[5+shift].name).is_dir())
            fn(src_all[shift], str(dst))
            f = (dst/('file%d.txt'%shift)).open()
            text = f.read()
            f.close()
            self.assertEqual('abcde%d'%shift, text)

if __name__ == '__main__':
    unittest.main()
