import sys
import os
import shlex
import time
import random


def eval_token(token, env_stack):
    """Return integer or string value for a token using stacked scopes."""
    for scope in reversed(env_stack):
        if token in scope:
            return scope[token]
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


def run_line(tokens, env_stack, labels, funcs, call_stack, data_stack, pc_after, loops_end):
    """Execute a single command. Return new PC or None."""
    if not tokens:
        return None
    env = env_stack[-1]
    cmd = tokens[0]
    if cmd == 'set' and len(tokens) >= 3:
        env[tokens[1]] = eval_token(tokens[2], env_stack)
    elif cmd == 'setg' and len(tokens) >= 3:
        env_stack[0][tokens[1]] = eval_token(tokens[2], env_stack)
    elif cmd == 'add' and len(tokens) >= 4:
        a = eval_token(tokens[1], env_stack)
        b = eval_token(tokens[2], env_stack)
        env[tokens[3]] = a + b
    elif cmd == 'sub' and len(tokens) >= 4:
        a = eval_token(tokens[1], env_stack)
        b = eval_token(tokens[2], env_stack)
        env[tokens[3]] = a - b
    elif cmd == 'mul' and len(tokens) >= 4:
        a = eval_token(tokens[1], env_stack)
        b = eval_token(tokens[2], env_stack)
        env[tokens[3]] = a * b
    elif cmd == 'div' and len(tokens) >= 4:
        a = eval_token(tokens[1], env_stack)
        b = eval_token(tokens[2], env_stack)
        env[tokens[3]] = a // b
    elif cmd == 'mod' and len(tokens) >= 4:
        a = eval_token(tokens[1], env_stack)
        b = eval_token(tokens[2], env_stack)
        env[tokens[3]] = a % b
    elif cmd == 'abs' and len(tokens) == 3:
        val = eval_token(tokens[1], env_stack)
        env[tokens[2]] = abs(int(val))
    elif cmd == 'pow' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env_stack))
        b = int(eval_token(tokens[2], env_stack))
        env[tokens[3]] = a ** b
    elif cmd == 'min' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env_stack))
        b = int(eval_token(tokens[2], env_stack))
        env[tokens[3]] = a if a < b else b
    elif cmd == 'max' and len(tokens) >= 4:
        a = int(eval_token(tokens[1], env_stack))
        b = int(eval_token(tokens[2], env_stack))
        env[tokens[3]] = a if a > b else b
    elif cmd == 'upper' and len(tokens) == 3:
        env[tokens[2]] = str(eval_token(tokens[1], env_stack)).upper()
    elif cmd == 'lower' and len(tokens) == 3:
        env[tokens[2]] = str(eval_token(tokens[1], env_stack)).lower()
    elif cmd == 'slice' and len(tokens) == 5:
        s = str(eval_token(tokens[1], env_stack))
        start = int(eval_token(tokens[2], env_stack))
        end = int(eval_token(tokens[3], env_stack))
        env[tokens[4]] = s[start:end]
    elif cmd == 'split' and len(tokens) == 4:
        s = str(eval_token(tokens[1], env_stack))
        sep = str(eval_token(tokens[2], env_stack))
        env[tokens[3]] = s.split(sep)
    elif cmd == 'join' and len(tokens) == 4:
        lst = eval_token(tokens[1], env_stack)
        sep = str(eval_token(tokens[2], env_stack))
        env[tokens[3]] = sep.join(str(x) for x in lst)
    elif cmd == 'append' and len(tokens) == 3:
        lst = env.setdefault(tokens[1], [])
        lst.append(eval_token(tokens[2], env_stack))
    elif cmd == 'get' and len(tokens) == 4:
        lst = eval_token(tokens[1], env_stack)
        idx = int(eval_token(tokens[2], env_stack))
        env[tokens[3]] = lst[idx]
    elif cmd == 'lenlist' and len(tokens) == 3:
        lst = eval_token(tokens[1], env_stack)
        env[tokens[2]] = len(lst)
    elif cmd == 'inc' and len(tokens) == 2:
        var = tokens[1]
        env[var] = env.get(var, 0) + 1
    elif cmd == 'dec' and len(tokens) == 2:
        var = tokens[1]
        env[var] = env.get(var, 0) - 1
    elif cmd == 'and' and len(tokens) >= 4:
        a = bool(eval_token(tokens[1], env_stack))
        b = bool(eval_token(tokens[2], env_stack))
        env[tokens[3]] = int(a and b)
    elif cmd == 'or' and len(tokens) >= 4:
        a = bool(eval_token(tokens[1], env_stack))
        b = bool(eval_token(tokens[2], env_stack))
        env[tokens[3]] = int(a or b)
    elif cmd == 'not' and len(tokens) >= 3:
        a = bool(eval_token(tokens[1], env_stack))
        env[tokens[2]] = int(not a)
    elif cmd == 'concat' and len(tokens) >= 4:
        a = str(eval_token(tokens[1], env_stack))
        b = str(eval_token(tokens[2], env_stack))
        env[tokens[3]] = a + b
    elif cmd == 'len' and len(tokens) == 3:
        a = str(eval_token(tokens[1], env_stack))
        env[tokens[2]] = len(a)
    elif cmd == 'rand' and len(tokens) == 3:
        max_val = int(eval_token(tokens[1], env_stack))
        env[tokens[2]] = random.randint(0, max_val - 1 if max_val > 0 else 0)
    elif cmd == 'sleep' and len(tokens) == 2:
        secs = float(eval_token(tokens[1], env_stack))
        time.sleep(secs)
    elif cmd == 'copy' and len(tokens) == 3:
        env[tokens[2]] = eval_token(tokens[1], env_stack)
    elif cmd == 'arg' and len(tokens) == 3:
        idx = int(eval_token(tokens[1], env_stack))
        args = env_stack[0].get('args', [])
        env[tokens[2]] = args[idx] if idx < len(args) else ''
    elif cmd == 'argc' and len(tokens) == 2:
        args = env_stack[0].get('args', [])
        env[tokens[1]] = len(args)
    elif cmd == 'push' and len(tokens) == 2:
        data_stack.append(eval_token(tokens[1], env_stack))
    elif cmd == 'pop' and len(tokens) == 2:
        if not data_stack:
            raise ValueError('Stack empty')
        env[tokens[1]] = data_stack.pop()
    elif cmd == 'swap' and len(tokens) == 3:
        a = tokens[1]
        b = tokens[2]
        env[a], env[b] = env.get(b), env.get(a)
    elif cmd == 'open' and len(tokens) == 4:
        path = str(eval_token(tokens[1], env_stack))
        mode = str(eval_token(tokens[2], env_stack))
        env[tokens[3]] = open(path, mode)
    elif cmd == 'readfile' and len(tokens) == 3:
        path = str(eval_token(tokens[1], env_stack))
        with open(path, 'r', encoding='utf-8') as fh:
            env[tokens[2]] = fh.read()
    elif cmd == 'writefile' and len(tokens) == 3:
        path = str(eval_token(tokens[1], env_stack))
        data = str(eval_token(tokens[2], env_stack))
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(data)
    elif cmd == 'appendfile' and len(tokens) == 3:
        path = str(eval_token(tokens[1], env_stack))
        data = str(eval_token(tokens[2], env_stack))
        with open(path, 'a', encoding='utf-8') as fh:
            fh.write(data)
    elif cmd == 'readline' and len(tokens) == 3:
        fh = eval_token(tokens[1], env_stack)
        env[tokens[2]] = fh.readline().rstrip('\n')
    elif cmd == 'write' and len(tokens) == 3:
        fh = eval_token(tokens[1], env_stack)
        fh.write(str(eval_token(tokens[2], env_stack)))
    elif cmd == 'close' and len(tokens) == 2:
        fh = eval_token(tokens[1], env_stack)
        fh.close()
    elif cmd == 'read' and len(tokens) == 2:
        env[tokens[1]] = input()
    elif cmd == 'exists' and len(tokens) == 3:
        path = str(eval_token(tokens[1], env_stack))
        env[tokens[2]] = int(os.path.exists(path))
    elif cmd == 'chdir' and len(tokens) == 2:
        path = str(eval_token(tokens[1], env_stack))
        os.chdir(path)
    elif cmd == 'listdir' and len(tokens) == 3:
        path = str(eval_token(tokens[1], env_stack))
        env[tokens[2]] = os.listdir(path) if os.path.exists(path) else []
    elif cmd == 'envget' and len(tokens) == 3:
        name = str(eval_token(tokens[1], env_stack))
        env[tokens[2]] = os.environ.get(name, '')
    elif cmd == 'system' and len(tokens) >= 2:
        cmdline = ' '.join(str(eval_token(t, env_stack)) for t in tokens[1:])
        os.system(cmdline)
    elif cmd == 'joinpath' and len(tokens) == 4:
        a = str(eval_token(tokens[1], env_stack))
        b = str(eval_token(tokens[2], env_stack))
        env[tokens[3]] = os.path.join(a, b)
    elif cmd == 'print' and len(tokens) >= 2:
        parts = [str(eval_token(t, env_stack)) for t in tokens[1:]]
        print(' '.join(parts))
    elif cmd == 'goto' and len(tokens) == 2:
        label = tokens[1]
        if label not in labels:
            raise ValueError(f'Unknown label: {label}')
        return labels[label]
    elif cmd == 'while':
        cond = tokens[1:]
        idx = pc_after - 1
        if len(cond) == 3:
            a = eval_token(cond[0], env_stack)
            op = cond[1]
            b = eval_token(cond[2], env_stack)
            ok = compare(a, op, b)
        elif len(cond) == 1:
            ok = bool(eval_token(cond[0], env_stack))
        else:
            raise ValueError('Invalid while syntax')
        if not ok:
            return loops_end[idx] + 1
    elif cmd == 'endwhile':
        start = int(tokens[1])
        return start
    elif cmd == 'if' and len(tokens) >= 6 and tokens[4] == 'goto':
        a = eval_token(tokens[1], env_stack)
        op = tokens[2]
        b = eval_token(tokens[3], env_stack)
        label = tokens[5]
        if compare(a, op, b):
            if label not in labels:
                raise ValueError(f'Unknown label: {label}')
            return labels[label]
    elif cmd == 'call' and len(tokens) >= 2:
        name = tokens[1]
        if name not in funcs:
            raise ValueError(f'Unknown function: {name}')
        start, params = funcs[name]
        if len(tokens) - 2 != len(params):
            raise ValueError('Argument count mismatch')
        new_env = {}
        for param, arg in zip(params, tokens[2:]):
            new_env[param] = eval_token(arg, env_stack)
        call_stack.append(pc_after)
        env_stack.append(new_env)
        return start
    elif cmd == 'return':
        if not call_stack:
            return None
        env_stack.pop()
        return call_stack.pop()
    elif cmd == 'exit':
        return float('inf')
    else:
        raise ValueError(f"Unknown command: {' '.join(tokens)}")
    return None


