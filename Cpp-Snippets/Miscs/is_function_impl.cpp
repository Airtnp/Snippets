// ref: https://twitter.com/ericniebler/status/852192542653329408
#include <type_traits>

template <int I> struct priority_tag : priority_tag<I - 1> {};
template <> struct priority_tag<0> {};

namespace detail {
// Function types:
template<typename T>
constexpr bool is_function_impl_(priority_tag<0>) { return true; }

// Array types:
template<typename T, typename = decltype(std::declval<T&>()[0])>
constexpr bool is_function_impl_(priority_tag<1>) { return false; }

// Anything that can be returned from a function (including
// void, reference, and scalar types):
template<typename T, typename = T(*)()>
constexpr bool is_function_impl_(priority_tag<2>) { return false; }

// Classes (notably abstract class types that would not be caught by the above):
template<typename T, typename = int T::*>
constexpr bool is_function_impl_(priority_tag<3>) { return false; }
} // namespace detail

template <typename T>
constexpr bool is_function_v = detail::is_function_impl_<T>(priority_tag<3>{});

template <typename T>
struct is_function : std::bool_constant<is_function_v<T>>
{};

//===----------------------------------------------------------------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is dual licensed under the MIT and the University of Illinois Open
// Source Licenses. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

// type_traits

// is_function

#include <type_traits>
#include <cstddef>        // for std::nullptr_t

template <class T>
void test_is_function()
{
    static_assert( ::is_function<T>::value, "");
    static_assert( ::is_function<const T>::value, "");
    static_assert( ::is_function<volatile T>::value, "");
    static_assert( ::is_function<const volatile T>::value, "");
    static_assert( ::is_function_v<T>, "");
    static_assert( ::is_function_v<const T>, "");
    static_assert( ::is_function_v<volatile T>, "");
    static_assert( ::is_function_v<const volatile T>, "");
}

template <class T>
void test_is_not_function()
{
    static_assert(!::is_function<T>::value, "");
    static_assert(!::is_function<const T>::value, "");
    static_assert(!::is_function<volatile T>::value, "");
    static_assert(!::is_function<const volatile T>::value, "");
    static_assert(!::is_function_v<T>, "");
    static_assert(!::is_function_v<const T>, "");
    static_assert(!::is_function_v<volatile T>, "");
    static_assert(!::is_function_v<const volatile T>, "");
}

class Empty
{
};

class NotEmpty
{
    virtual ~NotEmpty();
};

union Union {};

struct bit_zero
{
    int :  0;
};

class Abstract
{
    virtual ~Abstract() = 0;
};

enum Enum {zero, one};
struct incomplete_type;

typedef void (*FunctionPtr)();

int main()
{
	test_is_function<void(void)>();
	test_is_function<int(int)>();
	test_is_function<int(int, double)>();
	test_is_function<int(Abstract *)>();
	test_is_function<void(...)>();

  test_is_not_function<std::nullptr_t>();
  test_is_not_function<void>();
  test_is_not_function<int>();
  test_is_not_function<int&>();
  test_is_not_function<int&&>();
  test_is_not_function<int*>();
  test_is_not_function<double>();
  test_is_not_function<char[3]>();
  test_is_not_function<char[]>();
  test_is_not_function<Union>();
  test_is_not_function<Enum>();
  test_is_not_function<FunctionPtr>(); // function pointer is not a function
  test_is_not_function<Empty>();
  test_is_not_function<bit_zero>();
  test_is_not_function<NotEmpty>();
  test_is_not_function<Abstract>();
  test_is_not_function<Abstract*>();
  test_is_not_function<incomplete_type>();

  test_is_function<void() noexcept>();
  test_is_function<void() const && noexcept>();
}
