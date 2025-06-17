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


def compare(a, op, b):
    """Evaluate a comparison operation."""
    if op == '==':
        return a == b
    if op == '!=':
        return a != b
    if op == '>':
        return a > b
    if op == '<':
        return a < b
    if op == '>=':
        return a >= b
    if op == '<=':
        return a <= b
    raise ValueError(f'Unknown operator: {op}')


def run_line(tokens, env, labels, funcs, stack, pc_after):
    """Execute a single command. Return new PC or None."""
    if not tokens:
        return None
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
    elif cmd == 'mul' and len(tokens) >= 4:
        a = eval_token(tokens[1], env)
        b = eval_token(tokens[2], env)
        env[tokens[3]] = a * b
    elif cmd == 'div' and len(tokens) >= 4:
        a = eval_token(tokens[1], env)
        b = eval_token(tokens[2], env)
        env[tokens[3]] = a // b
    elif cmd == 'mod' and len(tokens) >= 4:
        a = eval_token(tokens[1], env)
        b = eval_token(tokens[2], env)
        env[tokens[3]] = a % b
    elif cmd == 'read' and len(tokens) == 2:
        env[tokens[1]] = input()
    elif cmd == 'print' and len(tokens) >= 2:
        parts = [str(eval_token(t, env)) for t in tokens[1:]]
        print(' '.join(parts))
    elif cmd == 'goto' and len(tokens) == 2:
        label = tokens[1]
        if label not in labels:
            raise ValueError(f'Unknown label: {label}')
        return labels[label]
    elif cmd == 'if' and len(tokens) >= 6 and tokens[4] == 'goto':
        a = eval_token(tokens[1], env)
        op = tokens[2]
        b = eval_token(tokens[3], env)
        label = tokens[5]
        if compare(a, op, b):
            if label not in labels:
                raise ValueError(f'Unknown label: {label}')
            return labels[label]
    elif cmd == 'call' and len(tokens) == 2:
        name = tokens[1]
        if name not in funcs:
            raise ValueError(f'Unknown function: {name}')
        stack.append(pc_after)
        return funcs[name]
    elif cmd == 'return':
        if not stack:
            return None
        return stack.pop()
    elif cmd == 'exit':
        return float('inf')
    else:
        raise ValueError(f"Unknown command: {' '.join(tokens)}")
    return None


def run_systx(path, args):
    env = {'args': args}
    with open(path) as f:
        raw_lines = [line.rstrip() for line in f]
    labels = {}
    funcs = {}
    lines = []
    for raw in raw_lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            lines.append(None)
            continue
        if line.startswith(':'):
            labels[line[1:].strip()] = len(lines)
            lines.append(None)
            continue
        if line.startswith('func '):
            name = line.split(None, 1)[1].strip()
            funcs[name] = len(lines)
            lines.append(None)
            continue
        if line == 'end':
            lines.append(['return'])
            continue
        lines.append(shlex.split(line))

    stack = []
    pc = 0
    while pc < len(lines):
        tokens = lines[pc]
        pc += 1
        if tokens is None:
            continue
        new_pc = run_line(tokens, env, labels, funcs, stack, pc)
        if new_pc is not None:
            if new_pc == float('inf'):
                break
            pc = int(new_pc)


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
