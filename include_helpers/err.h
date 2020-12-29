//
// Created by mfran on 29/12/2020.
//

#ifndef PDC_MINI_AEVOL_ERR_H
#define PDC_MINI_AEVOL_ERR_H

#if _WIN32

// Placeholder is very basic: printf the message to stderr and exit with given status.

#include <cstdarg>
#include <cstdio>
#include <cstdlib>

inline void err(int l_status, const char* format, ...) {
    std::va_list list_args;
    va_start(list_args, format);
    std::vfprintf(stderr, format, list_args);
    std::exit(l_status);
}

#else
#   include <err.h>
#endif

#endif //PDC_MINI_AEVOL_ERR_H
