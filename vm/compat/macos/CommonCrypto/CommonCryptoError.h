/* Haro's own declaration of CommonCrypto's status type and its success value, as CommonRandom.h here needs them (see there). */
#ifndef HARO_COMPAT_COMMONCRYPTOERROR_H
#define HARO_COMPAT_COMMONCRYPTOERROR_H
#include <stdint.h>
typedef int32_t CCCryptorStatus;
enum { kCCSuccess = 0 };
#endif
