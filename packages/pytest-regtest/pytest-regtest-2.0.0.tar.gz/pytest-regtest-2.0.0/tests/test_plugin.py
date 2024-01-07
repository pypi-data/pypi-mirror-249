import pytest
import sys

IS_WIN = sys.platform == "win32"


@pytest.fixture
def create_test_regtest_context_manager(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest, tmpdir):

            print("this is not recorded")
            with regtest:
                print("this is expected outcome")
                print(tmpdir.join("test").strpath)
                print(tempfile.gettempdir())
                print(tempfile.mkdtemp())
                print("obj id is", hex(id(tempfile)))

         """
    )
    yield testdir


@pytest.fixture
def create_test_regtest_fh(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest, tmpdir):

            print("this is not recorded")
            print("this is expected outcome", file=regtest)
            print(tmpdir.join("test").strpath, file=regtest)
            print(tempfile.gettempdir(), file=regtest)
            print(tempfile.mkdtemp(), file=regtest)
            print("obj id is", hex(id(tempfile)), file=regtest)

         """
    )
    yield testdir


@pytest.fixture
def create_test_regtest_all(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    yield testdir


def test_regtest_context_manager(create_test_regtest_context_manager):
    _test_regtest_output(create_test_regtest_context_manager)


def test_regtest_fh(create_test_regtest_fh):
    _test_regtest_output(create_test_regtest_fh)


def test_regtest_all(create_test_regtest_all):
    _test_regtest_output(create_test_regtest_all)


def _test_regtest_output(test_setup):
    result = test_setup.runpytest()
    result.assert_outcomes(failed=1, passed=0, xfailed=0)

    expected_diff = """
                    >   --- is
                    >   +++ tobe
                    >   @@ -1,5 +0,0 @@
                    >   -this is expected outcome
                    >   -<tmpdir_from_fixture>/test
                    >   -<tmpdir_from_tempfile_module>
                    >   -<tmpdir_from_tempfile_module>
                    >   -obj id is 0x?????????
                    """.strip().split(
        "\n"
    )

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )


def test_xfail(testdir):

    testdir.makepyfile(
        """
        import tempfile
        import pytest

        @pytest.mark.xfail
        def test_regtest(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=0, passed=0, xfailed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(xpassed=1)

    result = testdir.runpytest()
    result.assert_outcomes(xpassed=1)


def test_failed_test(testdir):

    testdir.makepyfile(
        """
        import tempfile
        import pytest

        def test_regtest(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))

            assert False
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(failed=1)


def test_converter_pre(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_pre

        @register_converter_pre
        def to_upper_conv(line, request):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print("obj id is 0xabcdeffff")
         """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)

    expected_diff = """
                    >   --- is
                    >   +++ tobe
                    >   @@ -1,2 +0,0 @@
                    >   -THIS IS EXPECTED OUTCOME
                    >   -OBJ ID IS 0XABCDEFFFF
                    """.strip().split(
        "\n"
    )

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_converter_post(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_post

        @register_converter_post
        def to_upper_conv(line, request):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)

    expected_diff = """
                    >   --- is
                    >   +++ tobe
                    >   @@ -1,5 +0,0 @@
                    >   -THIS IS EXPECTED OUTCOME
                    >   -<TMPDIR_FROM_FIXTURE>/TEST
                    >   -<TMPDIR_FROM_TEMPFILE_MODULE>
                    >   -<TMPDIR_FROM_TEMPFILE_MODULE>
                    >   -OBJ ID IS 0X?????????
                    """.strip().split(
        "\n"
    )

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_consider_line_endings(create_test_regtest_fh):
    create_test_regtest_fh.runpytest("--regtest-reset")

    # just check if cmd line flags work without throwing exceptions:
    result = create_test_regtest_fh.runpytest("--regtest-consider-line-endings")
    result.assert_outcomes(failed=1)


def test_tee(create_test_regtest_fh):
    create_test_regtest_fh.runpytest("--regtest-reset")

    # just check if cmd line flags work without throwing exceptions:
    result = create_test_regtest_fh.runpytest("--regtest-tee")
    result.assert_outcomes(failed=1)

