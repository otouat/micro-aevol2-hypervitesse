//
// Created by mfran on 29/12/2020.
//

#ifndef PDC_MINI_AEVOL_STAT_H
#define PDC_MINI_AEVOL_STAT_H

#if _WIN32

#   include <direct.h>
inline int mkdir(const char* path, ...) {
    return _mkdir(path);
}

#else
#   include <sys/stat.h>
#endif

#endif //PDC_MINI_AEVOL_STAT_H
