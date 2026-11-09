/* Haro's own declaration of the one CommonCrypto call mimalloc makes on macOS (its random source, prim/unix/prim.c), for a build
   cross-compiled without Apple's SDK: Zig's macOS headers carry no CommonCrypto, and its libSystem stub exports the symbol, which
   libSystem re-exports from libcommonCrypto. Included only when the target is macOS (build.zig). */
#ifndef HARO_COMPAT_COMMONRANDOM_H
#define HARO_COMPAT_COMMONRANDOM_H
#include <stddef.h>
#include "CommonCryptoError.h"
typedef CCCryptorStatus CCRNGStatus;
CCRNGStatus CCRandomGenerateBytes(void *bytes, size_t count);
#endif
