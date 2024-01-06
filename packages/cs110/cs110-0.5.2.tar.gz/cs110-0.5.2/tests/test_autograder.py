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


def test__is_valid_email():
    for localpart in ['first.last', 'c24first.last', 'C24first.last',
                      'first.last1', 'c24first.last1', 'C24first.last1',
                      'first.last.country']:
        email = f"{localpart}@afacademy.af.edu"
        assert autograder._is_valid_email(email), \
            f'Rejected valid email address: {email}'

    for email in ['first.last', 'first.last@usafa.edu', '@usafa.edu',
                  'username <email@afacademy.af.edu>',
                  'first.last@afacademy.af.edu ']:
        assert not autograder._is_valid_email(email), \
            f'Accepted invalid email address: {email}'


def test__prompt_for_email():
    valid = 'first.last@afacademy.af.edu'
    with mock.patch('builtins.input', return_value=valid) as mock_input:
        assert autograder._prompt_for_email() == valid
        mock_input.assert_has_calls([
            mock.call("\nThis is your first time running autograder! "
                      "Enter your school email:\n"),
        ])

    with mock.patch('builtins.input',  # side_effect for multiple return values
                    side_effect=['invalid', 'invalid', valid]) as mock_input:
        assert autograder._prompt_for_email() == valid
        mock_input.assert_has_calls([
            mock.call("\nThis is your first time running autograder! "
                      "Enter your school email:\n"),
            mock.call("Improper format. Please re-enter your email: "),
            mock.call("Improper format. Please re-enter your email: "),
        ])


def test__get_login(tmpdir):
    email = 'first.last@afacademy.af.edu'
    with mock.patch('cs110.autograder._prompt_for_email',
                    return_value=email) as mock_prompt_for_email, \
         mock.patch('xdg.xdg_config_home',
                    return_value=tmpdir) as mock_xdg_config_home:
        assert autograder._get_login() == email

        mock_xdg_config_home.assert_called_once_with()
        mock_prompt_for_email.assert_called_once_with()

        assert os.path.exists(os.path.join(tmpdir, 'cs110.ini'))

    with mock.patch('cs110.autograder._prompt_for_email',
                    return_value=email) as mock_prompt_for_email, \
         mock.patch('xdg.xdg_config_home',
                    return_value=tmpdir) as mock_xdg_config_home:
        assert autograder._get_login() == email

        mock_xdg_config_home.assert_called_once_with()
        mock_prompt_for_email.assert_not_called()


def test__get_login_with_missing_directories(tmpdir):
    directories = os.path.join(tmpdir, 'a', 'b', 'c', 'missing')
    test__get_login(directories)


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
         mock.patch('cs110.autograder._get_login',
                    return_value='fake-email') as mock_get_login, \
         mock.patch('cs110.autograder.run_testcases',
                    wraps=autograder.run_testcases) as mock_run_testcases, \
         mock.patch('cs110.autograder.run_script',
                    wraps=run_script) as mock_run_script:
        autograder.main()

    mock_get_login.assert_called()
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
