//
// Created by elturpin on 03/12/2020.
//

#include "include_helpers/err.h"
#include "include_helpers/sys/stat.h"
#include "Abstract_ExpManager.h"

/**
 * Create stats and backup directory
 */
void Abstract_ExpManager::create_directory() {
    // Backup
    int status = mkdir("backup", 0755);
    if (status == -1 && errno != EEXIST) {
        err(EXIT_FAILURE, "backup");
    }

    // Stats
    status = mkdir("stats", 0755);
    if (status == -1 && errno != EEXIST) {
        err(EXIT_FAILURE, "stats");
    }
}