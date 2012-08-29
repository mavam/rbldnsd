#ifndef HASH_H
#define HASH_H

/// Computes the SHA256 hash for a given contiguous chunk of bytes.
///
/// @param bytes A pointer to the beginning of the contiguous byte sequence to
/// hash.
///
/// @param size The number of bytes to process beginning at *bytes*.
///
/// @param out The 64 byte character representation of the digest.
///
/// @return 1 on success and 0 on failure.
int sha256(void *bytes, size_t size, char out[64]);

#endif /* include guard */
