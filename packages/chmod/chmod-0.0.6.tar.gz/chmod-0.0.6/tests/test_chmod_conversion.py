import pytest
from chmod import ChmodConversion
class TestChmodConversion():
    
    def setup_method(self):
        self.a = ChmodConversion()
    
    
    def test_int_to_perm(self):
        assert self.a.int_to_perm(755) == "rwxr-xr-x"
        assert self.a.int_to_perm(644) == "rw-r--r--"
        assert self.a.int_to_perm(777) == "rwxrwxrwx"
        assert self.a.int_to_perm(771) == "rwxrwx--x"
    
    def test_perm_to_int(self):
        assert self.a.perm_to_int("rwxr-xr-x") == "755"
        assert self.a.perm_to_int("rw-r--r--") == "644"
        assert self.a.perm_to_int("rwxrwxrwx") == "777"
        assert self.a.perm_to_int("--x---rwx") == "107"
    
    def test_error_handling_int_to_perm(self):
        assert self.a.int_to_perm(182) == "Incorrect value"
        assert self.a.int_to_perm(912) == "Incorrect value"
        assert self.a.int_to_perm(178) == "Incorrect value"
        assert self.a.int_to_perm(888) == "Incorrect value"
    
    def test_error_handling_perm_to_int(self):
        assert self.a.perm_to_int("") == "Empty string"
        assert self.a.perm_to_int("rwxrw") == "Incorrect length"
        assert self.a.perm_to_int("asd") == "asd: Incorrect format (has to be in this format - rwx)\n"
        assert self.a.perm_to_int("abc---ccc") == "abc: Incorrect format (has to be in this format - rwx)\nccc: Incorrect format (has to be in this format - rwx)\n"
        
if __name__ == '__main__':
    pytest.main()
