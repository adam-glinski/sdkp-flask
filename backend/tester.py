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
    returns:
        - `True` if the test passed
        - `False` if the test failed
    """
    output = subprocess.run(
            ["python3", "-c", script],
            input=input,
            capture_output=True,
            text=True
    )

    output = output.stdout.strip()
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
    assert test_code(fib_code, input="", expected_output="34")
    assert test_code(palindrome_code, input="zakaz", expected_output="True")
    assert not test_code(palindrome_code, input="Hello, World!", expected_output="True")
