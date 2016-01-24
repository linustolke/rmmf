import unittest
import os
import subprocess

class TestDemoTransform(unittest.TestCase):
    def setUp(self):
        self.orig_dir = os.getcwd()
        os.chdir("test/demo")

    def tearDown(self):
        os.chdir(self.orig_dir)

    def test1(self):
        p1 = subprocess.Popen(["python", "../../rmmf.py"],
                              stdout=subprocess.PIPE)
        (sout, serr) = p1.communicate()
        self.assertEqual(p1.returncode, 0)

        p2 = subprocess.Popen(["diff", "makefile.output", "-"],
                              stdin=subprocess.PIPE)
        p2.communicate(sout)
        self.assertEqual(p2.returncode, 0)

