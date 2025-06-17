import sys
import os
import shlex


def eval_token(token, env):
    """Return integer or string value for a token."""
    if token in env:
        return env[token]
    try:
        return int(token)
    except ValueError:
        return token


def run_line(tokens, env):
    if not tokens:
        return
    cmd = tokens[0]
    if cmd == 'set' and len(tokens) >= 3:
        env[tokens[1]] = eval_token(tokens[2], env)
    elif cmd == 'add' and len(tokens) >= 4:
        a = eval_token(tokens[1], env)
        b = eval_token(tokens[2], env)
        env[tokens[3]] = a + b
    elif cmd == 'sub' and len(tokens) >= 4:
        a = eval_token(tokens[1], env)
        b = eval_token(tokens[2], env)
        env[tokens[3]] = a - b
    elif cmd == 'print' and len(tokens) >= 2:
        parts = [str(eval_token(t, env)) for t in tokens[1:]]
        print(' '.join(parts))
    else:
        raise ValueError(f"Unknown command: {' '.join(tokens)}")


def run_systx(path, args):
    env = {'args': args}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens = shlex.split(line)
            run_line(tokens, env)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(f"Usage: {sys.argv[0]} <script.systx> [args]")
        return
    script = sys.argv[1]
    if not os.path.exists(script):
        print(f"Error: script {script} not found")
        return
    run_systx(script, sys.argv[2:])


if __name__ == '__main__':
    main()
