import sys
import os
import shlex
import time
import random


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


def run_line(tokens, env, labels, funcs, call_stack, data_stack, pc_after):
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
    elif cmd == 'abs' and len(tokens) == 3:
        val = eval_token(tokens[1], env)
        env[tokens[2]] = abs(int(val))
    elif cmd == 'pow' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env))
        b = int(eval_token(tokens[2], env))
        env[tokens[3]] = a ** b
    elif cmd == 'min' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env))
        b = int(eval_token(tokens[2], env))
        env[tokens[3]] = a if a < b else b
    elif cmd == 'max' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env))
        b = int(eval_token(tokens[2], env))
        env[tokens[3]] = a if a > b else b
    elif cmd == 'upper' and len(tokens) == 3:
        env[tokens[2]] = str(eval_token(tokens[1], env)).upper()
    elif cmd == 'lower' and len(tokens) == 3:
        env[tokens[2]] = str(eval_token(tokens[1], env)).lower()
    elif cmd == 'slice' and len(tokens) == 5:
        s = str(eval_token(tokens[1], env))
        start = int(eval_token(tokens[2], env))
        end = int(eval_token(tokens[3], env))
        env[tokens[4]] = s[start:end]
    elif cmd == 'split' and len(tokens) == 4:
        s = str(eval_token(tokens[1], env))
        sep = str(eval_token(tokens[2], env))
        env[tokens[3]] = s.split(sep)
    elif cmd == 'join' and len(tokens) == 4:
        lst = eval_token(tokens[1], env)
        sep = str(eval_token(tokens[2], env))
        env[tokens[3]] = sep.join(str(x) for x in lst)
    elif cmd == 'append' and len(tokens) == 3:
        lst = env.setdefault(tokens[1], [])
        lst.append(eval_token(tokens[2], env))
    elif cmd == 'get' and len(tokens) == 4:
        lst = eval_token(tokens[1], env)
        idx = int(eval_token(tokens[2], env))
        env[tokens[3]] = lst[idx]
    elif cmd == 'lenlist' and len(tokens) == 3:
        lst = eval_token(tokens[1], env)
        env[tokens[2]] = len(lst)
    elif cmd == 'inc' and len(tokens) == 2:
        var = tokens[1]
        env[var] = env.get(var, 0) + 1
    elif cmd == 'dec' and len(tokens) == 2:
        var = tokens[1]
        env[var] = env.get(var, 0) - 1
    elif cmd == 'and' and len(tokens) >= 4:
        a = bool(eval_token(tokens[1], env))
        b = bool(eval_token(tokens[2], env))
        env[tokens[3]] = int(a and b)
    elif cmd == 'or' and len(tokens) >= 4:
        a = bool(eval_token(tokens[1], env))
        b = bool(eval_token(tokens[2], env))
        env[tokens[3]] = int(a or b)
    elif cmd == 'not' and len(tokens) >= 3:
        a = bool(eval_token(tokens[1], env))
        env[tokens[2]] = int(not a)
    elif cmd == 'concat' and len(tokens) >= 4:
        a = str(eval_token(tokens[1], env))
        b = str(eval_token(tokens[2], env))
        env[tokens[3]] = a + b
    elif cmd == 'len' and len(tokens) == 3:
        a = str(eval_token(tokens[1], env))
        env[tokens[2]] = len(a)
    elif cmd == 'rand' and len(tokens) == 3:
        max_val = int(eval_token(tokens[1], env))
        env[tokens[2]] = random.randint(0, max_val - 1 if max_val > 0 else 0)
    elif cmd == 'sleep' and len(tokens) == 2:
        secs = float(eval_token(tokens[1], env))
        time.sleep(secs)
    elif cmd == 'copy' and len(tokens) == 3:
        env[tokens[2]] = eval_token(tokens[1], env)
    elif cmd == 'push' and len(tokens) == 2:
        data_stack.append(eval_token(tokens[1], env))
    elif cmd == 'pop' and len(tokens) == 2:
        if not data_stack:
            raise ValueError('Stack empty')
        env[tokens[1]] = data_stack.pop()
    elif cmd == 'swap' and len(tokens) == 3:
        a = tokens[1]
        b = tokens[2]
        env[a], env[b] = env.get(b), env.get(a)
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
        call_stack.append(pc_after)
        return funcs[name]
    elif cmd == 'return':
        if not call_stack:
            return None
        return call_stack.pop()
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

    call_stack = []
    data_stack = []
    pc = 0
    while pc < len(lines):
        tokens = lines[pc]
        pc += 1
        if tokens is None:
            continue
        new_pc = run_line(tokens, env, labels, funcs, call_stack, data_stack, pc)
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
