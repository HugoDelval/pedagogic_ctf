#!/usr/bin/python3
import sys, os, subprocess
import re
import shutil
import pwd
import random, string
import importlib.machinery

SUPPORTED_EXTENSIONS = ['.py', '.go', '.pl', '.php', '.java']


def run_cmd(cmd_list):
    child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    ret = child.returncode
    return streamdata.decode(), ret


def random_string(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def get_unique_user(chall_name, nb=0):
    if nb > 10:
        raise OSError("Can't find a free username..")
    user = chall_name[-9:] + "_" + random_string(21)
    try:
        pwd.getpwnam(user)
        return get_unique_user(chall_name, nb + 1)
    except:
        return user


def check_args(corrected_script_dir, challenge_name, language_extension):
    regex_challenge_name = r"^[\w-]{4,30}$"
    regex_challenge_name_compiled = re.compile(regex_challenge_name)
    if not regex_challenge_name_compiled.match(challenge_name):
        print("Challenge name param not valid.")
        sys.exit(1)
    regex_corrected_script_dir = r"^/srv/writable/" + challenge_name + r"_[a-zA-Z0-9]{30}/?$"
    regex_corrected_script_dir_compiled = re.compile(regex_corrected_script_dir)
    if not regex_corrected_script_dir_compiled.match(corrected_script_dir):
        print("Path param not valid : " + corrected_script_dir)
        sys.exit(1)
    if not os.path.isdir(corrected_script_dir):
        print("Directory does not exists : " + corrected_script_dir)
        sys.exit(1)
    corrected_script_path = os.path.join(corrected_script_dir, challenge_name + language_extension)
    if not os.path.exists(corrected_script_path):
        print("File does not exists : " + corrected_script_path)
        sys.exit(1)
    if language_extension not in SUPPORTED_EXTENSIONS:
        print("Extension not supported : " + language_extension)
        sys.exit(1)
    challenge_path = os.path.join(os.path.sep, 'srv', 'ctf_go', 'challs', challenge_name + '.dir')
    if not os.path.isdir(challenge_path):
        print("Directory does not exists : " + challenge_path)
        sys.exit(1)


def launch_init_challenge(language_extension, challenge_name, corrected_script_dir):
    # launch init script challenge (for custom init)
    init = importlib.machinery.SourceFileLoader('init', os.path.join(corrected_script_dir, "init.py")).load_module()
    randomized = random_string(30)
    init.init(corrected_script_dir, randomized, challenge_name + language_extension)

    # create unique user
    unique_user = get_unique_user(challenge_name)
    streamdata, return_code = run_cmd(['useradd', unique_user])
    if return_code != 0:
        print("An error occured while adding user '" + unique_user + "' : " + str(streamdata))
        sys.exit(1)

    # compile challenge
    script_path = os.path.join(corrected_script_dir, challenge_name + language_extension)
    script_path_compiled = os.path.join(corrected_script_dir, challenge_name)
    if language_extension == ".pl":
        # we just need to create a symbolic link
        os.symlink(script_path, script_path_compiled)
    elif language_extension == ".py":
        # we just need to create a symbolic link
        os.symlink(script_path, script_path_compiled)
    elif language_extension == ".go":
        streamdata, return_code = run_cmd(["/usr/bin/go", "build", "-o", script_path_compiled, script_path])
        if return_code != 0:
            print("An error occured while building go file : " + str(streamdata))
            sys.exit(1)
    # change wrapper
    wrapper_path = os.path.join(corrected_script_dir, 'wrapper.c')
    with open(wrapper_path) as wrapper_handler:
        wrapper = wrapper_handler.read()
    wrapper = wrapper.replace('CHALLENGE', script_path_compiled)
    wrapper = wrapper.replace('THE_USER', unique_user)
    with open(wrapper_path, "w") as wrapper_handler:
        wrapper_handler.write(wrapper)
    # compile wrapper
    wrapper_bin_path = os.path.join(corrected_script_dir, 'wrapper')
    streamdata, return_code = run_cmd(['/usr/bin/gcc', "-o", wrapper_bin_path, wrapper_path])
    if return_code != 0:
        print("An error occured while compiling wrapper : " + str(streamdata))
        sys.exit(1)

    # chown / chmod
    streamdata, return_code = run_cmd(['/bin/chown', unique_user + ":" + unique_user, corrected_script_dir, '-R'])
    if return_code != 0:
        print("An error occured while chowning : " + str(streamdata))
        sys.exit(1)
    streamdata, return_code = run_cmd(['/bin/chown', "root:" + unique_user, wrapper_bin_path])
    if return_code != 0:
        print("An error occured while chowning : " + str(streamdata))
        sys.exit(1)
    streamdata, return_code = run_cmd(['/bin/chmod', "500", script_path_compiled])
    if return_code != 0:
        print("An error occured while chmoding : " + str(streamdata))
        sys.exit(1)
    streamdata, return_code = run_cmd(['/bin/chmod', "4750", wrapper_bin_path])
    if return_code != 0:
        print("An error occured while chmoding : " + str(streamdata))
        sys.exit(1)

    return unique_user, randomized


def launch_exploit_challenge(corrected_script_dir, randomized):
    binary = os.path.join(corrected_script_dir, "wrapper")
    exploit = importlib.machinery.SourceFileLoader('exploit',
                                                   os.path.join(corrected_script_dir, "exploit.py")).load_module()
    return exploit.exploit(binary, randomized)


def launch_check_challenge_valid(corrected_script_dir, randomized):
    binary = os.path.join(corrected_script_dir, "wrapper")
    check = importlib.machinery.SourceFileLoader('check', os.path.join(corrected_script_dir, "check.py")).load_module()
    return check.check(binary, randomized)


def cp_files(corrected_script_dir, challenge_name, language_extension):
    base_challs_path = os.path.join(os.path.sep, 'srv', 'ctf_go', 'challs')
    challenge_path = os.path.join(base_challs_path, challenge_name + '.dir')
    try:
        shutil.copy(os.path.join(challenge_path, "init.py"), corrected_script_dir)
        shutil.copy(os.path.join(challenge_path, "exploit.py"), corrected_script_dir)
        shutil.copy(os.path.join(challenge_path, "check.py"), corrected_script_dir)
        shutil.copy(os.path.join(base_challs_path, "wrapper.c"), corrected_script_dir)
    except:
        print('Copy failed, please contact an admin.')
        sys.exit(1)


def delete_everything(user, corrected_script_dir):
    shutil.rmtree(corrected_script_dir)
    streamdata, return_code = run_cmd(['userdel', user])
    if return_code != 0:
        print("An error occured while removing user '" + user + "' : " + str(streamdata))
        sys.exit(1)


if __name__ == "__main__":
    corrected_script_dir = sys.argv[1]
    challenge_name = sys.argv[2]
    language_extension = sys.argv[3]
    check_args(corrected_script_dir, challenge_name, language_extension)
    cp_files(corrected_script_dir, challenge_name, language_extension)
    user, randomized = launch_init_challenge(language_extension, challenge_name, corrected_script_dir)
    os.chdir(corrected_script_dir)
    try:
        can_exploit = launch_exploit_challenge(corrected_script_dir, randomized)
        can_use = launch_check_challenge_valid(corrected_script_dir, randomized)
    except Exception as e:
        can_exploit = True
        can_use = False
        print(e)
    delete_everything(user, corrected_script_dir)
    if can_exploit:
        print("I can still exploit your code ;). If you need hints, don't hesitate to ask !")
        sys.exit(1)
    if not can_use:
        print(
            "I can't use your code :/\nYou broke a functionnality in the code ! So your fix is not accepted.\nIf you "
            "needs hint don't hesitate to ask !")
        sys.exit(1)
