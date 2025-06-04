#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_usage(const char *prog) {
    printf("Usage: %s <command> [args]\n", prog);
    printf("Commands:\n");
    printf("  install <pkg>    Install a package from the repos or AUR\n");
    printf("  remove <pkg>     Remove a package\n");
    printf("  search <query>   Search for packages\n");
    printf("  update           Update package databases\n");
    printf("  fallbacks        List fallback package systems\n");
}

void print_fallbacks() {
    const char *fallbacks[] = {
        "apt", "dnf", "yum", "zypper", "portage",
        "pkg", "homebrew", "chocolatey", "snap", "flatpak",
        "pip", "npm", "cargo"
    };
    int count = sizeof(fallbacks) / sizeof(fallbacks[0]);
    printf("Fallback package systems if AUR/yay fail:\n");
    for (int i = 0; i < count; ++i) {
        printf("  %s\n", fallbacks[i]);
    }
}

int run_cmd(const char *cmd) {
    int ret = system(cmd);
    if (ret != 0) {
        fprintf(stderr, "Command failed: %s\n", cmd);
        print_fallbacks();
    }
    return ret;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    const char *cmd = argv[1];
    if (strcmp(cmd, "install") == 0) {
        if (argc < 3) {
            fprintf(stderr, "install command requires a package name\n");
            return 1;
        }
        char command[256];
        snprintf(command, sizeof(command), "yay -S %s", argv[2]);
        return run_cmd(command);
    } else if (strcmp(cmd, "remove") == 0) {
        if (argc < 3) {
            fprintf(stderr, "remove command requires a package name\n");
            return 1;
        }
        char command[256];
        snprintf(command, sizeof(command), "sudo pacman -R %s", argv[2]);
        return run_cmd(command);
    } else if (strcmp(cmd, "search") == 0) {
        if (argc < 3) {
            fprintf(stderr, "search command requires a query\n");
            return 1;
        }
        char command[256];
        snprintf(command, sizeof(command), "yay -Ss %s", argv[2]);
        return run_cmd(command);
    } else if (strcmp(cmd, "update") == 0) {
        return run_cmd("sudo pacman -Syu");
    } else if (strcmp(cmd, "fallbacks") == 0) {
        print_fallbacks();
        return 0;
    } else {
        fprintf(stderr, "Unknown command: %s\n", cmd);
        print_usage(argv[0]);
    }

    return 0;
}
