// https://www.reddit.com/r/cpp/comments/77lltx/c17_constexpr_function_arguments_kind_of/
#include <string_view>
#include <utility>
using namespace std::literals;

namespace detail
{
    template<class Type, bool = (((Type*)nullptr)->operator()(), true)>
    constexpr bool has_constexpr_pure_invoke(int) { return true; }

    template<class T>
    constexpr bool has_constexpr_pure_invoke(float) { return false; }

    template<class T>
    concept bool EmptyLambda = sizeof(T) <= 1 && has_constexpr_pure_invoke<T>(0);

    template<EmptyLambda T>
    struct lambda_holder
    {
        constexpr lambda_holder(T&&) {}
        static constexpr auto value = ((T*)nullptr)->operator()();
        constexpr auto operator*() const { return value; }
    };

    template<class T>
    lambda_holder(T&&) -> lambda_holder<T>;
}

// https://gcc.gnu.org/onlinedocs/cpp/Variadic-Macros.html#Variadic-Macros
// If your macro is complicated, you may want a more descriptive name for the variable argument than __VA_ARGS__. CPP permits this, as an extension. You may write an argument name immediately before the ‘…’; that name is used for the variable argument.
#define carg(x...) detail::lambda_holder([]() { return x; })

// userland starts here

// by type
template<class T> // advantage, T::value usable inside template argument list
constexpr auto f1(T const &) // const & instead of && to avoid use of std::decay_t on T
{
    constexpr auto arg = T::value;
    static_assert(arg == 3.14);
}

// part of Concept TS
// by value
constexpr auto f2(auto&& t) { constexpr auto arg = *t; /*...*/ }

template<char... Chars> struct template_string {};

template<class T>
constexpr auto make_template_string(T const &)
{
    // C++20 / Concept TS
    return []<size_t... Indexs>(std::index_sequence<Indexs...>) {
        return template_string<T::value[Indexs]...>{};
    }(std::make_index_sequence<T::value.length()>{});
}

int main()
{
    f1(carg(3.14));
    f2(carg(3.14));
    auto str = make_template_string(carg("hello"sv));
    static_assert(std::is_same_v<decltype(str), template_string<'h', 'e', 'l', 'l', 'o'>>);
}

#ifdef VALID_CPP_17

#include <string_view>
#include <utility>
using namespace std::literals;

 #define carg(...) ([]() constexpr -> decltype(auto) { return __VA_ARGS__; })

// userland starts here

// by type
template<class T>
constexpr auto f1(T value)
{
    constexpr auto arg = value();
    static_assert(arg == 3.14);
}

//by value
template<typename T>
constexpr auto f2(T t) { constexpr auto arg = t(); /*...*/ }

// Template strings
template<char... Chars> struct template_string {};

template<class T, std::size_t... Indexs>
constexpr auto make_template_string_helper(T value, std::index_sequence<Indexs...>)
{
    constexpr auto str = value();
    return template_string<str[Indexs]...>{};
}

template<class T>
constexpr auto make_template_string(T value)
{
    constexpr auto str = value();
    constexpr auto length = str.length();

    return make_template_string_helper(value, std::make_index_sequence<length>{});
}

int main()
{
    f1(carg(3.14));
    f2(carg(3.14));
    auto str = make_template_string(carg("hello"sv));
    static_assert(std::is_same_v<decltype(str), template_string<'h', 'e', 'l', 'l', 'o'>>);
}

#endif













