#include <stdio.h>
#include "hash.h"

int sha256(void *bytes, size_t size, char out[64]) {
    unsigned char digest[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    if (! SHA256_Init(&sha256))
        return 0;

    if (! SHA256_Update(&sha256, bytes, size))
        return 0;

    if (! SHA256_Final(digest, &sha256))
        return 0;

    int i;
    for (i = 0; i < SHA256_DIGEST_LENGTH; ++i)
        sprintf(out + (i * 2), "%02x", digest[i]);

    return 1;
}
