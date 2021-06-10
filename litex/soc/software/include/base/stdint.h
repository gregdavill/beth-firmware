#ifndef __STDINT_H
#define __STDINT_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef __LP64__
typedef long intptr_t;
typedef unsigned long uintptr_t;
#else
typedef int intptr_t;
typedef unsigned int uintptr_t;
#endif

typedef unsigned long long uint64_t;
typedef unsigned int uint32_t;
typedef unsigned short uint16_t;
typedef unsigned char uint8_t;

typedef long long int64_t;
typedef int int32_t;
typedef short int16_t;
typedef signed char int8_t;

typedef signed char int_least8_t;
typedef unsigned char uint_least8_t;
typedef signed short int_least16_t;
typedef unsigned short uint_least16_t;
typedef signed int int_least32_t;
typedef unsigned int uint_least32_t;
typedef signed long long int_least64_t;
typedef unsigned long long uint_least64_t;

#define INT8_MAX 127
#define INT16_MAX 32767
#define INT32_MAX 2147483647
#define INT64_MAX 9223372036854775807LL

#define INT8_MIN -128
#define INT16_MIN -32768
#define INT32_MIN (-INT32_MAX - 1)
#define INT64_MIN (-INT64_MAX - 1LL)

#define UINT8_MAX 255
#define UINT16_MAX 65535
#define UINT32_MAX 4294967295U
#define UINT64_MAX 18446744073709551615ULL

#define __int_c_join(a, b) a ## b
#define __int_c(v, suffix) __int_c_join(v, suffix)
#define __uint_c(v, suffix) __int_c_join(v##U, suffix)

#define INT64_C(v) __int_c(v, LL)
#define UINT64_C(v) __uint_c(v, LL)
#define INT32_C(v) v
#define UINT32_C(v) v##U

#ifdef __cplusplus
}
#endif

#endif /* __STDINT_H */
