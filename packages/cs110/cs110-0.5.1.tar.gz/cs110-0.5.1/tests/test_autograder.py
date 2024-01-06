import re
import os.path
import subprocess

import mock

from cs110 import autograder


@mock.patch('requests.get')
def test_connected_to_internet(mock_get):
    autograder.connected_to_internet()
    mock_get.assert_called_once_with(autograder.autograder_ping,
                                     timeout=mock.ANY)


def test_get_user_preference():
    autograder.connected = True
    with mock.patch('builtins.input', return_value='y') as mock_input:
        assert autograder.get_user_preference() is True
        mock_input.assert_called_once_with("Test against server? [y/N]: ")

    autograder.connected = False
    autograder.get_user_preference()
    with mock.patch('builtins.input') as mock_input:
        assert autograder.get_user_preference() is False
        mock_input.assert_not_called()


def test__get_login():
    with mock.patch('getpass.getuser') as mock_getuser, \
         mock.patch('os.getlogin') as mock_getlogin:
        autograder._get_login()
        mock_getuser.assert_called_once_with()
        mock_getlogin.assert_not_called()

    with mock.patch('getpass.getuser', side_effect=OSError) as mock_getuser, \
         mock.patch('os.getlogin') as mock_getlogin:
        autograder._get_login()
        mock_getuser.assert_called_once_with()
        mock_getlogin.assert_called_once_with()


@mock.patch('sys.exit')
@mock.patch('requests.post')
@mock.patch('cs110.autograder.get_user_preference', return_value=True)
@mock.patch('cs110.autograder.connected_to_internet', return_value=True)
def test_main(mock_connected_to_internet, mock_get_user_preference,
              mock_post, mock_exit):
    with open(os.path.join(os.path.dirname(__file__),
                           'examples/helloworld_test.py'), 'r') as f:
        test = f.read()

    mock_response = mock.Mock()
    mock_response.json.return_value = {
      'id': 0,
      'message': test,
      'response_code': 200,
      'timestamp': 0,
    }
    mock_post.return_value = mock_response

    autograder_run_script = autograder.run_script

    def run_script(filename, *args, **kwargs):
        return autograder_run_script(os.path.join(os.path.dirname(__file__),
                                                  'examples', filename),
                                     *args, **kwargs)

    test = test.replace('helloworld.py', 'tests/examples/helloworld.py')

    with mock.patch('builtins.print') as mock_print, \
         mock.patch('cs110.autograder.run_testcases',
                    wraps=autograder.run_testcases) as mock_run_testcases, \
         mock.patch('cs110.autograder.run_script',
                    wraps=run_script) as mock_run_script:
        autograder.main()

    mock_run_testcases.assert_called_once()
    mock_run_script.assert_called_once_with('helloworld.py', mock.ANY)

    mock_print.assert_any_call("Your Program's Output:", end='')
    mock_print.assert_any_call("Hello World\n")
    mock_print.assert_any_call("Feedback:", end='')
    mock_print.assert_any_call("SUCCESS!")

    mock_exit.assert_called_once_with()


def test_main_file_name_vs_path():
    program = 'tests/examples/helloworld.py'
    result = subprocess.run(['python', program], capture_output=True)

    output = result.stdout.decode('utf-8')
    assert 'Your Program' in output, 'Missing file in debugging output'

    match = re.search(r'Your Program: (?P<program>[/\w.]+)', output)
    if match is not None:
        assert program == match.group('program')
    else:
        # parsing file name (or path) failed, fall back by using entire output
        assert f'Your Program: {program}' in output