def run_systx(path, args):
    env_stack = [{'args': args}]
    with open(path, encoding='utf-8') as f:
        raw_lines = [line.rstrip() for line in f]
    labels = {}
    funcs = {}
    loops_end = {}
    lines = []
    loop_stack = []
    for raw in raw_lines:
        line = raw.rstrip()
        if ';#' in line:
            line = line.split(';#', 1)[0]
        if '#' in line:
            line = line.split('#', 1)[0]
        line = line.strip()
        if line.endswith(';'):
            line = line[:-1].rstrip()
        if not line:
            lines.append(None)
            continue
        if line.startswith(':'):
            labels[line[1:].strip()] = len(lines)
            lines.append(None)
            continue
        if line.startswith('func '):
            parts = shlex.split(line)
            name = parts[1]
            params = parts[2:]
            funcs[name] = (len(lines), params)
            lines.append(None)
            continue
        if line.startswith('while '):
            loop_stack.append(len(lines))
            lines.append(shlex.split(line))
            continue
        if line == 'endwhile':
            if not loop_stack:
                raise ValueError('endwhile without while')
            start = loop_stack.pop()
            lines.append(['endwhile', str(start)])
            loops_end[start] = len(lines)-1
            continue
        if line == 'end':
            lines.append(['return'])
            continue
        lines.append(shlex.split(line))

    if loop_stack:
        raise ValueError('Unclosed while loop')

    call_stack = []
    data_stack = []
    pc = 0
    while pc < len(lines):
        tokens = lines[pc]
        pc += 1
        if tokens is None:
            continue
        new_pc = run_line(tokens, env_stack, labels, funcs, call_stack, data_stack, pc, loops_end)
        if new_pc is not None:
            if new_pc == float('inf'):
                break
            pc = int(new_pc)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(f"Usage: {sys.argv[0]} <script.stx> [args]")
        return
    script = sys.argv[1]
    if not os.path.exists(script):
        print(f"Error: script {script} not found")
        return
    run_systx(script, sys.argv[2:])


if __name__ == '__main__':
    main()
