import os
import subprocess
import sys

# The SHA-1 hash used by git to indicate ref creation or deletion.
no_rev = '0' * 40

verbose = True

# Get the value of a git config key
# Normally, git config returns non-zero if the key doesn't exist
def get_git_config(key, default=None):
    args = ['git', 'config', key]
    value = run(args, False)
    if len(value) > 0:
        return value[0]
    else:
        return default

# Run a command and return a list of its output lines.
def run(args, exit_on_fail=True):
    # Can't use subprocess.check_output until 2.7 (drugstore has 2.4).
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        if verbose:
            sys.stderr.write('Failed command: ' + ' '.join(args) + '\n')
            if err != '':
                sys.stderr.write('stderr:\n' + err)
        if exit_on_fail:
            sys.stderr.write('Unexpected command failure, exiting\n')
            sys.exit(1)
    return out.splitlines()


# Return the path to a file in the hook directory.
def hookdir_file(name):
    return os.path.join(os.getenv('GIT_DIR'), 'hooks', name)

# Check if the environment is sane for a git hook to run. This means
# checking that GIT_DIR is set and that it exists.
def is_env_sane():
    git_dir = os.getenv('GIT_DIR')
    if git_dir == None:
        return False
    if not os.path.exists(git_dir):
        return False
    # Everything went okay
    return True

if run(['git', 'config', 'hooks.verbose'])[0].lower() == 'false':
    verbose = False
