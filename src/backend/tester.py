import subprocess
import difflib


def get_diff(expected: str, actual: str) -> str:
    expected_lines = expected.strip().splitlines()
    actual_lines = actual.strip().splitlines()

    diff = difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile='expected',
            tofile='actual',
            lineterm=''
    )
    for line in diff:
        print(line)
    diff_str = "".join(diff)

    return diff_str


def test_code(script: str, input: str, expected_output: str) -> bool:
    """
    Function that tests `script` by passing in `input` as stdin, and checking the output against the `output` arg.

    returns:
        bool: True if the expected_output matches the actual output.
    """
    output = subprocess.run(
            ["python3", "-c", script],
            input=input,
            capture_output=True,
            text=True
    )

    err = output.stderr.strip()
    output = output.stdout.strip()
    if err != "":  # Assume script should never throw errors
        print(f"[DEBUG]{script=} returned err: {err}")
        return False
    expected_output = expected_output

    if output == expected_output:
        return True

    # print(get_diff(expected_output, output))
    get_diff(expected_output, output)
    return False


if __name__ == "__main__":
    fib_code = """
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
print(fibonacci(9))  # Output: 34
    """

    palindrome_code = """
def is_palindrome(t):
    return t == t[::-1]

print(is_palindrome(input()))
    """

    error_code = """
this code shouldnt work
    """
    assert test_code(fib_code, input="", expected_output="34")
    assert test_code(palindrome_code, input="zakaz", expected_output="True")
    assert not test_code(palindrome_code, input="Hello, World!", expected_output="True")
    assert not test_code(error_code, input="3", expected_output="3")
